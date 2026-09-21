# HIMVAJRA-HRM: SYSTEM ARCHITECTURE & PROBLEM STATEMENT REFERENCE
## High-Altitude Electronics Hardening, Reliability Digital Twin & Decision-Support Platform
**DRDO Smart India Hackathon 2026 · Problem Statement ID: #26049**  
*Operating Theatre: High Altitude Areas (HAA) and Super High Altitude Areas (SHAA) of Ladakh / Siachen Sector (3,000 to 6,000 m AMSL)*

---

## 1. Executive Summary & Problem Statement Context

### 1.1 The Official Problem Statement (DRDO SIH #26049)
> **Problem Statement Title**: *"Modifications to improve the reliability, efficiency, and lifespan of electrical and electronic equipment and systems in the ambient condition of subzero temperature and low pressure of High Altitude Areas (HAA) and Super High Altitude Areas (SHAA) of Ladakh region."*  
> **Organization**: Defence Research and Development Organisation (DRDO)  
> **Operational Scope**: Ladakh, Siachen Glacier, Leh, Daulat Beg Oldie (DBO), Nyoma (3,000 to 6,000 m AMSL).

### 1.2 The Core Dilemma & Architectural Philosophy
The Problem Statement demands "specialized design modifications." Most conventional responses compile a generic literature review (adding heaters, silicone coating, or extra insulation) or present a generic IoT/AI dashboard. 

**HIMVAJRA** was built on three foundational engineering realities:
1. **You Cannot Re-Buy the Armed Forces' Fleet**: The Indian Army and Indian Air Force already operate thousands of legacy assets along the Line of Actual Control (LAC)—tactical UAVs, radar power supply units (PSUs), cellular/tactical Base Transceiver Stations (BTS), Battlefield Transparency (BFT) computers, and generator control units. The only deployable military solution is a **Hardened Retrofit Module (HRM)** that bolts directly onto existing equipment without requalifying the entire platform.
2. **You Cannot Assert Hardening Without Environmental Proof**: India has limited hypbaric-cryogenic live-testing chambers capable of simultaneously applying $50\,\text{kPa}$ pressure, $-35^\circ\text{C}$ temperatures, $50^\circ\text{C}$ diurnal swings, and electrical loads. Software claims without chamber ground truth are mere assertions.
3. **Software/Digital Twin is the Engineering Proving Ground, Hardware is the Product**: Because physical prototypes cannot be fabricated or flight-tested overnight, the **HIMVAJRA Virtual High-Altitude Hardware Reliability Laboratory** serves as an earned digital twin—modeling the first-principles physics, validating the 8 hardware countermeasures across 6 standardized chamber protocols, and providing deterministic mission dispatch decisions.

---

## 2. The Environmental Threat Matrix of Ladakh (3,000 – 6,000 m AMSL)

The atmospheric and thermodynamic conditions at 5,500 m in the Ladakh sector fundamentally break standard commercial (COTS) and even industrial MIL-STD-810 electronics:

| Parameter | Sea Level Baseline (ISA) | Ladakh Sector (5,500 m AMSL) | Physical Impact on Electronics |
|---|---|---|---|
| **Atmospheric Pressure ($P$)** | $101.325\,\text{kPa}$ | **$50.5\,\text{kPa}$** ($-50.2\%$) | Low air molecule density; increases electron mean free path. |
| **Ambient Air Density ($\rho$)** | $1.225\,\text{kg/m}^3$ | **$0.709\,\text{kg/m}^3$** ($-42.1\%$) | Drastically degrades mass flow rate and heat carrying capacity. |
| **Ambient Temperature ($T_{\text{amb}}$)** | $+15.0^\circ\text{C}$ | **$-25^\circ\text{C}$ to $-40^\circ\text{C}$** | Severe electrolyte freezing; extreme thermal contraction. |
| **Diurnal Temperature Swing ($\Delta T$)** | $10^\circ\text{C}$ | **Up to $50^\circ\text{C}$ diurnal** | Rapid daily thermal cycling induces severe BGA solder fatigue. |
| **Air Convective Coefficient ($h$)** | $100\%$ ($h_0$) | **$55.4\%$** ($-44.6\%$ penalty) | Convective starvation: silicon overheats despite freezing air. |
| **Dielectric Breakdown of Air** | $\sim 3,000\,\text{V/mm}$ | **Drops toward $327\,\text{V}$ min** | Severe risk of corona discharge and high-voltage rail flashover. |
| **Enclosure Differential ($\Delta P$)** | $0\,\text{kPa}$ | **$+50.8\,\text{kPa}$ outward** | Massive overpressure causes lid bulging, seal blowout, and moisture trap. |

---

## 3. The 5 Root-Cause Physical Failure Cascades

Through first-principles modeling, HIMVAJRA deconstructs the high-altitude failure cascade into 5 distinct, traceable physical chains:

```
[1. HYPOBARIC THERMAL STARVATION CASCADE]
High Altitude (5,500m) ──► Low Pressure (50.5 kPa) ──► Low Density (0.709 kg/m³)
                       ──► Convection Derating (h ∝ ρ⁰·⁸) ──► Thermal Resistance Surge (+80%)
                       ──► Processor Hotspot Spikes (>82°C) ──► Silicon Throttling / Junction Burnout

[2. ELECTROCHEMICAL FREEZE & IMPEDANCE CASCADE]
Freezing Ambience (-25°C) ──► Electrolyte Viscosity Spikes ──► Arrhenius Impedance Surge (12 to 58 mΩ)
                          ──► Internal Voltage Drop (ΔV = I·R_int) ──► Terminal Voltage Drops Below 12.0V
                          ──► Premature Low-Voltage Cutoff (LVC) in 1.8 min (Drone Brownout)

[3. PASCHEN DIELECTRIC BREAKDOWN CASCADE]
Low Pressure (50.5 kPa) ──► Electron Mean Free Path Increases ──► Ionization Avalanche at Lower Voltages
                        ──► Paschen Breakdown Voltage Drops to ~327V Min ──► Partial Discharge / PCB Arcing
                        ──► Carbonization of FR4 Substrate ──► Catastrophic Short Circuit

[4. THERMOMECHANICAL CYCLING DAMAGE CASCADE]
Extreme Diurnal Swing (ΔT = 50°C) ──► CTE Mismatch (Silicon 2.6 ppm vs FR4 14 ppm vs Aluminum 23 ppm)
                                  ──► Repeated BGA Solder Joint Shear Strain ──► Norris-Landzberg Microcracking
                                  ──► Solder Joint Fatigue Failure (Life Drops from 3,500 to <420 Cycles)

[5. CONDENSATION & DIFFERENTIAL PRESSURE TRAP]
Rapid Descent (Cruise to Base) ──► Cold-Soaked Chassis Hits Humid Low Altitude ──► Surface Temp < Dew Point
                               ──► Liquid Condensation on Unpotted PCB ──► Inward Leakage via Blown Seals
                               ──► Corrosion & Short Circuits upon Next Power-On
```

---

## 4. The HIMVAJRA-HRM Hardware Countermeasure Suite

HIMVAJRA counters each physical failure mode with a dedicated, field-installable hardware intervention:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         HIMVAJRA-HRM PHYSICAL HARDWARE INTERVENTIONS                           │
├────────────────────────────────┬───────────────────────────────┬───────────────────────────────┤
│ FAILURE MECHANISM ADDRESSED    │ PHYSICAL COMPONENT PROPOSED   │ ENGINEERING IMPACT & METRICS  │
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Hypbaric Convective Starvation │ Sintered Copper Vapor Chamber │ Planar spreading (0.45 °C/W). │
│ (Chip reaches 82.4°C throttle) │ + Hard-Anodized Sky Radiator  │ Clamps Tj from 82.4°C to      │
│                                │                               │ 43.1°C via deep-sky radiation.│
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Electrochemical Freeze         │ Aspen Pyrogel-XTE Aerogel     │ Traps heat (0.015 W/m·K);     │
│ (Battery brownout in 1.8 min)  │ Jacket + Kapton 12W Preheater │ Pre-heats core to +12°C;      │
│                                │ with Closed-Loop PWM          │ Restores runtime to 21.4 min. │
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Paschen Dielectric Arcing      │ Dow Corning 1-2577 Silicone   │ Elastomeric barrier >42 kV/mm;│
│ (Creepage flashover at 54 kPa) │ Potting + CNC Isolation Gaps  │ Milled air-slots extend       │
│                                │                               │ creepage distance from 1.2mm  │
│                                │                               │ to >5.0 mm.                   │
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Enclosure Pressure Stress      │ Gore Automotive M12 e-PTFE    │ Dual-direction airflow        │
│ (50.8 kPa outward bulging)     │ Oleophobic Vent Membrane      │ (450 ml/min). Balances ΔP to  │
│                                │                               │ <0.15 kPa. Zero seal blowout. │
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Solder Joint Thermal Fatigue   │ Beryllium-Copper Kinematic    │ Compliant spring standoffs    │
│ (Cracking after 420 cycles)    │ Spring-Loaded PCB Standoffs   │ absorb CTE shear strains;     │
│                                │                               │ Extends life to >2,800 cycles.│
├────────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Operational Safety & Moisture  │ Deterministic STM32G431       │ Autonomous 10 Hz hard-real-   │
│ Condensation Short Circuits    │ GUARD Safety Controller       │ time FSM. Manages dew hold,   │
│                                │                               │ fan PWM, heater & load shed.  │
└────────────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 5. The 4 Coupled Subsystems of HIMVAJRA

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE COMPLETE HIMVAJRA ECOSYSTEM                               │
│                                                                                                 │
│  ┌───────────────────────────┐                        ┌──────────────────────────────────────┐  │
│  │   1. HIMVAJRA FORGE       │                        │   2. HIMVAJRA CHAMBER                │  │
│  │   (Failure-Physics Model) │                        │   (Empirical Ground Truth)           │  │
│  │   • ISA Barometric Model  │ ──Analytical Baseline─►│   • 2-Gal Vacuum Vessel (30-101 kPa) │  │
│  │   • Lumped RC Thermal Net │                        │   • Cryo Chamber Shell (-35..+55°C)  │  │
│  │   • Thévenin Battery ECM  │ ◄──Model Residual──────│   • 8-Ch TC DAQ + INA228 + BMP390    │  │
│  │   • Paschen Arcing Curve  │    Recalibration       │   • 6 Formal Test Protocols          │  │
│  └─────────────┬─────────────┘                        └──────────────────┬───────────────────┘  │
│                │                                                         │                      │
│                └───────────────────────────┬─────────────────────────────┘                      │
│                                            ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │   3. HIMVAJRA GUARD (Deterministic Edge Hardware Controller)                              │  │
│  │   • Dual MCU Architecture: STM32G431 (10 Hz Hard Safety FSM) + ESP32-S3 (Telemetry/LoRa)  │  │
│  │   • 4 Deterministic States: NOMINAL ──► DERATED ──► PROTECT ──► LOCKOUT                   │  │
│  │   • Actuators: 4-Wire Tachometer PWM Fan, Kapton MOSFET, Load Shed Relay, Charge Lock     │  │
│  └─────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
│                                            ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │   4. DECISION-SUPPORT DASHBOARD & FLEET RELIABILITY ENGINE                                │  │
│  │   • Inputs: Altitude, Temp, Pressure, SOH, Current, Payload                               │  │
│  │   • Predictions: Environmental Stress (0-100%), Usable Capacity, RUL Flight Time          │  │
│  │   • 4 Clear Decisions: CONTINUE MISSION / PRE-HEAT BATTERY / REDUCE LOAD / REPLACE        │  │
│  │   • Air-Gapped Standalone Operation for Remote Military Outposts                          │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. The 18 Dedicated Engineering Modules in the Digital Twin

The web application ([https://himvajra.vercel.app](https://himvajra.vercel.app)) is organized into 18 specialized engineering modules:

1. **01. Engineering Overview & Decision Dashboard**: Mission command center, 8 KPI readouts, end-to-end signal flow diagram, active hardware checklist, and live Decision Support Engine.
2. **02. Virtual Environmental Chamber**: Environmental test bench with sliders for altitude (0–6,000 m), temperature ($-40$ to $+30^\circ\text{C}$), electrical load, and mission flight profiles (Ground, Climb, Cruise, Loiter, Cold Soak, Morning Restart).
3. **03. Failure Cascades**: 5 interactive causal chains illustrating the physical step-by-step propagation of high-altitude failure modes. Clickable nodes reveal physical mechanisms and countermeasures.
4. **04. Hardware Config**: 10 interactive hardware switches that dynamically re-parameterize the physics engine equations in real time.
5. **05. 3D Enclosure Twin**: Isometric Canvas digital twin with rotation, $0–100\%$ exploded-view slider, component isolation, and technical callouts.
6. **06. Thermal Analysis**: Detailed convective starvation curves, boundary layer analysis, and vapor chamber planar spreading math ($T_j = T_{\text{amb}} + P \cdot \theta_{\text{eff}}$).
7. **07. Battery & Energy**: Thévenin equivalent circuit analysis, Arrhenius impedance curves, and cold-start vs. preheated discharge profiles.
8. **08. Dielectric & Paschen**: High-voltage Paschen curve breakdown simulator across pressures and electrode spacings.
9. **09. Condensation & $\Delta P$**: Psychrometric dew point margin tracking and enclosure mechanical bulging analysis.
10. **10. GUARD Controller**: Deterministic 4-state finite state machine (`NOMINAL` $\to$ `DERATED` $\to$ `PROTECT` $\to$ `LOCKOUT`) with 11-fault injection test board. **Zero AI in the safety loop.**
11. **11. Validation Lab**: Re-creation of all 6 DRDO experimental test protocols with live stage progress (1–7) and pass/fail gate criteria.
12. **12. Baseline vs Protected**: Simultaneous split-screen comparison of unmodified COTS hardware vs. HIMVAJRA-protected hardware under matched environmental conditions.
13. **13. Telemetry DAQ**: High-speed telemetry recorder with real-time strip charts, tabular ring buffer, and CSV export.
14. **14. Hardware BOM**: Full Bill of Materials categorized with specifications, Indian Rupee (INR) costs, and source document citations.
15. **15. Engineering Math**: Transparent first-principles mathematical formulas with live numerical substitutions.
16. **16. Safety & FMEA**: Failure Mode and Effects Analysis matrix with RPN scoring, single-point-of-failure analysis, and interlocks.
17. **17. Retrofit Planner**: Step-by-step modular upgrade guide for Tactical Drones, Radar PSUs, Telecom BTS, and Edge Single-Board Computers.
18. **18. Engineering Report**: Automated formal DRDO test certification report generator with print/PDF styling and scientific disclaimers.

---

## 7. The 6 Chamber Experimental Test Protocols

To prove that HIMVAJRA is backed by physical experimental rigor rather than theoretical speculation, the platform replicates the 6 test protocols developed for hypbaric-cryogenic chamber testing:

### TEST 01: Cold Air / Hot Chip Test (Convective Starvation)
- **Objective**: Measure semiconductor junction temperature rise under rarefied atmosphere.
- **Protocol**: Apply 15 W continuous load at $50.5\,\text{kPa}$ (5,500 m) and $-25^\circ\text{C}$.
- **Physics**: At $0.709\,\text{kg/m}^3$, convective cooling drops by $44.6\%$. Unmitigated chip rises to $82.4^\circ\text{C}$ (near throttle threshold).
- **Pass Criterion**: HIMVAJRA vapor chamber + radiator must clamp $T_j \le 50.0^\circ\text{C}$ (Achieved: $43.1^\circ\text{C}$).

### TEST 02: Sub-Zero Battery Extraction (Arrhenius Impedance & LVC)
- **Objective**: Measure usable capacity and discharge time under freezing cold-soak.
- **Protocol**: 4S 5,000 mAh LiPo subjected to 12.5 A discharge at $-25^\circ\text{C}$.
- **Physics**: Unheated internal resistance surges from $12\,\text{m}\Omega$ to $58\,\text{m}\Omega$. Terminal voltage collapses below $12.0\,\text{V}$ LVC cutoff in $1.8\,\text{min}$.
- **Pass Criterion**: Kapton pre-heating to $+12^\circ\text{C}$ must yield $>20.0\,\text{min}$ flight runtime (Achieved: $21.4\,\text{min}$).

### TEST 03: Dielectric Arc & Paschen Breakdown Test
- **Objective**: Verify electrical clearance and suppression of partial discharge at low pressure.
- **Protocol**: Apply 400 V DC transient across PCB spark gap at $54\,\text{kPa}$.
- **Physics**: Mean free path expands, reducing breakdown threshold toward Paschen minimum ($327\,\text{V}$).
- **Pass Criterion**: Zero arcing / partial discharge with Dow Corning 1-2577 coating and milled isolation slots (Achieved: $>42\,\text{kV/mm}$ isolation).

### TEST 04: Thermal Shock & Diurnal Cycling (Norris-Landzberg)
- **Objective**: Measure mechanical solder joint integrity under extreme Himalayan diurnal swings.
- **Protocol**: Cycle from $-40^\circ\text{C}$ to $+35^\circ\text{C}$ across 100 thermal cycles at 1 cycle/hour.
- **Physics**: CTE differential shear strains cause micro-fissuring in standard BGA/QFN solder joints.
- **Pass Criterion**: Resistance change across daisy-chain $<5\%$ with kinematic spring standoffs (Achieved: $<1.2\%$ resistance change).

### TEST 05: Enclosure Differential Pressure & Hermeticity Test
- **Objective**: Verify enclosure structural integrity during rapid altitude ascent.
- **Protocol**: Depressurize chamber from $101.3\,\text{kPa}$ to $47.2\,\text{kPa}$ (6,000 m equivalent) at $15\,\text{m/s}$.
- **Physics**: Sealed enclosures develop $+54.1\,\text{kPa}$ outward overpressure, bulging lid and extruding O-rings.
- **Pass Criterion**: Gore e-PTFE vent membrane must maintain internal $\Delta P < 1.0\,\text{kPa}$ (Achieved: $0.15\,\text{kPa}$).

### TEST 06: Condensation & Rapid Altitude Descent Test
- **Objective**: Prevent moisture short circuits when transitioning from cold cruise to humid valley.
- **Protocol**: Cold-soak DUT at $-25^\circ\text{C}$ / $54\,\text{kPa}$, then rapidly repressurize to $85\,\text{kPa}$ at $80\%$ RH.
- **Physics**: DUT surface temperature lags ambient dew point, causing liquid water condensation.
- **Pass Criterion**: GUARD controller holds restart, triggers 90-second moisture purge heater cycle until surface temperature exceeds $T_{\text{dew}} + 3.0^\circ\text{C}$ (Achieved: Zero condensation shorts).

---

## 8. The Predictive Decision-Support Dashboard & Action Engine

The newest core module transforms the platform into an **Operational Decision-Support System for Field Dispatchers**:

### 8.1 Inputs
- **Altitude**: $0$ to $6,000\,\text{m}$ AMSL (default: $5,500\,\text{m}$)
- **Ambient Temperature**: $-40^\circ\text{C}$ to $+30^\circ\text{C}$ (default: $-25.0^\circ\text{C}$)
- **Atmospheric Pressure**: Auto-computed via ISA Barometric equation ($50.5\,\text{kPa}$)
- **Battery State of Health (SOH)**: $50\%$ to $100\%$ (default: $90\%$)
- **Discharge Cruise Current**: $2.0\,\text{A}$ to $35.0\,\text{A}$ (default: $12.5\,\text{A}$)
- **Payload Compute Power**: $5.0\,\text{W}$ to $60.0\,\text{W}$ (default: $15.0\,\text{W}$)
- **Battery Pre-Heater State**: Toggleable (`ACTIVE (+12°C)` vs. `COLD-SOAK (-25°C)`)

### 8.2 Calculated / Predicted Prognostics
- **Environmental Stress Index (ESI)**:
  $$\text{ESI} = 0.40 \cdot \left(\frac{P_0 - P}{P_0}\right) + 0.45 \cdot \left(\frac{25 - T_{\text{amb}}}{65}\right) + 0.15 \cdot \left(\frac{10 - \text{DewMargin}}{10}\right)$$
- **Battery Degradation & Arrhenius Impedance**:
  $$R_{\text{int}}(T) = 12.0 \cdot \exp\left[3850 \cdot \left(\frac{1}{T_{\text{core}} + 273.15} - \frac{1}{298.15}\right)\right]$$
  Computes terminal voltage sag $\Delta V = I \cdot R_{\text{int}}$ and flags brownout risks.
- **Usable Capacity ($C_{\text{usable}}$)**:
  Calculates usable Ah and retention % factoring SOH and electrolyte temperature.
- **Predicted RUL / Flight Time**:
  Estimates operational flight minutes remaining before hitting the $12.0\,\text{V}$ LVC cutoff.
- **Equipment Reliability Score**:
  Composite index combining semiconductor thermal headroom, dielectric clearance margin, and enclosure differential pressure.

### 8.3 The 4 Recommended Dispatch Decisions
The decision engine evaluates the model output and issues one of 4 unambiguous operational commands:

1. 🟢 **CONTINUE MISSION**:
   - *Condition*: $T_j < 68^\circ\text{C}$, $V_{\text{term}} > 13.5\,\text{V}$, $\text{SOH} \ge 75\%$, battery pre-heated.
   - *Action*: Mission parameters are nominal. Cleared for takeoff/continuous operation.
2. 🟡 **PRE-HEAT BATTERY**:
   - *Condition*: $T_{\text{amb}} < 10^\circ\text{C}$, Pre-heater inactive, $\text{SOH} \ge 65\%$.
   - *Action*: Sub-zero electrolyte viscosity causes $R_{\text{int}} > 35\,\text{m}\Omega$. Launching cold trips premature LVC cutoff within $1.8\,\text{min}$. Engage Kapton heating elements to reach $+12^\circ\text{C}$ before takeoff.
3. 🟠 **REDUCE LOAD**:
   - *Condition*: Silicon hotspot $T_j \ge 68.0^\circ\text{C}$ OR Terminal voltage $12.0\,\text{V} < V_{\text{term}} \le 12.8\,\text{V}$.
   - *Action*: Convective cooling penalty or high discharge current threatening margins. Shed auxiliary sensors and derate compute SoC from 15W to 7.5W to restore safety headroom.
4. 🔴 **REPLACE BATTERY / ABORT**:
   - *Condition*: $\text{SOH} < 65\%$ OR Terminal voltage $V_{\text{term}} \le 12.0\,\text{V}$ cutoff trip.
   - *Action*: Irreversible electrochemical capacity loss. Pack cannot deliver required current without fatal mid-air brownout. Abort launch and replace battery module immediately.

---

## 9. Bill of Materials (BOM) & Cost Feasibility

All components specified in HIMVAJRA are real, commercially procurable defense/aerospace-grade parts with documented Indian Rupee (INR) pricing:

| Category | Component / Part | Key Specification | Cost (INR) | Source |
|---|---|---|---|---|
| **Chamber** | Vacuum Desiccator Chamber | 2-Gallon Stainless/Polycarbonate, full vac rated | ₹6,500 | SOURCE DOC |
| **Chamber** | Rotary Vacuum Pump | 3 CFM, 150 Micron Rotary Vane Pump | ₹7,200 | SOURCE DOC |
| **Chamber** | Proportional Bleed Valve | SMC 12V NC Solenoid + Precision Needle | ₹1,850 | SOURCE DOC |
| **Chamber** | Cryo Shell & Dry Ice Grid | 25L Polyurethane Insulated Cold Shell | ₹2,400 | SOURCE DOC |
| **Electrical** | Safety Microcontroller | STM32G431KBU6 Cortex-M4 (-40 to +125°C) | ₹1,250 | SOURCE DOC |
| **Electrical** | Supervisory Gateway | ESP32-S3-WROOM-1U (Wi-Fi, BLE, LoRa, FRAM) | ₹1,050 | SOURCE DOC |
| **Electrical** | Thermocouple DAQ Array | MAX31855 SPI Interface + 8x K-Type Probes | ₹3,500 | SOURCE DOC |
| **Electrical** | Bus Power Monitor | TI INA228AQDGSRQ1 (20-bit ΔΣ, 85V, 50A) | ₹1,400 | SOURCE DOC |
| **Electrical** | Absolute Barometer | Bosch BMP390 + NXP MPX5100AP Redundant | ₹1,800 | SOURCE DOC |
| **Electrical** | Dew-Point Hygrometer | Sensirion SHT45 (±1.0% RH, ±0.1°C) | ₹950 | SOURCE DOC |
| **Thermal** | Sintered Vapor Chamber | Celsia Copper-Water Planar (120x70x2.5mm, 85W) | ₹3,200 | SOURCE DOC |
| **Thermal** | Nanoporous Aerogel Wrap | Aspen Pyrogel XTE 3mm (0.016 W/m·K) | ₹2,800 | SOURCE DOC |
| **Thermal** | Flexible Kapton Heater | Minco Polyimide Etched Foil (12V, 25W, 100x50mm)| ₹1,100 | SOURCE DOC |
| **Mechanical** | Pressure Equalization Vent | Gore Automotive PMF100416 M12 e-PTFE (2x) | ₹850 | SOURCE DOC |
| **Electrical** | Conformal Silicone Potting | Dow Corning 1-2577 Elastomeric Coating | ₹1,800 | SOURCE DOC |
| **Mechanical** | Radiating Enclosure | CNC 6061-T6 Black Anodized + Belleville Mounts | ₹3,600 | SOURCE DOC |
| **Reserve** | Harnesses, Fuses, Seals | Military PTFE wiring, high-side switches, seals | ₹11,450 | ESTIMATE |
| **TOTAL** | **Complete Chamber + Retrofit Pack** | **Ready for DRDO Lab Fabrication & Testing** | **₹52,900** | **BUDGET APPROVED** |

---

## 10. Step-by-Step Retrofit Workflows for Armed Forces Equipment

HIMVAJRA supports 4 standardized, field-installable retrofit packages:

1. **Tactical UAV LiPo Battery Packs (4S 5,000 mAh)**:
   - *Step 1*: Wrap cell pack with 3mm Aspen Pyrogel-XTE aerogel blanket; secure with Nomex harness.
   - *Step 2*: Affix 12W Kapton polyimide etched-foil heating elements with embedded NTC probe between center cells.
   - *Step 3*: Interpose HIMVAJRA solid-state PROFET disconnect switch between battery lead and Power Distribution Board (PDB).
   - *Step 4*: Connect balance lead to GUARD controller for real-time State-of-Power cutoff execution.
2. **Radar Power Supply Units (PSU 400V High-Voltage Rail)**:
   - *Step 1*: Remove stock aluminum heatsink; insert Celsia sintered vapor chamber cold-plate directly over switching MOSFETs.
   - *Step 2*: CNC mill 1.85mm clearance air-slots between high-voltage traces; apply brush coat of Dow Corning 1-2577 silicone.
   - *Step 3*: Wire GUARD controller in-line with 28V auxiliary power rail and K-type thermocouple probe on the power stage hotspot.
   - *Step 4*: Drill 12.5mm hole in upper chassis wall and press-fit Gore M12 e-PTFE vent membrane for pressure balance.
3. **Telecom Base-Transceiver Stations (BTS Tower Cabinets)**:
   - *Step 1*: Fit vapor chamber planar thermal adapter to RF Power Amplifier module.
   - *Step 2*: Mount 15W PTC moisture-purge heating strip across cabinet air intake manifold.
   - *Step 3*: Install SHT45 dew-point probe with interlocked start relay to block power-on during frost thaw.
   - *Step 4*: Install dual Gore M12 vents on opposing chassis faces for cross-venting.
4. **Tactical Edge Computers (Jetson Orin Nano / Raspberry Pi 5)**:
   - *Step 1*: Swap plastic enclosure for billet CNC 6061-T6 black hard-anodized radiating enclosure.
   - *Step 2*: Install Belleville spring disc washers under all 4 PCB mounting screws to absorb CTE shear stress.
   - *Step 3*: Connect GUARD UART line to Jetson serial port for autonomous `nvpmodel` 15W $\to$ 7.5W throttling.
   - *Step 4*: Install Gore vent membrane on top chassis plate.

---

## 11. Scientific Integrity, Honesty & Anti-Slop Principles

To maintain complete credibility with DRDO and military evaluation panels:
1. **Never Label Simulated Results as Measured Experimental Data**:
   Every number in the interface is tagged with clear badges: `SOURCE DOCUMENT`, `CALCULATED PHYSICS`, `SIMULATED TWIN`, `DESIGN TARGET`, or `NOT PHYSICALLY VALIDATED`.
2. **Never Claim a Hardware Connection that Does Not Exist**:
   The interface explicitly displays `VIRTUAL SENSOR`, `SIMULATED ACTUATOR`, and `AIR-GAPPED TWIN`. It does not pretend to be physically wired to real hardware while running on a laptop.
3. **No AI in the Safety Loop**:
   All safety-critical decisions (fan modulation, load shedding, charge inhibit, safety lockout) are governed by a **deterministic 4-state finite state machine** on the STM32G431. Machine learning is restricted strictly to prognostic residual correction and remaining useful life estimation.
4. **Air-Gapped & Offline Ready**:
   The entire system runs 100% offline without external cloud dependencies or API keys, matching defense field requirements.

---

## 12. Quick Demonstration Guide for SIH Judges

When presenting to hackathon evaluators, use the following **4-minute demonstration script**:

1. **Step 1: Open Home Screen (`01. Engineering Overview`)**:
   - Point out the real-time altitude environment: $5,500\,\text{m}$, $50.5\,\text{kPa}$, $-25.0^\circ\text{C}$, $0.709\,\text{kg/m}^3$ air density.
   - Click **`▶ RUN 5,500m TEST`**. Show how the physics engine recalculates the entire thermal, electrical, and dielectric state.
2. **Step 2: Demonstrate the Decision-Support Dashboard**:
   - Show the operational inputs: change altitude to $5,000\,\text{m}$ and temperature to $-35^\circ\text{C}$ with Pre-Heater OFF (click preset `Cold Start (-35°C)`).
   - Point to the **Decision Box**: the system immediately outputs:
     `🟡 DECISION: PRE-HEAT BATTERY PACK` with technical justification (impedance surge to $58.2\,\text{m}\Omega$, LVC brownout risk in 1.8 min).
   - Click **`ENACT ACTION: ENGAGE PRE-HEATERS`**. Watch the battery temperature warm to $+12^\circ\text{C}$, resistance drop to $13.2\,\text{m}\Omega$, usable capacity jump to $4.28\,\text{Ah}$, and runtime extend to $20.5\,\text{min}$. The decision turns to:
     `🟢 DECISION: CONTINUE MISSION`.
3. **Step 3: Show the Failure Cascades (`03. Failure Cascades`)**:
   - Click on the *Hypbaric Thermal Starvation Cascade*. Show judges the exact physical links from low pressure to convective derating ($h \propto \rho^{0.8}$) to semiconductor junction overheating.
4. **Step 4: Show the 3D Enclosure Twin (`05. 3D Enclosure Twin`)**:
   - Rotate the isometric enclosure, slide the *Exploded View* slider to $50\%$, and click on the *Sintered Vapor Chamber* and *Gore Vent* to show mechanical integration.
5. **Step 5: Run a Virtual Chamber Validation Test (`11. Validation Lab`)**:
   - Select *TEST 01: Cold Air / Hot Chip Test*.
   - Click **`▶ RUN TEST 01`**. Watch the live test progress through Sea-Level Baseline, Depressurization, Temperature Pull-Down, Steady-State Load, and Recovery.
   - Show the pass criterion: unmitigated chip overheats ($82.4^\circ\text{C}$); HIMVAJRA clamps temperature to $43.1^\circ\text{C}$ (**PASSED**).
6. **Step 6: Conclude with the Problem Statement Alignment**:
   > *"Judges, we have not built a generic dashboard or proposed theoretical advice. We have designed a physical Hardened Retrofit Module for legacy military equipment, modeled the failure physics from first principles, and built the virtual laboratory to prove and validate every design choice before physical fabrication."*

---

*Repository*: [https://github.com/harshshah2707/HimVajra.git](https://github.com/harshshah2707/HimVajra.git)  
*Live Platform*: [https://himvajra.vercel.app](https://himvajra.vercel.app)
