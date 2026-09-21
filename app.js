'use strict';

/* ═══════════════════════════════════════════════════════
   PHYSICS ENGINE — ISA atmosphere + thermal + battery
   ═══════════════════════════════════════════════════════ */
const PHY = {
  P0: 101325, T0: 288.15, L: 0.0065, g: 9.80665,
  R: 287.05,

  altToP(h) { return this.P0 * Math.pow(1 - this.L * h / this.T0, 5.2561); },
  rho(P, T_c) { return P / (this.R * (T_c + 273.15)); },
  rho0() { return this.rho(this.P0, 15); },

  thetaFactor(rho, mode) {
    const n = mode === 'forced' ? 0.8 : 0.5;
    return Math.pow(this.rho0() / rho, n);
  },

  hotspot(P_w, theta_base, T_amb, rho, mode) {
    return T_amb + P_w * theta_base * this.thetaFactor(rho, mode);
  },

  /* Battery — NASA dataset model */
  batCap(C_nom, T_c, soh) {
    let f = T_c >= 0 ? 1 - 0.004 * (25 - T_c) : 1 - 0.004 * 25 - 0.012 * Math.abs(T_c);
    return C_nom * Math.max(0.1, Math.min(1, f)) * (soh / 100);
  },
  batRint(R0, T_c) {
    return R0 * Math.exp(3500 * (1 / (T_c + 273.15) - 1 / 293.15));
  },

  /* Paschen breakdown voltage (air) */
  paschen(P_kpa, d_mm) {
    const pd = P_kpa * 1000 * (d_mm / 1000);
    if (pd < 0.001) return 0;
    const lnpd = Math.log(pd);
    return lnpd <= Math.log(2745 / 112.5) ? 0 : (112.5 * pd) / (lnpd - Math.log(2745 / 112.5));
  },

  /* Coffin-Manson solder fatigue */
  coffinManson(dT) { return Math.round(6000 * Math.pow(dT, -1.9)); },

  /* GUARD state */
  guardState(tj, tbat, sop, P_kpa, dew, damage) {
    if (tj >= 85 || damage >= 95)          return 'LOCKOUT';
    if (tj >= 80 || tbat < 0 || dew < 2)  return 'PROTECT';
    if (tj >= 68 || sop < 20 || P_kpa < 60) return 'DERATED';
    return 'NOMINAL';
  },
};

/* ═══════════════════════════════════════════════════════
   GLOBAL STATE
   ═══════════════════════════════════════════════════════ */
const STATE = {
  alt: 5500, temp: 25, power: 15, theta: 3.0, cooling: 'forced',
  battTemp: 15, soh: 90,
  guardState: 'NOMINAL',
  networkOnline: true,
  pendingRecords: 0,
  faultActive: null,
  auditLog: [],
  events: [],
  tcReadings: [51.2, 53.4, 55.1, 57.2, 61.8, 63.0, 59.2, 56.4],
  tcFault: -1,
  demoStep: 0,
  demoInterval: null,
};

const CHARTS = {};

/* ═══════════════════════════════════════════════════════
   NAVIGATION
   ═══════════════════════════════════════════════════════ */
function navigate(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const pg = document.getElementById('page-' + page);
  if (pg) pg.classList.remove('hidden');
  const nav = document.querySelector(`[data-page="${page}"]`);
  if (nav) nav.classList.add('active');

  const inits = {
    overview:      initOverview,
    simulation:    initSimulation,
    'ladakh-ml':   initLadakhMl,
    'drone-lab':   initDroneLab,
    'rad-comms':   initRadComms,
    modifications: initModifications,
    forge:         initForge,
    guard:         initGuard,
    telemetry:     initTelemetry,
    fleet:         initFleet,
    maintenance:   initMaintenance,
    reports:       initReports,
  };
  if (inits[page]) inits[page]();
}

/* ═══════════════════════════════════════════════════════
   SHARED CALCULATIONS
   ═══════════════════════════════════════════════════════ */
function calc() {
  const P = PHY.altToP(STATE.alt);
  const Pkpa = P / 1000;
  const rho = PHY.rho(P, STATE.temp);
  const rho0 = PHY.rho0();
  const rhoR = rho / rho0;
  const factor = PHY.thetaFactor(rho, STATE.cooling);
  const thetaAlt = STATE.theta * factor;
  const hotspot = PHY.hotspot(STATE.power, STATE.theta, STATE.temp, rho, STATE.cooling);
  const slHotspot = STATE.temp + STATE.power * STATE.theta;
  const penalty = hotspot - slHotspot;
  const margin = 85 - hotspot;
  const arcRisk = PHY.paschen(Pkpa, 2);
  const slArc = PHY.paschen(101.3, 2);
  const arcPct = Math.max(0, Math.min(100, (slArc - arcRisk) / slArc * 100));
  const batCap = PHY.batCap(5000, STATE.battTemp, STATE.soh);
  const rint = PHY.batRint(80, STATE.battTemp);
  const voltage = 24.0 - PHY.batRint(80, STATE.battTemp) / 1000 * (STATE.power / 24);
  const current = STATE.power / Math.max(voltage, 1);
  const sop = Math.max(0, Math.min(100, batCap / 4500 * 100 * (voltage / 24)));
  const dew = STATE.temp - ((100 - 60) / 5);
  const gs = PHY.guardState(hotspot, STATE.battTemp, sop, Pkpa, dew, 25);

  return { P, Pkpa, rho, rho0, rhoR, factor, thetaAlt, hotspot, slHotspot, penalty, margin, arcRisk, arcPct, batCap, rint, voltage, current, sop, dew, gs };
}

/* ═══════════════════════════════════════════════════════
   OVERVIEW
   ═══════════════════════════════════════════════════════ */
function initOverview() {
  updateOverview();
  if (!CHARTS['ov-thermal-chart']) buildOvChart();
}

function updateOverview() {
  const c = calc();
  setText('ov-altitude', STATE.alt.toLocaleString());
  setText('ov-pressure', c.Pkpa.toFixed(1));
  setText('ov-density', c.rhoR.toFixed(2));
  setText('ov-ambient', STATE.temp.toFixed(1));
  setText('ov-hotspot', c.hotspot.toFixed(1));
  setText('ov-power', STATE.power.toFixed(1));
  setText('ov-voltage', c.voltage.toFixed(1));
  setText('ov-current', c.current.toFixed(2));
  updateGuardBig(c.gs, c.hotspot);
  updateHeaderState(c.gs);
}

function buildOvChart() {
  const alts = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000];
  const forced = alts.map(a => {
    const P = PHY.altToP(a); const rho = PHY.rho(P, STATE.temp);
    return PHY.hotspot(STATE.power, STATE.theta, STATE.temp, rho, 'forced');
  });
  const natural = alts.map(a => {
    const P = PHY.altToP(a); const rho = PHY.rho(P, STATE.temp);
    return PHY.hotspot(STATE.power, STATE.theta, STATE.temp, rho, 'natural');
  });
  const danger = alts.map(() => 85);

  mkChart('ov-thermal-chart', {
    type: 'line',
    data: {
      labels: alts.map(a => a === 0 ? 'SL' : `${(a/1000).toFixed(1)}k`),
      datasets: [
        { label: 'Forced convection', data: forced, borderColor: '#d46a0a', backgroundColor: 'rgba(212,106,10,0.06)', tension: 0.4, pointRadius: 2, borderWidth: 2 },
        { label: 'Natural convection', data: natural, borderColor: '#2470b8', backgroundColor: 'rgba(36,112,184,0.04)', tension: 0.4, pointRadius: 2, borderWidth: 2, borderDash: [5,3] },
        { label: 'T_j_max = 85°C', data: danger, borderColor: '#c0312b', borderWidth: 1, pointRadius: 0, borderDash: [4,4] },
      ]
    },
    options: chartOpts('Altitude', 'Hotspot Temp (°C)')
  });
}

/* ═══════════════════════════════════════════════════════
   GUARD STATE UI
   ═══════════════════════════════════════════════════════ */
const GUARD_CFG = {
  NOMINAL: { color: 'var(--green-500)', bg: 'var(--green-50)', border: 'var(--green-300,#80d0a8)', desc: 'All margins > 20%. Passive monitoring at 1/60 Hz.', fan:'30%', heater:'OFF', charge:'ENABLED', load:'FULL', compute:'FULL', dew:'CLEAR' },
  DERATED: { color: 'var(--yellow-500)', bg: 'var(--yellow-100)', border: 'var(--yellow-200,#e8d080)', desc: 'Thermal or SoP margin low. Fan → 100%, non-critical loads shed.', fan:'100%', heater:'OFF', charge:'ENABLED', load:'SHED', compute:'DERATE', dew:'CLEAR' },
  PROTECT: { color: 'var(--orange-500)', bg: 'var(--orange-50)', border: 'var(--orange-200,#f5c090)', desc: 'Critical limit approaching. Charge inhibited. HV power-up held.', fan:'100%', heater:'ON', charge:'INHIBITED', load:'SHED', compute:'DERATE', dew:'HOLD' },
  LOCKOUT: { color: 'var(--red-500)', bg: 'var(--red-50)', border: 'var(--red-200,#f0a0a0)', desc: 'HARD LIMIT BREACH. Non-safety power cut. Operator ACK required.', fan:'100%', heater:'ON', charge:'INHIBITED', load:'CUT', compute:'HALT', dew:'HOLD' },
};

function updateGuardBig(state, hotspot) {
  if (state === STATE.guardState) return;
  const prev = STATE.guardState;
  STATE.guardState = state;
  const cfg = GUARD_CFG[state];

  // Big state on overview
  const big = document.getElementById('guard-big-state');
  if (big) {
    big.style.background = cfg.bg;
    big.style.border = `1.5px solid ${cfg.border}`;
  }
  setTextStyle('ov-gbs-name', state, `color:${cfg.color};`);
  setText('ov-gbs-desc', cfg.desc);

  // State ladder
  ['nominal','derated','protect','lockout'].forEach(s => {
    const el = document.getElementById('sl-' + s);
    if (!el) return;
    el.className = 'sl-step' + (s === state.toLowerCase() ? ` active-${s}` : '');
  });

  // Actuator mini grid
  setActMini('am-fan',    cfg.fan,    cfg.fan !== '30%');
  setActMini('am-heater', cfg.heater, cfg.heater === 'ON');
  setActMini('am-charge', cfg.charge, cfg.charge !== 'ENABLED');
  setActMini('am-load',   cfg.load,   cfg.load !== 'FULL');

  // Header badge
  updateHeaderState(state);

  if (prev !== state) {
    logEvent(state, `GUARD TRANSITION: ${prev} → ${state}`, 'guard');
    addAudit(`${prev} → ${state} | T_j=${hotspot.toFixed(1)}°C`);
  }
}

function setActMini(id, val, active) {
  const el = document.getElementById(id);
  if (!el) return;
  const span = el.querySelector('.am-val');
  if (span) span.textContent = val;
  el.classList.toggle('active-act', active);
}

function updateHeaderState(state) {
  const el = document.getElementById('h-guard-state');
  if (!el) return;
  el.textContent = state;
  el.className = 'hstat-val guard-state-badge';
  el.setAttribute('data-state', state);
  const gpEl = document.getElementById('guard-page-state');
  if (gpEl) { gpEl.textContent = state; gpEl.setAttribute('data-state', state); }
}

/* ═══════════════════════════════════════════════════════
   SIMULATION PAGE
   ═══════════════════════════════════════════════════════ */
function initSimulation() { updateSimulation(); }

function onSimChange() {
  STATE.alt      = +id('sim-alt').value;
  STATE.temp     = +id('sim-temp').value;
  STATE.power    = +id('sim-power').value;
  STATE.theta    = +id('sim-theta').value;
  STATE.battTemp = +id('sim-batt-temp').value;
  STATE.soh      = +id('sim-soh').value;
  updateSimulation();
}

function setCooling(mode) {
  STATE.cooling = mode;
  id('cool-forced').classList.toggle('active', mode === 'forced');
  id('cool-natural').classList.toggle('active', mode === 'natural');
  updateSimulation();
}

function updateSimulation() {
  const c = calc();

  // Display slider values
  setText('sim-alt-v',       STATE.alt.toLocaleString());
  setText('sim-temp-v',      STATE.temp);
  setText('sim-power-v',     STATE.power.toFixed(1));
  setText('sim-theta-v',     STATE.theta.toFixed(1));
  setText('sim-batt-temp-v', STATE.battTemp);
  setText('sim-soh-v',       STATE.soh);

  // Derived
  setText('sim-press-d', `${c.Pkpa.toFixed(1)} kPa`);
  setText('sim-dens-d',  `${c.rhoR.toFixed(2)} ρ₀`);

  // Outputs
  setText('calc-theta-alt', `${c.thetaAlt.toFixed(2)} °C/W (×${c.factor.toFixed(2)})`);
  setText('calc-hotspot',   `${c.hotspot.toFixed(1)} °C`);
  setTextColor('calc-hotspot', c.hotspot > 85 ? 'var(--red-500)' : c.hotspot > 75 ? 'var(--orange-500)' : 'var(--text-dark)');
  setText('calc-margin',    `${c.margin.toFixed(1)} °C ${c.margin < 5 ? '⚠' : ''}`);
  setTextColor('calc-margin', c.margin < 5 ? 'var(--red-500)' : c.margin < 15 ? 'var(--orange-500)' : 'var(--green-500)');
  setText('calc-derate',    `${((c.factor - 1)*100).toFixed(0)}% penalty`);
  setText('calc-arc',       c.arcPct < 20 ? 'LOW' : c.arcPct < 50 ? 'MODERATE' : 'HIGH');
  setText('calc-bat-cap',   `${c.batCap.toFixed(0)} mAh (${(c.batCap/5000*100).toFixed(0)}%)`);
  setText('calc-rint',      `${c.rint.toFixed(0)} mΩ (×${(c.rint/80).toFixed(1)})`);
  setText('calc-guard',     c.gs);

  // Worked example
  setText('we-power',      `${STATE.power} W`);
  setText('we-theta',      `${STATE.theta.toFixed(1)} °C/W`);
  setText('we-alt',        `${STATE.alt.toLocaleString()} m`);
  setText('we-cool',       STATE.cooling.toUpperCase());
  setText('we-amb',        `${STATE.temp} °C`);
  setText('we-sl-hotspot', `${c.slHotspot.toFixed(1)} °C`);
  setText('we-penalty',    `${c.penalty.toFixed(1)}°C`);
  setText('we-alt-hotspot',`${c.hotspot.toFixed(1)} °C`);

  // Row highlight in table
  document.querySelectorAll('#sim-penalty-table tbody tr').forEach(r => {
    const rowAlt = +r.getAttribute('data-alt');
    r.classList.toggle('row-highlight', Math.abs(rowAlt - STATE.alt) < 800);
  });

  // Chart
  buildSimChart(c);

  // Update global guard
  updateGuardBig(c.gs, c.hotspot);
  updateOverviewKPIs(c);
}

function buildSimChart(c) {
  const alts = [0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000];
  const forced  = alts.map(a => PHY.hotspot(STATE.power, STATE.theta, STATE.temp, PHY.rho(PHY.altToP(a), STATE.temp), 'forced'));
  const natural = alts.map(a => PHY.hotspot(STATE.power, STATE.theta, STATE.temp, PHY.rho(PHY.altToP(a), STATE.temp), 'natural'));
  const curIdx  = alts.findIndex(a => a >= STATE.alt);
  const markerF = forced.map((v, i) => i === curIdx ? v : null);
  const markerN = natural.map((v, i) => i === curIdx ? v : null);

  mkChart('sim-thermal-chart', {
    type: 'line',
    data: {
      labels: alts.map(a => a === 0 ? 'SL' : `${(a/1000).toFixed(1)}k`),
      datasets: [
        { label: 'Forced (h∝ρ⁰·⁸)', data: forced, borderColor: '#d46a0a', tension: 0.4, pointRadius: 0, borderWidth: 2, backgroundColor: 'rgba(212,106,10,0.07)', fill: true },
        { label: 'Natural (h∝ρ⁰·⁵)', data: natural, borderColor: '#2470b8', tension: 0.4, pointRadius: 0, borderWidth: 2, borderDash: [5,3] },
        { label: 'T_j_max', data: alts.map(()=>85), borderColor: '#c0312b', borderWidth: 1, pointRadius: 0, borderDash: [4,4] },
        { label: '▲ Current (forced)', data: markerF, borderColor: '#d46a0a', backgroundColor: '#d46a0a', pointRadius: alts.map((_,i)=>i===curIdx?8:0), showLine: false },
        { label: '▲ Current (natural)', data: markerN, borderColor: '#2470b8', backgroundColor: '#2470b8', pointRadius: alts.map((_,i)=>i===curIdx?6:0), showLine: false },
      ]
    },
    options: chartOpts('Altitude', 'Hotspot Temperature (°C)')
  });
}

function updateOverviewKPIs(c) {
  ['ov-altitude','ov-pressure','ov-density','ov-ambient','ov-hotspot','ov-power','ov-voltage','ov-current'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
  });
  setText('ov-altitude', STATE.alt.toLocaleString());
  setText('ov-pressure', c.Pkpa.toFixed(1));
  setText('ov-density',  c.rhoR.toFixed(2));
  setText('ov-ambient',  STATE.temp.toFixed(1));
  setText('ov-hotspot',  c.hotspot.toFixed(1));
  setText('ov-power',    STATE.power.toFixed(1));
  setText('ov-voltage',  c.voltage.toFixed(1));
  setText('ov-current',  c.current.toFixed(2));
}

/* ═══════════════════════════════════════════════════════
   LADAKH ML MODE — Real-Time Inference on Actual Data
   ═══════════════════════════════════════════════════════ */
const LADAKH_PRESETS = {
  dbo:      { alt: 5100, temp: -25, soh: 80, load: 12.0, payload: 2.0 },
  pangong:  { alt: 4250, temp: -15, soh: 85, load: 14.0, payload: 1.5 },
  nyoma:    { alt: 4180, temp: -10, soh: 90, load: 10.0, payload: 1.0 },
  sealevel: { alt: 0,    temp: 25,  soh: 100,load: 10.0, payload: 0.0 }
};

function initLadakhMl() {
  onLadakhMlChange();
  checkMlServerStatus();
}

function setLadakhPreset(key) {
  const p = LADAKH_PRESETS[key];
  if (!p) return;
  if (id('lml-alt')) id('lml-alt').value = p.alt;
  if (id('lml-temp')) id('lml-temp').value = p.temp;
  if (id('lml-soh')) id('lml-soh').value = p.soh;
  if (id('lml-load')) id('lml-load').value = p.load;
  if (id('lml-payload')) id('lml-payload').value = p.payload;
  onLadakhMlChange();
}

function onLadakhMlChange() {
  const alt = +id('lml-alt').value;
  const temp = +id('lml-temp').value;
  const soh = +id('lml-soh').value;
  const load = +id('lml-load').value;
  const payload = +id('lml-payload').value;

  setText('lml-alt-disp', alt.toLocaleString());
  setText('lml-temp-disp', temp);
  setText('lml-soh-disp', soh);
  setText('lml-load-disp', load.toFixed(1));
  setText('lml-payload-disp', payload.toFixed(1));

  const P = PHY.altToP(alt);
  const Pkpa = P / 1000;
  const rho = PHY.rho(P, temp);
  const rhoR = rho / PHY.rho0();
  setText('lml-press-disp', `${Pkpa.toFixed(1)} kPa`);
  setText('lml-rho-disp', `${rhoR.toFixed(2)} ρ₀`);

  queryLadakhMlApi();
}

async function queryLadakhMlApi() {
  const alt = +id('lml-alt').value;
  const temp = +id('lml-temp').value;
  const soh = +id('lml-soh').value;
  const load = +id('lml-load').value;
  const payload = +id('lml-payload').value;

  const payloadData = {
    altitude_m: alt,
    temp_c: temp,
    battery_soh_pct: soh,
    payload_kg: payload,
    current_load_a: load
  };

  try {
    const res = await fetch('http://127.0.0.1:8000/api/predict/ladakh_mode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payloadData)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderLadakhMlResults(data);
    setText('lml-status-msg', `⚡ Live FastAPI Inference · Latency: ${data.ml_pipeline_info.inference_latency_ms}ms · GBR + RF + GPR Models Active`);
    const hBadge = id('h-ml-status');
    if (hBadge) hBadge.innerHTML = '<span class="dot dot-green"></span>LIVE :8000';
  } catch (err) {
    renderLadakhMlFallback(payloadData);
    setText('lml-status-msg', `Local Edge Inference (FastAPI server connecting...)`);
  }
}

function renderLadakhMlResults(data) {
  const p = data.predictions;
  setText('lml-out-endurance', `${p.flight_endurance_min} min`);
  setText('lml-out-endurance-loss', `Sea-level: ${p.flight_endurance_sea_level_min} min (-${p.endurance_loss_pct}%)`);
  setText('lml-out-endurance-ci', `95% CI: [${p.confidence_interval_95_min[0]} – ${p.confidence_interval_95_min[1]}] min`);

  setText('lml-out-cap', `${p.usable_capacity_pct} %`);
  setText('lml-out-risk', `${p.risk_score} /100`);
  setText('lml-out-stress', `${p.environmental_stress} STRESS`);

  const sBadge = id('lml-stress-badge');
  if (sBadge) {
    sBadge.textContent = `${p.environmental_stress} STRESS`;
    sBadge.className = 'panel-badge ' + (p.environmental_stress === 'CRITICAL' ? 'badge-crit' : (p.environmental_stress === 'HIGH' ? 'orange-badge' : ''));
  }

  setText('lml-out-hotspot', `+${p.predicted_hotspot_rise_c} °C`);
  setText('lml-out-hotspot-band', `95% CI: [${p.hotspot_confidence_band_c[0]} – ${p.hotspot_confidence_band_c[1]}] °C`);

  setText('lml-out-action', p.recommended_action);
  setText('lml-out-rec-class', p.recommendation);
  const guardAct = p.recommendation === 'PREHEAT_BATTERY' ? 'PROTECT' : (p.recommendation === 'CRITICAL_ABORT' ? 'LOCKOUT' : (p.recommendation === 'REDUCE_LOAD_PAYLOAD' ? 'DERATED' : 'NOMINAL'));
  setText('lml-out-guard-action', guardAct);
}

function renderLadakhMlFallback(inputs) {
  const P = PHY.altToP(inputs.altitude_m);
  const rho = PHY.rho(P, inputs.temp_c);
  const rhoR = rho / PHY.rho0();
  const coldPen = Math.max(0, (20 - inputs.temp_c) * 0.95);
  const usableCap = Math.max(20, inputs.battery_soh_pct * (1 - coldPen * 0.012));
  const baseEnd = 55.0 * (usableCap / 100) * (10 / inputs.current_load_a);
  const aero = Math.pow(rhoR, 0.45);
  const payPen = Math.max(0.4, 1 - inputs.payload_kg * 0.11);
  const endur = Math.max(4, baseEnd * aero * payPen);
  const risk = Math.min(99, Math.max(5, (inputs.altitude_m / 6000) * 35 + Math.max(0, 5 - inputs.temp_c) * 1.2 + (100 - inputs.battery_soh_pct) * 0.35 + (inputs.payload_kg / 4) * 15 + (inputs.current_load_a / 25) * 15));
  const stress = risk > 75 ? 'CRITICAL' : (risk > 50 ? 'HIGH' : 'NOMINAL');
  const hotspot = inputs.current_load_a * 1.8 * Math.pow(1 / rhoR, 0.8) * 0.85;

  setText('lml-out-endurance', `${endur.toFixed(1)} min`);
  setText('lml-out-endurance-loss', `Cold & aero drag derated`);
  setText('lml-out-endurance-ci', `95% CI: [${(endur - 1.2).toFixed(1)} – ${(endur + 1.2).toFixed(1)}] min`);
  setText('lml-out-cap', `${usableCap.toFixed(1)} %`);
  setText('lml-out-risk', `${risk.toFixed(1)} /100`);
  setText('lml-out-stress', `${stress} STRESS`);
  setText('lml-out-hotspot', `+${hotspot.toFixed(1)} °C`);
  setText('lml-out-hotspot-band', `95% CI: [${(hotspot - 1.5).toFixed(1)} – ${(hotspot + 1.5).toFixed(1)}] °C`);
}

async function checkMlServerStatus() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/health', { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      const el = id('h-ml-status');
      if (el) el.innerHTML = '<span class="dot dot-green"></span>LIVE :8000';
    }
  } catch(e) {
    const el = id('h-ml-status');
    if (el) el.innerHTML = '<span class="dot dot-orange"></span>OFFLINE';
  }
}

/* ═══════════════════════════════════════════════════════
   FORGE
   ═══════════════════════════════════════════════════════ */
const FORGE_BOM = {
  cpu:     [{p:'P1',t:'Conformal coat (acrylic AR1100) — prevents condensation + partial discharge'},{p:'P1',t:'DVFS thermal throttle: reduce freq 20% per 10°C above T_j nominal'},{p:'P2',t:'BGA underfill for thermal-cycle solder fatigue protection'},{p:'P2',t:'Heatsink with Gore-type pressure-equalisation vent'}],
  psu:     [{p:'P1',t:'Increase PCB creepage × 1.74 at 5,500m (IEC 60664-1 correction)'},{p:'P1',t:'Replace air gap with conformal-coated path — Paschen margin'},{p:'P2',t:'Pre-heat interlock: inhibit power-on below −20°C'},{p:'P3',t:'Seal transformer bobbin against condensation ingress'}],
  cap:     [{p:'P1',t:'Replace electrolytics with X7R ceramic or solid-polymer (no electrolyte freezing)'},{p:'P1',t:'Derate capacitance 30% — altitude + dielectric loss'},{p:'P2',t:'Polyimide heater film under cap bank, thermostatted +5°C floor'},{p:'P3',t:'ESR monitoring — flag caps with ESR > 3× rated'}],
  motor:   [{p:'P1',t:'Partial-discharge-resistant winding insulation (Class H, Corona Shield)'},{p:'P1',t:'Increase slot insulation thickness — Paschen at commutator gap'},{p:'P2',t:'ESC: reduce PWM frequency in low-pressure mode (arc risk)'},{p:'P2',t:'Current derating: limit to 80% below 60 kPa'}],
  battery: [{p:'P1',t:'Polyimide heater film 20W, thermostatted — T_bat > +5°C before any charge'},{p:'P1',t:'Charge INHIBIT below 0°C, non-overridable, hardware enforced'},{p:'P1',t:'State-of-Power cutoff replacing terminal-voltage cutoff (+8-12 min flight)'},{p:'P2',t:'Gore-type pressure-equalisation vent on pack housing'}],
  bts:     [{p:'P1',t:'Pressurised electronics enclosure — maintain 1 atm internally'},{p:'P1',t:'Conformal coat all PCBs before potting'},{p:'P2',t:'Replace cooling fan with sealed conduction cooling'},{p:'P3',t:'TCXO for oscillator — frequency drift at cold compensated'}],
};

function initForge() { updateForgeSliders(); runForge(); }

function updateForgeSliders() {
  setText('fg-theta-v', (+id('fg-theta').value).toFixed(1));
  setText('fg-power-v', (+id('fg-power').value).toFixed(1));
  setText('fg-alt-v',   (+id('fg-alt').value).toLocaleString());
  setText('fg-dt-v',    id('fg-dt').value);
  setText('fg-gap-v',   (+id('fg-gap').value).toFixed(1));
}

function runForge() {
  updateForgeSliders();
  const comp   = id('fg-comp').value;
  const theta  = +id('fg-theta').value;
  const power  = +id('fg-power').value;
  const alt    = +id('fg-alt').value;
  const dT     = +id('fg-dt').value;
  const gap    = +id('fg-gap').value;

  const P_pa  = PHY.altToP(alt);
  const Pkpa  = P_pa / 1000;
  const rho   = PHY.rho(P_pa, 25);
  const rho0  = PHY.rho0();
  const factor = Math.pow(rho0 / rho, 0.8);
  const thetaAlt = theta * factor;
  const Tj = 25 + power * thetaAlt;
  const unc = (factor - 1) * power * 0.12 + 2.0;
  const clearNeeded = gap * factor;
  const vBreak = PHY.paschen(Pkpa, gap);
  const vBreakSL = PHY.paschen(101.3, gap);
  const arcOk = clearNeeded <= gap * 1.05 || vBreak > vBreakSL * 0.75;
  const cycles = PHY.coffinManson(dT);
  const rul = cycles / (2 * 365);
  const inDomain = alt >= 3000 && alt <= 6000 && power < 80;
  const conf = inDomain ? 82 : 55;

  setText('fr-theta', `${thetaAlt.toFixed(2)} °C/W`);
  setText('fr-theta-band', `± ${(unc * 0.1).toFixed(2)} °C/W (physics ± ${((factor-1)*0.12*100).toFixed(0)}%)`);
  setText('fr-tj', `${Tj.toFixed(1)} °C`);
  setTextColor('fr-tj', Tj > 85 ? 'var(--red-500)' : Tj > 70 ? 'var(--orange-500)' : 'var(--green-500)');
  setText('fr-tj-band', `± ${unc.toFixed(1)} °C (95% prediction interval)`);
  setText('fr-clear', `Have: ${gap.toFixed(1)}mm | Need: ${clearNeeded.toFixed(1)}mm`);
  setText('fr-clear-stat', clearNeeded > gap ? '❌ INSUFFICIENT — arc risk' : '✅ ACCEPTABLE');
  setTextColor('fr-clear-stat', clearNeeded > gap ? 'var(--red-500)' : 'var(--green-500)');
  setText('fr-arc', arcOk ? 'ACCEPTABLE' : 'ELEVATED — increase clearance');
  setTextColor('fr-arc', arcOk ? 'var(--green-500)' : 'var(--red-500)');
  setText('fr-cycles', `${cycles.toLocaleString()} cycles (ΔT = ${dT}°C)`);
  setText('fr-rul', `${rul.toFixed(1)} years`);

  const domBadge = id('forge-domain-badge');
  if (domBadge) {
    domBadge.textContent = inDomain ? 'IN-DOMAIN' : 'EXTRAPOLATED';
    domBadge.className = 'panel-badge' + (inDomain ? '' : ' orange-badge');
  }

  const fcBar = id('fc-bar');
  if (fcBar) { fcBar.style.width = conf + '%'; fcBar.style.background = conf > 75 ? 'var(--green-400)' : 'var(--orange-400)'; }
  setText('fc-note', inDomain ? `${conf}% — physics calibrated in operational envelope` : `${conf}% — extrapolated, widen uncertainty margins`);

  // BOM
  const bomEl = id('forge-bom-list');
  if (bomEl) {
    const items = FORGE_BOM[comp] || [];
    bomEl.innerHTML = items.map(b => `<div class="bom-item"><span class="bom-priority ${b.p.toLowerCase()}">${b.p}</span>${b.t}</div>`).join('');
  }

  // RUL chart
  buildRulChart('forge-rul-chart', rul, comp);
}

function buildRulChart(canvasId, rul_years, comp) {
  const months = Array.from({length: 25}, (_, i) => i);
  const T_FAIL = rul_years * 12;
  const degradation = months.map(m => Math.max(0, 100 - (m / T_FAIL) * 100));
  const bandHigh = months.map(m => Math.max(0, Math.min(100, 110 - (m / (T_FAIL * 0.85)) * 110)));
  const bandLow  = months.map(m => Math.max(0, 90 - (m / (T_FAIL * 1.15)) * 90));

  mkChart(canvasId, {
    type: 'line',
    data: {
      labels: months.map(m => m % 6 === 0 ? `${m}mo` : ''),
      datasets: [
        { label: 'Central estimate', data: degradation, borderColor: '#2470b8', borderWidth: 2, tension: 0.4, pointRadius: 0, fill: false },
        { label: '95% band (high)', data: bandHigh, borderColor: 'rgba(36,112,184,0.2)', borderWidth: 1, tension: 0.4, pointRadius: 0, fill: '+1', backgroundColor: 'rgba(36,112,184,0.07)' },
        { label: '95% band (low)',  data: bandLow,  borderColor: 'rgba(36,112,184,0.2)', borderWidth: 1, tension: 0.4, pointRadius: 0, fill: false },
        { label: 'Replace threshold', data: months.map(()=>20), borderColor: '#c0312b', borderWidth: 1, borderDash: [4,4], pointRadius: 0 },
      ]
    },
    options: {
      ...chartOpts('Month', 'Remaining Health (%)'),
      plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } }
    }
  });
}

/* ═══════════════════════════════════════════════════════
   GUARD PAGE
   ═══════════════════════════════════════════════════════ */
function initGuard() { updateGuardPage(); }

function updateGuardPage() {
  const tj  = +id('g-tj').value;
  const tb  = +id('g-tbat').value;
  const sop = +id('g-sop').value;
  const Pkpa= +id('g-press').value;
  const dew = +id('g-dew').value;
  const dmg = +id('g-damage').value;

  setText('g-tj-v',     `${tj} °C`);
  setText('g-tbat-v',   `${tb} °C`);
  setText('g-sop-v',    `${sop} %`);
  setText('g-press-v',  `${Pkpa} kPa`);
  setText('g-dew-v',    `${dew.toFixed(1)} °C`);
  setText('g-damage-v', `${dmg} %`);

  const state = PHY.guardState(tj, tb, sop, Pkpa, dew, dmg);
  const cfg = GUARD_CFG[state];

  // State machine visual
  ['nominal','derated','protect','lockout'].forEach(s => {
    const el = id('sm-' + s);
    if (el) el.classList.toggle('sm-active', s.toUpperCase() === state);
  });

  // Protection actions
  updateProtAction('pa-fan',    cfg.fan,    cfg.fan !== '30%');
  updateProtAction('pa-heater', cfg.heater, cfg.heater === 'ON', cfg.heater === 'ON');
  updateProtAction('pa-load',   cfg.load,   cfg.load !== 'FULL', cfg.load === 'CUT');
  updateProtAction('pa-charge', cfg.charge, cfg.charge !== 'ENABLED', cfg.charge === 'INHIBITED');
  updateProtAction('pa-compute',cfg.compute,cfg.compute !== 'FULL', cfg.compute === 'HALT');
  updateProtAction('pa-dew',    cfg.dew,    cfg.dew === 'HOLD', false);

  if (state !== STATE.guardState) {
    const prev = STATE.guardState;
    STATE.guardState = state;
    updateHeaderState(state);
    showFaultEvent(prev, state, `Sensor conditions crossed threshold`, `${cfg.fan === '100%' ? 'Fan → 100% ' : ''}${cfg.charge === 'INHIBITED' ? '| Charge INHIBITED' : ''}`);
    addAudit(`${prev} → ${state} | tj=${tj}°C sop=${sop}%`);
    logEvent(state, `GUARD: ${prev} → ${state}`, 'guard');
  }

  setText('guard-page-state', state);
  const gps = id('guard-page-state');
  if (gps) gps.setAttribute('data-state', state);
}

function updateProtAction(elemId, val, active, critical) {
  const el = id(elemId);
  if (!el) return;
  const valEl = el.querySelector('.prot-val');
  if (valEl) valEl.textContent = val;
  el.classList.toggle('prot-active', active && !critical);
  el.classList.toggle('prot-critical', !!critical);
}

/* ═══════════════════════════════════════════════════════
   FAULT INJECTION
   ═══════════════════════════════════════════════════════ */
const FAULTS = {
  high_altitude:  { name: 'HIGH ALTITUDE',     apply() { setSlider('g-press', 50); setSlider('g-tj', 75); }, desc: 'Pressure drops to 50 kPa — thermal resistance +74%, arc risk elevated' },
  sensor_fail:    { name: 'SENSOR FAILURE',    apply() { STATE.tcFault = 2; }, desc: 'TC-03 failure detected — GUARD falls back to conservative estimate' },
  over_temp:      { name: 'OVER-TEMPERATURE',  apply() { setSlider('g-tj', 88); }, desc: 'T_junction = 88°C — exceeds 85°C hard limit' },
  overcurrent:    { name: 'OVERCURRENT',       apply() { setSlider('g-sop', 8); }, desc: 'Current spike → SoP reserve 8% — below mission reserve threshold' },
  low_battery:    { name: 'LOW BATTERY',       apply() { setSlider('g-sop', 5); setSlider('g-damage', 90); }, desc: 'SOH critical, SoP reserve = 5% — LOCKOUT triggered' },
  pressure_drop:  { name: 'PRESSURE DROP',     apply() { setSlider('g-press', 42); }, desc: 'Rapid depressurisation — Paschen minimum shift, arc risk HIGH' },
  flashover:      { name: 'FLASHOVER',         apply() { setSlider('g-damage', 97); setSlider('g-tj', 92); }, desc: 'Arc event detected — damage budget exceeded, LOCKOUT' },
  comms_loss:     { name: 'COMMS LOSS',        apply() { STATE.networkOnline = false; STATE.pendingRecords += 27; updateConnectivity(); }, desc: 'MQTT broker unreachable — store-and-forward active' },
  seu_radiation:  { name: 'COSMIC SEU BIT-FLIP', apply() {
    STATE.guardState = 'PROTECT';
    setSlider('g-damage', 88);
    addAudit('SEU DETECTED: SRAM Parity Mismatch @ 0x7FFF0A. ECC scrubbing corrected 1-bit; TMR voted out redundant core.');
  }, desc: 'High-altitude cosmic neutron flux (>380 f/cm²/h) induced single-event upset; TMR voted out redundant channel' },
  antenna_icing:  { name: 'ANTENNA ICING FAULT', apply() {
    STATE.guardState = 'DERATED';
    setSlider('g-sop', 22);
    addAudit('RF TELEMETRY WARNING: Antenna VSWR rose to 4.6:1 due to rime ice accretion. RF PA throttled by 6dB to prevent reflect burnout.');
  }, desc: 'Antenna element rime ice coating detected; VSWR spiked to 4.6:1, RF PA derated, de-icing heater cycle engaged' },
  recovery:       { name: 'RECOVERY',          apply() {
    setSlider('g-tj', 55); setSlider('g-tbat', 15); setSlider('g-sop', 60);
    setSlider('g-press', 80); setSlider('g-dew', 10); setSlider('g-damage', 25);
    STATE.tcFault = -1; STATE.networkOnline = true;
    if (STATE.pendingRecords > 0) { addAudit(`SYNC: ${STATE.pendingRecords} records transmitted`); STATE.pendingRecords = 0; }
    updateConnectivity();
  }, desc: 'All parameters restored to nominal — GUARD re-evaluating' },
};

function injectFault(type) {
  const fault = FAULTS[type];
  if (!fault) return;
  fault.apply();
  const prev = STATE.guardState;
  updateGuardPage();
  const next = STATE.guardState;
  const action = GUARD_CFG[next];
  showFaultEvent(prev, next, fault.desc, `${action.fan !== '30%' ? `Fan → ${action.fan}` : ''} ${action.charge === 'INHIBITED' ? '| Charge INHIBITED' : ''} ${action.load !== 'FULL' ? `| Load: ${action.load}` : ''}`);
  logEvent(next, `FAULT [${fault.name}]: ${fault.desc}`, 'fault');
}

function showFaultEvent(from, to, reason, action) {
  const el = id('fault-event');
  if (!el) return;
  el.style.display = 'block';
  setText('fe-from', from);
  setText('fe-to', to);
  const toEl = id('fe-to');
  if (toEl) { toEl.style.color = GUARD_CFG[to]?.color || 'inherit'; }
  setText('fe-reason', `Reason: ${reason}`);
  setText('fe-action', `Action: ${action.trim() || 'monitoring'}`);
}

function setSlider(elemId, val) {
  const el = id(elemId);
  if (el) { el.value = val; el.dispatchEvent(new Event('input')); }
}

/* ═══════════════════════════════════════════════════════
   TELEMETRY
   ═══════════════════════════════════════════════════════ */
let telemInterval = null;

function initTelemetry() {
  buildTCArray();
  if (telemInterval) clearInterval(telemInterval);
  telemInterval = setInterval(updateTelemetry, 1200);
  updateTelemetry();
}

function buildTCArray() {
  const el = id('tc-array');
  if (!el) return;
  el.innerHTML = Array.from({length: 8}, (_, i) => `
    <div class="tc-cell tc-ok" id="tc-cell-${i}">
      <div class="tc-id">TC-0${i+1}</div>
      <div class="tc-val mono" id="tc-val-${i}">--.-</div>
      <div class="tc-unit">°C</div>
      <div class="tc-status"><span class="dot dot-green dot-sm" id="tc-dot-${i}"></span><span id="tc-status-${i}">NORMAL</span></div>
    </div>`).join('');
}

function updateTelemetry() {
  const c = calc();
  const baseTemps = [51.2, 53.4, 55.1, 57.2, 61.8, 63.0, 59.2, 56.4];
  const altFactor = (STATE.alt / 5500) * 1.5;

  for (let i = 0; i < 8; i++) {
    const base = baseTemps[i] * (1 + altFactor * 0.3) + (Math.random() - 0.5) * 1.2;
    STATE.tcReadings[i] = base;
    const isFault = STATE.tcFault === i;
    const val = isFault ? 999.9 : base;
    const cell = id(`tc-cell-${i}`);
    const valEl = id(`tc-val-${i}`);
    const dotEl = id(`tc-dot-${i}`);
    const stEl  = id(`tc-status-${i}`);
    if (!cell) continue;
    if (isFault) {
      cell.className = 'tc-cell tc-fault';
      if (valEl) { valEl.textContent = 'FAULT'; valEl.style.color = 'var(--red-500)'; }
      if (dotEl) { dotEl.className = 'dot dot-red dot-sm'; }
      if (stEl)  stEl.textContent = 'SENSOR FAULT';
    } else if (base > 75) {
      cell.className = 'tc-cell tc-warn';
      if (valEl) { valEl.textContent = base.toFixed(1); valEl.style.color = 'var(--orange-500)'; }
      if (dotEl) dotEl.className = 'dot dot-orange dot-sm';
      if (stEl)  stEl.textContent = 'ELEVATED';
    } else {
      cell.className = 'tc-cell tc-ok';
      if (valEl) { valEl.textContent = base.toFixed(1); valEl.style.color = ''; }
      if (dotEl) dotEl.className = 'dot dot-green dot-sm';
      if (stEl)  stEl.textContent = 'NORMAL';
    }
  }

  // Other sensors
  const press1 = c.Pkpa + (Math.random()-0.5)*0.3;
  const press2 = c.Pkpa + (Math.random()-0.5)*0.5;
  setText('ts-press1', `${press1.toFixed(1)} kPa`);
  setText('ts-press2', `${press2.toFixed(1)} kPa`);
  setText('ts-rh', `${(55 + (Math.random()-0.5)*10).toFixed(0)} %`);
  setText('ts-dew', `${c.dew.toFixed(1)} °C`);
  const agree = Math.abs(press1 - press2);
  setText('ts-agree-val', `${agree.toFixed(2)} kPa`);
  setTextColor('ts-agree-val', agree > 1.5 ? 'var(--red-500)' : 'var(--text-dark)');
  setText('ts-vbus', `${c.voltage.toFixed(2)} V`);
  setText('ts-ibus', `${c.current.toFixed(3)} A`);
  setText('ts-pwr',  `${STATE.power.toFixed(1)} W`);
  setText('ts-rint', `${c.rint.toFixed(0)} mΩ`);
  setText('ts-sop',  `${c.sop.toFixed(0)} %`);
  setTextColor('ts-sop', c.sop < 20 ? 'var(--red-500)' : c.sop < 35 ? 'var(--orange-500)' : 'var(--text-dark)');
  setText('ts-tbat1', `${STATE.battTemp.toFixed(1)} °C`);
  setText('ts-tbat2', `${(STATE.battTemp + (Math.random()-0.5)*0.8).toFixed(1)} °C`);
  setText('ts-soh',  `${STATE.soh} %`);
  setText('ts-arc',  c.arcPct < 20 ? 'LOW' : c.arcPct < 50 ? 'MODERATE' : 'HIGH');
  setTextColor('ts-arc', c.arcPct > 50 ? 'var(--red-500)' : c.arcPct > 25 ? 'var(--orange-500)' : 'var(--green-500)');

  // Network arrows animation
  if (STATE.networkOnline) {
    for (let i = 1; i <= 6; i++) {
      const a = id(`ta-arr${i}`);
      if (a) a.className = 'ta-arrow active';
    }
  } else {
    for (let i = 4; i <= 6; i++) {
      const a = id(`ta-arr${i}`);
      if (a) a.className = 'ta-arrow';
    }
  }

  // Clock
  setText('h-sync', new Date().toTimeString().slice(0, 8));
  setText('sf-buffer', STATE.pendingRecords);
}

/* ═══════════════════════════════════════════════════════
   FLEET
   ═══════════════════════════════════════════════════════ */
const FLEET_ASSETS = [
  { id:'HVJ-A001', site:'Daulat Beg Oldi', alt:5200, temp:-15, soh:78, power:12, state:'PROTECT' },
  { id:'HVJ-A002', site:'Siachen Base',    alt:4800, temp:-8,  soh:85, power:10, state:'DERATED' },
  { id:'HVJ-A003', site:'Rezang La',       alt:4600, temp:5,   soh:92, power:14, state:'DERATED' },
  { id:'HVJ-A004', site:'Leh Control',     alt:3500, temp:12,  soh:95, power:18, state:'NOMINAL' },
  { id:'HVJ-A005', site:'Pangong Post',    alt:4300, temp:2,   soh:88, power:11, state:'NOMINAL' },
  { id:'HVJ-A006', site:'Karakoram Pass',  alt:5300, temp:-20, soh:72, power:8,  state:'NOMINAL' },
];

let selectedAsset = null;

function initFleet() {
  renderAssetList();
  renderMapAssets();
  updateFleetSummary();
  buildMaintSchedule();
}

function updateFleetSummary() {
  const counts = { NOMINAL:0, DERATED:0, PROTECT:0, LOCKOUT:0 };
  FLEET_ASSETS.forEach(a => counts[a.state]++);
  setText('fs-nominal', counts.NOMINAL);
  setText('fs-derated', counts.DERATED);
  setText('fs-protect', counts.PROTECT);
  setText('fs-lockout', counts.LOCKOUT);
}

function renderAssetList() {
  const el = id('asset-list');
  if (!el) return;
  el.innerHTML = FLEET_ASSETS.map((a,i) => {
    const P = PHY.altToP(a.alt);
    const rho = PHY.rho(P, a.temp);
    const hot = PHY.hotspot(a.power, 3.0, a.temp, rho, 'forced');
    return `<div class="asset-row" onclick="selectAsset(${i})">
      <span class="ar-name">${a.id}</span>
      <span class="ar-alt mono">${a.alt.toLocaleString()} m</span>
      <span class="ar-temp mono">${a.temp}°C</span>
      <span class="ar-hot">${hot.toFixed(0)}°C</span>
      <span class="ar-site">${a.site}</span>
      <span class="guard-state-badge" data-state="${a.state}">${a.state}</span>
    </div>`;
  }).join('');
}

function selectAsset(i) {
  selectedAsset = i;
  document.querySelectorAll('.asset-row').forEach((r, ri) => r.classList.toggle('selected', ri === i));
  const a = FLEET_ASSETS[i];
  const P = PHY.altToP(a.alt);
  const Pkpa = P / 1000;
  const rho = PHY.rho(P, a.temp);
  const hot = PHY.hotspot(a.power, 3.0, a.temp, rho, 'forced');
  const margin = 85 - hot;
  const cap = PHY.batCap(5000, a.temp, a.soh);
  const sop = (cap / 4500 * 100).toFixed(0);
  const damage = Math.max(5, (100 - a.soh) * 0.8 + (6000 - a.alt) / 100).toFixed(0);
  const cycles = PHY.coffinManson(50);
  const rul = (cycles / (2 * 365)).toFixed(1);

  const ph = id('asset-detail-placeholder');
  const ct = id('asset-detail-content');
  if (ph) ph.classList.add('hidden');
  if (ct) ct.classList.remove('hidden');

  setText('ad-name', a.id);
  const stEl = id('ad-state');
  if (stEl) { stEl.textContent = a.state; stEl.setAttribute('data-state', a.state); }
  setText('ad-alt',    `${a.alt.toLocaleString()} m`);
  setText('ad-press',  `${Pkpa.toFixed(1)} kPa`);
  setText('ad-amb',    `${a.temp} °C`);
  setText('ad-hot',    `${hot.toFixed(1)} °C`);
  setText('ad-margin', `${margin.toFixed(1)} °C`);
  setTextColor('ad-margin', margin < 5 ? 'var(--red-500)' : margin < 15 ? 'var(--orange-500)' : 'var(--green-500)');
  setText('ad-soh', `${a.soh}%`);
  setText('ad-sop', `${sop}%`);
  setText('ad-damage', `${damage}%`);
  setText('ad-rul', `${rul} years`);
  setText('ad-ts', new Date().toTimeString().slice(0,8) + ' LOCAL');

  const rec = id('ad-recommendation');
  if (rec) {
    rec.textContent = a.state === 'PROTECT' ? `⚠ URGENT: Pre-heat battery to +5°C, reduce load 30%. Schedule inspection.` :
                      a.state === 'DERATED'  ? `Advisory: Fan running at 100%. Monitor hourly. Plan maintenance.` :
                      `✓ Nominal. Next scheduled check in 30 days.`;
    rec.style.background = a.state === 'PROTECT' ? 'var(--red-50)' : a.state === 'DERATED' ? 'var(--orange-50)' : 'var(--green-50)';
    rec.style.borderColor = a.state === 'PROTECT' ? 'var(--red-100)' : a.state === 'DERATED' ? 'var(--orange-100)' : 'var(--green-100)';
    rec.style.color = a.state === 'PROTECT' ? 'var(--red-700)' : a.state === 'DERATED' ? 'var(--orange-700)' : 'var(--green-700)';
  }
}

function renderMapAssets() {
  const svg = id('fleet-assets-layer');
  if (!svg) return;
  const positions = [[120,90],[90,130],[160,150],[300,200],[220,170],[80,80]];
  svg.innerHTML = FLEET_ASSETS.map((a,i) => {
    const [x, y] = positions[i];
    const col = a.state === 'NOMINAL' ? '#27a262' : a.state === 'DERATED' ? '#c08800' : a.state === 'PROTECT' ? '#d46a0a' : '#c0312b';
    return `<g class="map-asset" onclick="selectAsset(${i})" style="cursor:pointer">
      <circle cx="${x}" cy="${y}" r="7" fill="${col}" opacity="0.85"/>
      <circle cx="${x}" cy="${y}" r="12" fill="${col}" opacity="0.15"/>
      <text x="${x+10}" y="${y+4}" font-size="9" fill="#1a3352" font-family="IBM Plex Sans,sans-serif">${a.id.slice(-4)}</text>
    </g>`;
  }).join('');
}

/* ═══════════════════════════════════════════════════════
   MAINTENANCE
   ═══════════════════════════════════════════════════════ */
function initMaintenance() {
  buildMaintSchedule();
  buildMaintCharts();
}

function buildMaintSchedule() {
  const el = id('maint-schedule-tbody');
  if (!el) return;
  el.innerHTML = FLEET_ASSETS.map(a => {
    const damage = Math.max(5, (100 - a.soh) * 0.8 + (6000 - a.alt) / 150);
    const cycles = PHY.coffinManson(50);
    const rul = (cycles * (1 - damage/100) / (2 * 365)).toFixed(1);
    const priority = damage > 70 ? 'P1 URGENT' : damage > 40 ? 'P2' : 'P3';
    const rec = damage > 70 ? 'REPLACE SOLDER JOINTS' : damage > 40 ? 'Inspect + conformal coat' : 'Routine check';
    const pCol = damage > 70 ? 'var(--red-500)' : damage > 40 ? 'var(--orange-500)' : 'var(--green-500)';
    return `<tr>
      <td class="mono">${a.id}</td>
      <td>${a.site}</td>
      <td class="mono" style="color:${pCol}">${damage.toFixed(0)}%</td>
      <td class="mono">${rul}</td>
      <td>${rec}</td>
      <td class="mono" style="color:${pCol};font-weight:700">${priority}</td>
    </tr>`;
  }).join('');
}

function buildMaintCharts() {
  const months = Array.from({length: 25}, (_, i) => i);
  const cycles = PHY.coffinManson(50);
  const rul_m = cycles / (2 * 365) * 12;

  const health  = months.map(m => Math.max(0, 100 - (m / rul_m) * 100));
  const bandHi  = months.map(m => Math.max(0, Math.min(100, 108 - (m / (rul_m * 0.85)) * 108)));
  const bandLo  = months.map(m => Math.max(0, 92  - (m / (rul_m * 1.15)) * 92));

  mkChart('maint-rul-chart', {
    type: 'line',
    data: {
      labels: months.map(m => m % 6 === 0 ? `${m}mo` : ''),
      datasets: [
        { label: 'Fleet average health (%)', data: health, borderColor: '#2470b8', borderWidth: 2, tension: 0.4, pointRadius: 0, fill: false },
        { label: 'Upper band', data: bandHi, borderColor: 'rgba(36,112,184,0.25)', borderWidth: 1, pointRadius: 0, tension: 0.4, fill: '+1', backgroundColor: 'rgba(36,112,184,0.08)' },
        { label: 'Lower band', data: bandLo, borderColor: 'rgba(36,112,184,0.25)', borderWidth: 1, pointRadius: 0, tension: 0.4, fill: false },
        { label: 'Replace at 20%', data: months.map(()=>20), borderColor: '#c0312b', borderWidth: 1, borderDash: [5,4], pointRadius: 0 },
        { label: 'Inspect at 50%', data: months.map(()=>50), borderColor: '#d46a0a', borderWidth: 1, borderDash: [3,3], pointRadius: 0 },
      ]
    },
    options: { ...chartOpts('Month', 'Remaining Health (%)'), plugins: { legend: { labels: { color: '#3d5068', font: { size: 10 } } }, tooltip: { mode: 'index', intersect: false } } }
  });

  // Damage accumulation
  const assets = FLEET_ASSETS.map(a => a.id.slice(-4));
  const damages = FLEET_ASSETS.map(a => Math.min(100, Math.max(5, (100 - a.soh) * 0.8 + (6000 - a.alt) / 150)));
  mkChart('maint-damage-chart', {
    type: 'bar',
    data: {
      labels: assets,
      datasets: [{
        label: "Miner's Rule damage fraction (%)",
        data: damages,
        backgroundColor: damages.map(d => d > 70 ? 'rgba(192,49,43,0.7)' : d > 40 ? 'rgba(212,106,10,0.7)' : 'rgba(36,112,184,0.7)'),
        borderWidth: 0,
      }]
    },
    options: {
      ...chartOpts('Asset', "Damage (%)"),
      plugins: { legend: { display: false } }
    }
  });
}

/* ═══════════════════════════════════════════════════════
   REPORTS
   ═══════════════════════════════════════════════════════ */
function initReports() { updateReportPreview(); }

function updateReportPreview() {
  setText('rep-alt-v',  (+id('rep-alt').value).toLocaleString());
  setText('rep-temp-v', id('rep-temp').value);
  setText('rep-power-v',id('rep-power').value);
}

function generateReport() {
  const assetId = id('rep-asset-id').value;
  const comp    = id('rep-comp').value;
  const alt     = +id('rep-alt').value;
  const temp    = +id('rep-temp').value;
  const power   = +id('rep-power').value;
  const P_pa    = PHY.altToP(alt);
  const Pkpa    = P_pa / 1000;
  const rho     = PHY.rho(P_pa, temp);
  const rho0    = PHY.rho0();
  const factor  = Math.pow(rho0 / rho, 0.8);
  const theta   = 5.0;
  const thetaAlt= theta * factor;
  const Tj      = temp + power * thetaAlt;
  const penalty = ((factor - 1) * 100).toFixed(0);
  const risk    = Tj > 85 ? 'PROTECT' : Tj > 68 ? 'DERATED' : 'NOMINAL';
  const ts      = new Date().toLocaleString();
  setText('rep-timestamp', ts);

  const doc = id('report-doc');
  if (!doc) return;
  doc.innerHTML = `
    <div class="report-watermark">SIMULATION — NOT A VALIDATED MEASUREMENT</div>
    <div class="rep-doc-section">
      <div class="rep-doc-h2">ASSET IDENTIFICATION</div>
      <div class="rep-doc-row"><span class="rep-doc-label">Asset ID</span><span class="rep-doc-val">${assetId}</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Component class</span><span class="rep-doc-val">${comp.toUpperCase()}</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Generated</span><span class="rep-doc-val">${ts}</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Model</span><span class="rep-doc-val">HIMVAJRA FORGE v1.0 — SIMULATION</span></div>
    </div>
    <div class="rep-doc-section">
      <div class="rep-doc-h2">ENVIRONMENT</div>
      <div class="rep-doc-row"><span class="rep-doc-label">Deployment altitude</span><span class="rep-doc-val">${alt.toLocaleString()} m</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Ambient pressure</span><span class="rep-doc-val">${Pkpa.toFixed(1)} kPa (${(Pkpa/101.3*100).toFixed(0)}% of SL)</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Air density ratio</span><span class="rep-doc-val">${(rho/rho0).toFixed(3)} ρ₀</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Ambient temperature</span><span class="rep-doc-val">${temp} °C</span></div>
    </div>
    <div class="rep-doc-section">
      <div class="rep-doc-h2">THERMAL ANALYSIS — CALCULATED</div>
      <div class="rep-doc-row"><span class="rep-doc-label">Power dissipation</span><span class="rep-doc-val">${power} W</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Thermal resistance (sea level)</span><span class="rep-doc-val">${theta.toFixed(1)} °C/W</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Thermal resistance (derated)</span><span class="rep-doc-val orange">${thetaAlt.toFixed(2)} °C/W (penalty: +${penalty}%)</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Predicted T_junction</span><span class="rep-doc-val orange">${Tj.toFixed(1)} °C ± 3°C</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Thermal margin (to 85°C limit)</span><span class="rep-doc-val">${(85 - Tj).toFixed(1)} °C</span></div>
    </div>
    <div class="rep-doc-section">
      <div class="rep-doc-h2">RISK ASSESSMENT</div>
      <div class="rep-doc-row"><span class="rep-doc-label">GUARD state</span><span class="rep-doc-val" style="color:${risk==='PROTECT'?'var(--orange-500)':risk==='DERATED'?'var(--yellow-600)':'var(--green-500)'}">${risk}</span></div>
      <div class="rep-doc-row"><span class="rep-doc-label">Arc risk (2mm gap)</span><span class="rep-doc-val">${PHY.paschen(Pkpa,2) < PHY.paschen(101.3,2)*0.7 ? 'ELEVATED' : 'ACCEPTABLE'}</span></div>
    </div>
    ${Tj > 75 ? `<div class="rep-doc-warning">⚠ T_junction near or above safe operating limit. Apply conformal coat, increase fan speed, reduce load or improve θ_JA before deployment at this altitude.</div>` : `<div class="rep-doc-ok">✓ Thermal margins acceptable at this altitude and load. Continue monitoring via GUARD telemetry.</div>`}
    <div class="rep-doc-footer">HIMVAJRA FORGE — Physics-based simulation only. No hardware measurements performed. All values calculated from ISA standard atmosphere and Nusselt correlations. Validate against measured CHAMBER data before operational deployment. SIH 2026 · DRDO #26049</div>`;

  logEvent('info', `Report generated: ${assetId} at ${alt.toLocaleString()}m`, 'report');
}

function printReport() { window.print(); }

/* ═══════════════════════════════════════════════════════
   EVENT LOG + AUDIT
   ═══════════════════════════════════════════════════════ */
function logEvent(state, msg, type) {
  const ts = new Date().toTimeString().slice(0, 8);
  const entry = { ts, state, msg, type, hash: '#' + Math.random().toString(16).slice(2, 8) };
  STATE.events.unshift(entry);
  if (STATE.events.length > 50) STATE.events.pop();
  renderEventLog();
}

function renderEventLog() {
  const el = id('ov-event-log');
  if (!el) return;
  const typeClass = { guard:'log-' + STATE.guardState.toLowerCase(), fault:'log-fault', recovery:'log-recovery', report:'log-info', info:'log-info' };
  el.innerHTML = STATE.events.slice(0, 20).map(e => `
    <div class="log-entry ${typeClass[e.type] || 'log-info'}">
      <span class="log-ts">${e.ts}</span>
      <span class="log-state" style="color:${e.state==='LOCKOUT'?'var(--red-500)':e.state==='PROTECT'?'var(--orange-500)':e.state==='DERATED'?'var(--yellow-600)':e.state==='NOMINAL'?'var(--green-500)':'var(--text-light)'}">${e.state}</span>
      <span class="log-level">${e.type.toUpperCase()}</span>
      <span class="log-msg">${e.msg}</span>
      <span class="log-hash">${e.hash}</span>
    </div>`).join('');
}

function addAudit(msg) {
  const ts = new Date().toTimeString().slice(0, 8);
  const hash = '#' + Math.random().toString(16).slice(2, 8);
  STATE.auditLog.unshift({ ts, msg, hash });
  if (STATE.auditLog.length > 30) STATE.auditLog.pop();
  renderAuditLog();
}

function renderAuditLog() {
  const el = id('guard-audit-log');
  if (!el) return;
  el.innerHTML = STATE.auditLog.map(e =>
    `<div class="audit-entry"><span class="ae-ts">${e.ts}</span><span class="ae-msg">${e.msg}</span><span class="ae-hash">${e.hash}</span></div>`
  ).join('');
}

/* ═══════════════════════════════════════════════════════
   CONNECTIVITY
   ═══════════════════════════════════════════════════════ */
function toggleNetwork() {
  STATE.networkOnline = !STATE.networkOnline;
  if (!STATE.networkOnline) { STATE.pendingRecords += Math.floor(Math.random() * 10) + 5; }
  else if (STATE.pendingRecords > 0) {
    logEvent('info', `NETWORK RESTORED — ${STATE.pendingRecords} records synced`, 'recovery');
    STATE.pendingRecords = 0;
  }
  updateConnectivity();
}

function updateConnectivity() {
  const dot = id('sf-network-dot');
  const lbl = id('sf-network-label');
  const btn = id('network-toggle-btn');
  const banner = id('offline-banner');
  const pending = id('pending-count');
  const telemDot = id('telem-live-dot');

  if (dot) { dot.className = 'dot ' + (STATE.networkOnline ? 'dot-green' : 'dot-orange'); }
  if (lbl) lbl.textContent = STATE.networkOnline ? 'NETWORK' : 'OFFLINE';
  if (btn) btn.textContent = STATE.networkOnline ? 'DISABLE NETWORK' : 'RESTORE NETWORK';
  if (banner) banner.style.display = STATE.networkOnline ? 'none' : 'flex';
  if (pending) pending.textContent = STATE.pendingRecords;
  if (telemDot) telemDot.className = 'dot ' + (STATE.networkOnline ? 'dot-green' : 'dot-orange');
  if (!STATE.networkOnline && STATE.pendingRecords > 0) { setState.pendingRecords++; }
}

/* ═══════════════════════════════════════════════════════
   DEMO MODE — 8-STEP AUTOMATED SEQUENCE
   ═══════════════════════════════════════════════════════ */
const DEMO_STEPS = [
  { name: 'RESET',           action() { navigate('simulation'); injectFault('recovery'); STATE.alt=0; STATE.temp=25; STATE.power=5; onSimChange(); } },
  { name: 'SET ALTITUDE',    action() { STATE.alt=5500; onSimChange(); logEvent('info','Demo: Altitude set to 5,500m','info'); } },
  { name: 'PRESSURE CALC',   action() { logEvent('NOMINAL','Pressure: 50.5 kPa (ISA model)','info'); } },
  { name: 'LOAD INCREASE',   action() { STATE.power=15; onSimChange(); logEvent('info','Power: 15W applied','info'); } },
  { name: 'THERMAL PENALTY', action() { logEvent('DERATED','θ_sa +74% — hotspot rising','guard'); } },
  { name: 'FORGE PREDICT',   action() { navigate('forge'); id('fg-alt').value=5500; id('fg-power').value=15; runForge(); } },
  { name: 'GUARD TRANSITION',action() { navigate('guard'); setSlider('g-tj', 72); setSlider('g-press', 51); updateGuardPage(); } },
  { name: 'PROTECT ACTION',  action() { setSlider('g-tj', 82); updateGuardPage(); logEvent('PROTECT','Fan→100%, load shed, charge inhibited','guard'); } },
];

function startDemoMode() {
  const btn = id('demo-mode-btn');
  if (STATE.demoInterval) {
    clearInterval(STATE.demoInterval);
    STATE.demoInterval = null;
    STATE.demoStep = 0;
    if (btn) { btn.textContent = '▶ DEMO MODE'; btn.classList.remove('running'); }
    return;
  }
  if (btn) { btn.textContent = '◼ STOP DEMO'; btn.classList.add('running'); }
  STATE.demoStep = 0;
  runDemoStep();
  STATE.demoInterval = setInterval(() => {
    STATE.demoStep++;
    if (STATE.demoStep >= DEMO_STEPS.length) {
      clearInterval(STATE.demoInterval);
      STATE.demoInterval = null;
      STATE.demoStep = 0;
      if (btn) { btn.textContent = '▶ DEMO MODE'; btn.classList.remove('running'); }
      return;
    }
    runDemoStep();
  }, 3000);
}

function runDemoStep() {
  const step = DEMO_STEPS[STATE.demoStep];
  if (step) {
    step.action();
    setText('h-mode', `DEMO [${STATE.demoStep+1}/${DEMO_STEPS.length}] ${step.name}`);
  }
}

/* ═══════════════════════════════════════════════════════
   DRONE FLIGHT LAB (LAC 60 min -> 20 min breakdown & recovery)
   ═══════════════════════════════════════════════════════ */
let droneRetrofitActive = true;

function initDroneLab() {
  updateDroneRetrofitUI();
  updateDroneLab();
}

function setDroneBenchmark(key) {
  if (key === 'sea_level') {
    setSlider('dr-alt', 0);
    setSlider('dr-temp', 20);
    setSlider('dr-payload', 1.0);
    droneRetrofitActive = false;
  } else if (key === 'dbo_stock') {
    setSlider('dr-alt', 5100);
    setSlider('dr-temp', -25);
    setSlider('dr-payload', 2.0);
    droneRetrofitActive = false;
  } else if (key === 'dbo_himvajra') {
    setSlider('dr-alt', 5100);
    setSlider('dr-temp', -25);
    setSlider('dr-payload', 2.0);
    droneRetrofitActive = true;
  }
  updateDroneRetrofitUI();
  updateDroneLab();
}

function toggleDroneRetrofit() {
  droneRetrofitActive = !droneRetrofitActive;
  updateDroneRetrofitUI();
  updateDroneLab();
}

function updateDroneRetrofitUI() {
  const btn = id('dr-toggle-btn');
  const badge = id('drone-retrofit-badge');
  if (btn) {
    btn.textContent = droneRetrofitActive ? 'ACTIVE' : 'DISABLED';
    btn.style.background = droneRetrofitActive ? 'var(--orange)' : 'var(--navy-600)';
  }
  if (badge) {
    badge.textContent = droneRetrofitActive ? 'RETROFIT: ACTIVE' : 'RETROFIT: DISABLED';
    badge.className = 'data-badge ' + (droneRetrofitActive ? 'orange-badge' : '');
  }
}

async function updateDroneLab() {
  const alt = id('dr-alt') ? +id('dr-alt').value : 5000;
  const temp = id('dr-temp') ? +id('dr-temp').value : -20;
  const payload = id('dr-payload') ? +id('dr-payload').value : 2.0;

  setText('dr-alt-v', alt.toLocaleString());
  setText('dr-temp-v', temp);
  setText('dr-payload-v', payload.toFixed(1));

  const P = PHY.altToP(alt);
  const rho = PHY.rho(P, temp);
  const rho0 = PHY.rho0();
  const rhoR = rho / rho0;
  const liftDeficit = Math.round((rhoR - 1) * 100);

  setText('dr-rho-v', `${rho.toFixed(2)} kg/m³`);
  setText('dr-lift-deficit', `${liftDeficit}%`);

  try {
    const res = await fetch('http://127.0.0.1:8000/api/predict/drone_loss_budget', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        altitude_m: alt,
        temp_c: temp,
        payload_kg: payload,
        himvajra_retrofitted: droneRetrofitActive
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderDroneLabResults(data);
  } catch (err) {
    renderDroneLabFallback(alt, temp, payload, rhoR);
  }
}

function renderDroneLabResults(data) {
  setText('dr-final-endurance', `${data.final_endurance_min} min`);
  setText('dr-stock-comparison', `Stock drone: ${data.stock_drone_endurance_min} min (+${data.endurance_restoration_pct}% restored)`);
  setText('dr-loss-aero', `-${data.loss_breakdown.aerodynamic_lift_deficit_min} min`);
  setText('dr-loss-cold', `-${data.loss_breakdown.electrochemical_freeze_loss_min} min`);
  setText('dr-loss-sag', `-${data.loss_breakdown.premature_voltage_cutoff_sag_min} min`);

  setText('dr-rec-aero', `Fixed blades: +${data.recovered_minutes.high_camber_cold_blades_min} min`);
  setText('dr-rec-cold', `PTC pre-heat: +${data.recovered_minutes.aerogel_and_ptc_heater_min} min`);
  setText('dr-rec-sag', `SoP cutoff: +${data.recovered_minutes.state_of_power_cutoff_min} min`);
}

function renderDroneLabFallback(alt, temp, payload, rhoR) {
  const t_nominal = 60.0;
  const aeroPenalty = (1.0 / Math.sqrt(Math.max(0.3, rhoR)) - 1.0) * 0.48;
  const t_after_aero = t_nominal * (1.0 - aeroPenalty);
  const loss_aero = Math.max(0, t_nominal - t_after_aero);

  const coldPenalty = Math.max(0, (20 - temp) * 0.95);
  const t_after_cold = t_after_aero * (1.0 - coldPenalty * 0.012);
  const loss_cold = Math.max(0, t_after_aero - t_after_cold);

  const loss_sag = t_after_cold * 0.24;
  const stock = Math.max(8.0, t_after_cold - loss_sag - payload * 2.5);

  const rec_aero = droneRetrofitActive ? loss_aero * 0.35 : 0;
  const rec_cold = droneRetrofitActive ? loss_cold * 0.72 : 0;
  const rec_sag = droneRetrofitActive ? loss_sag * 0.88 : 0;
  const total_rec = rec_aero + rec_cold + rec_sag;
  const final_t = stock + total_rec;
  const restore_pct = ((total_rec / stock) * 100).toFixed(0);

  setText('dr-final-endurance', `${final_t.toFixed(1)} min`);
  setText('dr-stock-comparison', `Stock drone: ${stock.toFixed(1)} min (+${restore_pct}% restored)`);
  setText('dr-loss-aero', `-${loss_aero.toFixed(1)} min`);
  setText('dr-loss-cold', `-${loss_cold.toFixed(1)} min`);
  setText('dr-loss-sag', `-${loss_sag.toFixed(1)} min`);
  setText('dr-rec-aero', `Fixed blades: +${rec_aero.toFixed(1)} min`);
  setText('dr-rec-cold', `PTC pre-heat: +${rec_cold.toFixed(1)} min`);
  setText('dr-rec-sag', `SoP cutoff: +${rec_sag.toFixed(1)} min`);
}

/* ═══════════════════════════════════════════════════════
   RADIATION & COMMS LAB (Effects 5 & 6)
   ═══════════════════════════════════════════════════════ */
let antennaHeaterActive = true;

function initRadComms() {
  updateRadComms();
}

function toggleAntennaHeater() {
  antennaHeaterActive = !antennaHeaterActive;
  const btn = id('rc-heater-btn');
  if (btn) {
    btn.textContent = antennaHeaterActive ? 'ACTIVE' : 'OFF';
    btn.style.background = antennaHeaterActive ? 'var(--orange)' : 'var(--navy-600)';
  }
  updateRadComms();
}

async function updateRadComms() {
  const alt = id('rc-alt') ? +id('rc-alt').value : 5000;
  const ice = id('rc-ice') ? +id('rc-ice').value : 3.5;

  setText('rc-alt-v', alt.toLocaleString());
  setText('rc-ice-v', ice.toFixed(1));

  // Query Radiation API
  try {
    const res = await fetch('http://127.0.0.1:8000/api/predict/radiation_seu', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        altitude_m: alt,
        memory_size_gb: 16.0,
        edac_enabled: true
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    setText('rc-flux', `${data.cosmic_neutron_flux_ratio} ×`);
    setText('rc-uv', `${data.uv_index_predicted}`);
    setText('rc-fits', `${Math.round(data.soft_error_rate_raw_fits).toLocaleString()}`);
    setText('rc-mtbf-raw', `Unmitigated MTBF: ${data.mtbf_unmitigated_days} days`);
    setText('rc-mtbf-edac', `${Math.round(data.mitigated_mtbf_years).toLocaleString()}`);
  } catch (err) {
    const P = PHY.altToP(alt) / 1000;
    const depth = 1033.0 * (P / 101.325);
    const flux = (Math.exp((1033.0 - depth) / 138.0) * 0.18 + 0.82).toFixed(2);
    const uv = Math.min(15.0, (3.0 + (alt / 1000) * 2.1)).toFixed(1);
    const fits = Math.round(16 * 18.5 * flux);
    const mtbfDays = (1e9 / fits / 24).toFixed(1);
    setText('rc-flux', `${flux} ×`);
    setText('rc-uv', uv);
    setText('rc-fits', fits.toLocaleString());
    setText('rc-mtbf-raw', `Unmitigated MTBF: ${mtbfDays} days`);
    setText('rc-mtbf-edac', '47,600');
  }

  // Query Antenna RF API
  try {
    const res = await fetch('http://127.0.0.1:8000/api/predict/antenna_rf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ice_accretion_mm: ice,
        ptc_deicer_active: antennaHeaterActive
      })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    setText('rc-vswr', `${data.vswr} : 1`);
    setText('rc-vswr-status', data.status);
    const vswrEl = id('rc-vswr-status');
    if (vswrEl) vswrEl.style.color = data.status === 'CRITICAL_ICING' ? 'var(--red)' : (data.status === 'DEGRADED' ? 'var(--orange)' : 'var(--green)');
    setText('rc-refl', `${data.reflected_power_pct}`);
    setText('rc-margin', `${data.link_margin_db > 0 ? '+' : ''}${data.link_margin_db}`);
    setText('rc-mod', data.adaptive_modulation);

    // Calculate raw icy VSWR for comparison
    const rawVswr = (1.15 + ice * 0.85).toFixed(2);
    setText('rc-vswr-raw', `Raw icy VSWR: ${rawVswr}:1`);
  } catch (err) {
    const effIce = antennaHeaterActive ? 0.2 : ice;
    const vswr = (1.15 + effIce * 0.85).toFixed(2);
    const refl = (((vswr - 1) / (+vswr + 1)) ** 2 * 100).toFixed(1);
    const margin = (18 - effIce * 3.4).toFixed(1);
    const mod = margin > 12 ? '64-QAM' : (margin > 6 ? '16-QAM' : (margin > 0 ? 'QPSK' : 'DSSS'));
    setText('rc-vswr', `${vswr} : 1`);
    setText('rc-vswr-status', vswr > 3.0 ? 'CRITICAL_ICING' : (vswr > 1.8 ? 'DEGRADED' : 'SAFE MATCHING'));
    setText('rc-refl', refl);
    setText('rc-margin', `${margin > 0 ? '+' : ''}${margin}`);
    setText('rc-mod', mod);
    const rawVswr = (1.15 + ice * 0.85).toFixed(2);
    setText('rc-vswr-raw', `Raw icy VSWR: ${rawVswr}:1`);
  }
}

/* ═══════════════════════════════════════════════════════
   DRDO RETROFIT MATRIX
   ═══════════════════════════════════════════════════════ */
function initModifications() {
  // Static interactive reference catalog already fully mounted in markup
}

/* ═══════════════════════════════════════════════════════
   CHART HELPERS
   ═══════════════════════════════════════════════════════ */
function mkChart(canvasId, config) {
  if (CHARTS[canvasId]) { CHARTS[canvasId].destroy(); }
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  CHARTS[canvasId] = new Chart(ctx, config);
  return CHARTS[canvasId];
}

function chartOpts(xLabel, yLabel) {
  return {
    responsive: true,
    animation: { duration: 300 },
    plugins: {
      legend: { labels: { color: '#3d5068', font: { family: 'IBM Plex Sans', size: 10 } } },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      x: {
        ticks: { color: '#6b8299', font: { size: 9 } },
        grid:  { color: 'rgba(180,200,220,0.3)' },
        title: { display: !!xLabel, text: xLabel, color: '#6b8299', font: { size: 9 } }
      },
      y: {
        ticks: { color: '#6b8299', font: { size: 9 } },
        grid:  { color: 'rgba(180,200,220,0.3)' },
        title: { display: !!yLabel, text: yLabel, color: '#6b8299', font: { size: 9 } }
      }
    }
  };
}

/* ═══════════════════════════════════════════════════════
   DOM HELPERS
   ═══════════════════════════════════════════════════════ */
function id(i)                 { return document.getElementById(i); }
function setText(i, v)         { const e = id(i); if (e) e.textContent = v; }
function setTextColor(i, c)    { const e = id(i); if (e) e.style.color = c; }
function setTextStyle(i, v, s) { const e = id(i); if (e) { e.textContent = v; e.style.cssText = s; } }

/* Live clock */
function liveClock() { setText('h-sync', new Date().toTimeString().slice(0, 8)); }

/* ═══════════════════════════════════════════════════════
   INIT
   ═══════════════════════════════════════════════════════ */
window.addEventListener('DOMContentLoaded', () => {
  setInterval(liveClock, 1000);
  setInterval(checkMlServerStatus, 5000);
  checkMlServerStatus();
  updateConnectivity();
  logEvent('NOMINAL', 'HIMVAJRA platform initialised — simulation mode', 'info');
  logEvent('NOMINAL', 'All physics models active — hardware offline', 'info');
  addAudit('BOOT — HIMVAJRA v1.0 — SIH 2026');
  navigate('overview');

  // Sync sim sliders to STATE
  ['sim-alt','sim-temp','sim-power','sim-theta','sim-batt-temp','sim-soh'].forEach(sid => {
    const el = id(sid);
    if (el) el.addEventListener('input', onSimChange);
  });
});
