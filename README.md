# HIMVAJRA-HRM — Virtual High-Altitude Hardware Reliability Laboratory
### Digital Twin & Virtual Validation Environment for High-Altitude Electronics Hardening
**DRDO Smart India Hackathon 2026 · Problem Statement #26049 · Ladakh / Siachen Sector (3,000–6,000 m AMSL)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Physics: ISA_Atmosphere](https://img.shields.io/badge/Physics-First--Principles-orange.svg)](app.js)
[![Safety: Deterministic_FSM](https://img.shields.io/badge/Safety-Zero--AI_FSM-green.svg)](app.js)
[![Hardware: Hardened_Retrofit_Module](https://img.shields.io/badge/Hardware-HIMVAJRA--HRM-red.svg)](index.html)

---

## 1. Engineering Mission

In the high-altitude Himalayan operational theatre (Ladakh, Siachen, Leh: 3,000 to 6,000 m AMSL), commercial-off-the-shelf (COTS) and standard military avionics suffer catastrophic reliability degradation:
1. **Hypbaric Convective Starvation**: Atmospheric pressure drops by ~50% ($101.3 \to 50.5\,\text{kPa}$) and air density shrinks to $0.709\,\text{kg/m}^3$. Convective cooling capacity plummets by $45\%$, causing unmitigated thermal throttling and silicon junction burnout ($T_j > 85^\circ\text{C}$).
2. **Electrochemical Freezing & Impedance Spike**: At $-25^\circ\text{C}$ to $-40^\circ\text{C}$, LiPo/Li-ion electrolyte viscosity freezes, triggering an exponential Arrhenius internal resistance surge ($12\,\text{m}\Omega \to 58\,\text{m}\Omega$). High current draw causes severe terminal voltage collapse ($V_{\text{term}} < 12.0\,\text{V}$), tripping premature Low-Voltage Cutoff (LVC) in under 2 minutes.
3. **Paschen Dielectric Breakdown**: Reduced atmospheric pressure widens the electron mean free path. Breakdown voltage across PCB traces drops from $>3\,\text{kV/mm}$ toward the Paschen minimum ($327\,\text{V}$), triggering corona discharge, dielectric breakdown, and catastrophic PCB arcing.
4. **Enclosure Pressure Differential ($\Delta P$)**: Sealed enclosures experience up to $50.8\,\text{kPa}$ outwards differential pressure, leading to seal blowout, structural lid bulging, and subsequent inward moisture ingress upon descent.
5. **Condensation / Psychrometric Trap**: Rapid descent from cold cruise altitude into humid base camps drives component temperatures below ambient dew point, causing condensation short circuits on unpotted electronics.

**HIMVAJRA-HRM (Hardened Retrofit Module)** is the proposed physical hardware countermeasure system engineered to solve these problems through deterministic physical interventions. This repository hosts the **Virtual High-Altitude Hardware Reliability Laboratory** — a physics-based digital twin and virtual test environment that models, simulates, and proves the efficacy of the physical HRM before hardware fabrication.

---

## 2. The 8 Hardware Countermeasures

| Countermeasure | Component / Material | Physical Mechanism | Engineering Impact |
|---|---|---|---|
| **A. Vapor Chamber** | Sintered copper-water planar chamber (0.45 °C/W) | High-flux latent heat phase change spreading | Spreads localized silicon hotspots ($15\,\text{W}$) over $180\,\text{cm}^2$ chassis to enable radiative deep-sky heat rejection. |
| **B. Aerogel Jacket** | Aspen Pyrogel aerogel insulation ($0.015\,\text{W/m}\cdot\text{K}$) | Ultra-low thermal conductivity vacuum barrier | Reduces passive battery thermal loss by $68\%$, preventing electrolyte freezing. |
| **C. Active Pre-Heating** | Kapton polyimide etched-foil heating elements | Sensible Joulean core heating ($12\,\text{W}$) with closed-loop PWM | Preheats battery core from $-25^\circ\text{C}$ to $+12^\circ\text{C}$ prior to launch, restoring full $21.4\,\text{min}$ runtime. |
| **D. Pressure Vent** | Gore Automotive e-PTFE vent membrane | Gas-permeable oleophobic dual-direction breathability | Equalizes enclosure differential pressure from $50.8\,\text{kPa}$ down to $<0.15\,\text{kPa}$, eliminating lid bulging. |
| **E. Conformal Coating** | Dow Corning 1-2577 silicone elastomeric coating | Solid-state dielectric barrier ($>42\,\text{kV/mm}$) | Completely suppresses hypbaric partial discharge and Paschen arcing up to $42\,\text{kV}$. |
| **F. Isolation Slots** | CNC-milled air gaps in PCB between high-voltage rails | Geometric creepage distance extension ($1.2 \to >5.0\,\text{mm}$) | Prevents high-voltage tracking and surface flashover across board layers. |
| **G. Kinematic Mounts** | Spring-loaded copper-beryllium standoffs | Mechanical compliance across CTE mismatch boundaries | Dampens Norris-Landzberg solder joint shear strain, extending fatigue life from $420$ to $>2,800$ thermal cycles. |
| **H. GUARD Controller** | STM32G431 deterministic MCU with hardware interlocks | Autonomous 4-state finite state machine (Zero AI in safety loop) | High-speed ($10\,\text{Hz}$) deterministic safety response: fan modulation, load shedding, charge inhibit, and fault latching. |

---

## 3. First-Principles Mathematical Models

All calculations in `app.js` operate on transparent first-principles physics:

- **International Standard Atmosphere (ISA) Pressure**:
  $$P(h) = P_0 \cdot \left(1 - \frac{L \cdot h}{T_0}\right)^{\frac{g \cdot M}{R \cdot L}}$$
- **Air Density ($\rho$)**:
  $$\rho = \frac{P}{R_{\text{spec}} \cdot T_K} \quad \text{where } R_{\text{spec}} = 287.05\,\text{J/(kg}\cdot\text{K)}$$
- **Convection Derating**:
  $$h(h_{\text{alt}}) = h_0 \cdot \left(\frac{\rho}{\rho_0}\right)^{0.8}$$
- **Thermal RC Model with Radiative Heat Dump**:
  $$T_j = T_{\text{amb}} + P \cdot \left[\theta_{\text{vc}} + \left(\frac{1}{\theta_{\text{conv}}} + \frac{1}{\theta_{\text{rad}}}\right)^{-1}\right]$$
  $$q_{\text{rad}} = \epsilon \cdot \sigma \cdot A \cdot (T_{\text{chassis}}^4 - T_{\text{sky}}^4)$$
- **Thévenin Battery Model with Arrhenius Resistance**:
  $$R_{\text{int}}(T) = R_0 \cdot \exp\left[\frac{E_a}{R}\left(\frac{1}{T_K} - \frac{1}{T_{0,K}}\right)\right]$$
  $$V_{\text{term}} = V_{\text{OCV}} - I_{\text{load}} \cdot R_{\text{int}}(T)$$
- **Paschen Dielectric Breakdown**:
  $$V_B = \frac{B \cdot (P \cdot d)}{\ln[A \cdot (P \cdot d)] - \ln[\ln(1 + 1/\gamma)]}$$
- **Magnus-Tetens Dew-Point Model**:
  $$\alpha(T, \text{RH}) = \frac{17.27 \cdot T}{237.7 + T} + \ln\left(\frac{\text{RH}}{100}\right) \implies T_{\text{dew}} = \frac{237.7 \cdot \alpha}{17.27 - \alpha}$$
- **Norris-Landzberg Solder Fatigue Life**:
  $$N_f = A \cdot (\Delta T)^{-1.9} \cdot f^{1/3} \cdot \exp\left(\frac{\Phi}{k \cdot T_{\text{max}}}\right)$$

---

## 4. The 18 Dedicated Engineering Modules

1. **01. Engineering Overview**: Mission command center, 8-KPI strip, interactive system signal flow diagram, and live GUARD state ladder.
2. **02. Virtual Chamber**: Environmental test bench with sliders for altitude ($0–6,000\,\text{m}$), temperature ($-40$ to $+30^\circ\text{C}$), electrical load, and mission profile scenarios.
3. **03. Failure Cascades**: 5 interactive causal chains illustrating the physical step-by-step propagation of high-altitude failure modes.
4. **04. Hardware Config**: 10 interactive hardware switches that dynamically re-parameterize the physics engine equations in real time.
5. **05. 3D Enclosure Twin**: Isometric Canvas digital twin with rotation, $0–100\%$ exploded-view slider, component isolation, and technical callouts.
6. **06. Thermal Analysis**: Detailed convective starvation curves, boundary layer analysis, and vapor chamber dissipation math.
7. **07. Battery & Energy**: Thévenin equivalent circuit analysis, Arrhenius impedance curves, and cold-start vs. preheated discharge profiles.
8. **08. Dielectric & Paschen**: High-voltage Paschen curve breakdown simulator across pressures and electrode spacings.
9. **09. Condensation & $\Delta P$**: Psychrometric dew point margin tracking and enclosure mechanical bulging analysis.
10. **10. GUARD Controller**: Deterministic 4-state finite state machine (`NOMINAL` $\to$ `DERATED` $\to$ `PROTECT` $\to$ `LOCKOUT`) with 11-fault injection test board.
11. **11. Validation Lab**: Re-creation of all 6 DRDO experimental test protocols with live stage progress (1–7) and pass/fail gate criteria.
12. **12. Baseline vs Protected**: Simultaneous split-screen comparison of unmodified COTS hardware vs. HIMVAJRA-protected hardware.
13. **13. Telemetry DAQ**: High-speed telemetry recorder with real-time strip charts, tabular ring buffer, and CSV export.
14. **14. Hardware BOM**: Full Bill of Materials categorized with specifications, Indian Rupee (INR) costs, and source document citations.
15. **15. Engineering Math**: Transparent first-principles mathematical formulas with live numerical substitutions.
16. **16. Safety & FMEA**: Failure Mode and Effects Analysis matrix with RPN scoring, single-point-of-failure analysis, and interlocks.
17. **17. Retrofit Planner**: Step-by-step modular upgrade guide for Drone Payloads, Radar Modules, and EW SDR Systems.
18. **18. Engineering Report**: Automated formal DRDO test certification report generator with print/PDF styling and scientific disclaimers.

---

## 5. Virtual Chamber Test Protocols

The virtual validation laboratory implements the 6 rigorous test suites defined in the HIMVAJRA engineering specification:
- **TEST 01: Cold Air / Hot Chip Test** — 15 W load at 5,500 m / $-25^\circ\text{C}$ (Verifies vapor chamber limits junction rise to $<50^\circ\text{C}$).
- **TEST 02: Sub-Zero Battery Extraction** — 12.5 A discharge at $-25^\circ\text{C}$ (Verifies Kapton preheating extends runtime from $1.8\,\text{min}$ to $>20\,\text{min}$).
- **TEST 03: Dielectric Arc / Paschen Test** — 400 V transient at 54 kPa (Verifies conformal coating suppresses partial discharge).
- **TEST 04: Thermal Shock & Diurnal Cycling** — $-40^\circ\text{C} \leftrightarrow +35^\circ\text{C}$ across 100 cycles (Verifies kinematic standoffs absorb shear strain).
- **TEST 05: Pressure Differential & Hermeticity** — Rapid climb to 6,000 m (Verifies Gore vent maintains $\Delta P < 1.0\,\text{kPa}$).
- **TEST 06: Condensation & Rapid Altitude Descent** — 5,500 m cold soak to 1,500 m humid base (Verifies GUARD power-hold prevents condensation restart).

---

## 6. One-Click Demonstration Features for Judges

- **`▶ RUN 5,500m TEST`**: Instantly configures the environmental chamber to the primary Ladakh test scenario ($5,500\,\text{m}$, $-25^\circ\text{C}$, $50.5\,\text{kPa}$) and updates baseline vs. protected metrics.
- **`⚡ LOAD SIH DEMO`**: Automated 10-stage simulation walkthrough that demonstrates failure propagation, countermeasure activation, fault injection, and recovery.
- **`⚖ JUDGE MODE`**: Interactive 8-step modal explaining the full engineering story from problem definition to hardware architecture, comparison, and deployment feasibility.
- **`? WHY HARDWARE?`**: Comprehensive traceability matrix connecting every environmental stress to its physical mechanism, design requirement, hardware component, sensor, and chamber validation test.

---

## 7. Scientific Honesty & Provenance

Every data point in the user interface is tagged with clear provenance badges:
- `SOURCE DOCUMENT`: Exact values and specifications from DRDO problem statements and hardware datasheets.
- `CALCULATED PHYSICS`: Derived via verified thermodynamic, electrochemical, and atmospheric equations.
- `SIMULATED TWIN`: Real-time state machine and transient thermal responses.
- `DESIGN TARGET`: Target engineering specifications for prototype fabrication.
- `NOT PHYSICALLY VALIDATED`: Transparently discloses that physical environmental chamber testing remains required once physical hardware is fabricated.

---

## 8. Quick Start (Air-Gapped / Offline Ready)

The entire application runs 100% offline with zero external cloud or API dependencies:

```bash
# Clone the repository
git clone https://github.com/harshshah2707/HimVajra.git
cd HimVajra

# Start local server (Python 3)
python -m http.server 8080
```
Open **`http://localhost:8080`** in any modern web browser.

Optional Machine Learning prognostics backend (FastAPI):
```bash
pip install -r requirements.txt
python ml_service.py
# API docs available at http://127.0.0.1:8000/docs
```

---

## 9. Repository Structure

```
HimVajra/
├── index.html                                 # 18-module Engineering Digital Twin & Virtual Lab UI
├── style.css                                  # High-contrast aerospace instrumentation CSS theme
├── app.js                                     # First-principles physics engine & GUARD state machine
├── ml_service.py                              # Optional FastAPI ML residual & prognostics microservice
├── train_forge.py                             # Synthetic dataset generator & thermal ML model trainer
├── test_forge_api.py                          # Automated API verification script
├── data/
│   ├── forge_thermal_dataset.csv              # High-altitude environmental thermal dataset
│   ├── amovfly_uav_high_altitude_dataset.csv  # AMOVFLY high-altitude UAV flight records
│   └── nasa_battery_pcoe_dataset.csv          # NASA PCoE battery aging records
├── models/                                    # Pre-trained ML & GPR uncertainty models
├── README.md                                  # Complete engineering documentation
└── requirements.txt                           # Python dependencies
```

---

## 10. License

Developed for high-altitude defense electronics reliability (DRDO SIH Problem Statement #26049). Released under the MIT License.
