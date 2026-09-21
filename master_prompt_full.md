<USER_REQUEST>
# WEB SIMULATION MASTER PROMPT

## High-Altitude Electronics Reliability & Protection Platform

Build a **fully functional, high-fidelity engineering simulation web application** for the proposed high-altitude electronics reliability system.

The visual identity must closely follow the supplied SIH presentation design:

> **Professional aerospace / defence engineering + scientific instrumentation + government technology dashboard**

The website must NOT look like a generic SaaS dashboard, generic AI dashboard, cyberpunk interface, or startup landing page.

It should feel like an actual **engineering control, validation, simulation, and fleet-monitoring platform**.

---

# 1. CORE PRODUCT

The web application represents the software layer of a system that:

```text
CONTROLLED VALIDATION
        ↓
PHYSICS-BASED PREDICTION
        ↓
THERMAL / ELECTRICAL RISK ANALYSIS
        ↓
EMBEDDED PROTECTION
        ↓
FIELD TELEMETRY
        ↓
FLEET MONITORING
        ↓
MAINTENANCE DECISION
```

The platform should allow an engineer/operator to:

* Configure altitude/environmental conditions
* Configure electronics/load parameters
* Run a physics-based simulation
* Observe pressure, density, temperature and thermal behaviour
* View calculated derating
* View prediction bands
* Simulate faults
* Observe GUARD state transitions
* Observe protective actions
* Inspect telemetry
* View battery state-of-power
* View RUL / degradation estimates
* Generate a derating report
* Inspect fleet-level information

The application should make the underlying engineering logic **visible and understandable**.

---

# 2. VISUAL IDENTITY

Use the same visual language as the provided SIH slides.

## Overall Style

* Aerospace engineering
* High-altitude environment
* Scientific instrumentation
* Defence-grade reliability
* Clean government technology
* Engineering workstation
* Technical but approachable
* Data-rich without looking cluttered

Do NOT use:

* Neon cyberpunk
* Purple AI gradients
* Glassmorphism everywhere
* Cryptocurrency-style UI
* Generic startup cards
* Excessive rounded SaaS components
* Giant hero sections
* Cartoon illustrations
* Futuristic sci-fi interfaces
* Excessive animations

---

# 3. COLOR SYSTEM

Base palette:

### Deep Navy

Primary background / header.

### White

Primary content surfaces.

### Light Blue

Technical information and environmental monitoring.

### Orange

Critical engineering calculations, validation gates, warnings and important actions.

### Green

Normal / validated / healthy states.

### Red

Fault / protection / lockout states.

### Purple

Infrastructure / fleet / deployment layer.

Use orange very deliberately.

Orange should immediately communicate:

> **Calculated / important / validation / engineering attention**

Do not make the entire interface orange.

---

# 4. TYPOGRAPHY

Use a professional technical sans-serif font.

Recommended:

* Inter
* IBM Plex Sans
* IBM Plex Mono for telemetry / equations / numerical values

Use:

### Large

System title / major values

### Medium

Section headings

### Small

Technical labels

### Monospace

* Sensor values
* Telemetry
* Equations
* Pressures
* Temperatures
* Timestamps
* Device IDs
* Model outputs

Typography should resemble an engineering instrument rather than a marketing website.

---

# 5. GLOBAL LAYOUT

Use a persistent engineering application shell.

```text
┌──────────────────────────────────────────────────────────────┐
│ HIGH-ALTITUDE RELIABILITY SYSTEM        SYSTEM STATUS       │
├───────────────┬──────────────────────────────────────────────┤
│               │                                              │
│  NAVIGATION   │              MAIN WORKSPACE                  │
│               │                                              │
│  Overview     │                                              │
│  Simulation   │                                              │
│  Validation   │                                              │
│  Prediction   │                                              │
│  GUARD        │                                              │
│  Telemetry    │                                              │
│  Fleet        │                                              │
│  Reports      │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

The navigation should remain visually compact.

The main workspace should receive most of the screen.

---

# 6. TOP HEADER

Create a strong engineering header.

Left:

**HIGH-ALTITUDE RELIABILITY PLATFORM**

Subheading:

**Physics-driven prediction · measured validation · autonomous protection**

Right:

```text
SYSTEM
● ONLINE

MODE
SIMULATION

DATA
LOCAL / AIR-GAPPED

LAST SYNC
13:42:18
```

Include a small mountain/high-altitude silhouette in the header.

Keep it subtle.

---

# 7. MAIN DASHBOARD

The default landing page should be an engineering overview.

Show:

## ENVIRONMENT

```text
ALTITUDE
5,500 m

PRESSURE
50.5 kPa

AIR DENSITY
0.50 ρ₀

AMBIENT
25.0 °C
```

## ELECTRONICS

```text
HOTSPOT
63.0 °C

POWER
15.0 W

VOLTAGE
24.1 V

CURRENT
0.62 A
```

## SYSTEM STATE

Large state indicator:

```text
PROTECT
```

or:

```text
NOMINAL
DERATED
PROTECT
LOCKOUT
```

Use the same visual state progression:

```text
NOMINAL → DERATED → PROTECT → LOCKOUT
```

---

# 8. LIVE ENVIRONMENT SIMULATION

Create a functional simulation panel.

Controls:

### Altitude

Slider:

```text
0 m ──────────────── 5,500 m
```

### Ambient Temperature

Range:

```text
-40°C ───────────── +80°C
```

### Pressure

Automatically calculated from altitude.

### Cooling Mode

Toggle:

* Natural
* Forced

### Load

Adjustable power:

```text
1 W → 50 W
```

When values change, the simulation should update the calculated thermal behaviour.

Do NOT make controls fake.

The displayed outputs must be calculated from the simulation model.

---

# 9. PHYSICS ENGINE

Implement a transparent engineering calculation layer.

Use the relationships defined in the project:

### Air density

```text
ρ = P / (R · T)
```

### Natural convection

```text
h ∝ ρ^0.5
```

### Forced convection

```text
h ∝ ρ^0.8
```

### Paschen

```text
V_breakdown = f(p · d)
```

### Battery model

```text
V_term = V_ocv − I · R_int(T)
```

### Thermal model

Use a simplified thermal RC model for the simulation.

The interface should show which calculation is active.

Example:

```text
PHYSICS MODEL
✓ Density
✓ Convection
✓ Thermal RC
✓ Electrical load
✓ Battery ECM
✓ Breakdown risk
```

---

# 10. LIVE THERMAL GRAPH

Create a large Plotly-style chart.

X-axis:

**Altitude**

Y-axis:

**Hotspot Temperature**

Display:

* Natural cooling
* Forced cooling
* Current operating point

Example:

```text
Temperature
    │
70°C│                         ●
    │                    ●
60°C│               ●
    │          ●
50°C│     ●
    │ ●
    └────────────────────────────
      0   1000  3000  4500  5500
                 Altitude
```

The chart must update when simulation parameters change.

Use:

* Orange for forced cooling
* Blue for natural cooling
* Red marker for danger threshold

---

# 11. THERMAL PENALTY TABLE

Create a highly visible engineering table:

| Altitude |        P | ρ/ρ₀ | Natural | Forced |
| -------- | -------: | ---: | ------: | -----: |
| 3,000 m  | 70.1 kPa | 0.69 |    +20% |   +33% |
| 4,500 m  | 57.7 kPa | 0.57 |    +32% |   +56% |
| 5,500 m  | 50.5 kPa | 0.50 |    +41% |   +74% |

Highlight the selected altitude in orange.

Label:

**CALCULATED — NOT MEASURED**

This distinction is extremely important.

---

# 12. WORKED ENGINEERING EXAMPLE

Create a dedicated card:

## WORKED EXAMPLE

```text
15 W HOTSPOT

Sea-level θsa
3.0 °C/W

Altitude
5,500 m

Cooling
Forced

Predicted hotspot
≈63 °C
```

Then show:

```text
45°C
  ↓
ALTITUDE PENALTY
  ↓
63°C
```

Caption:

**Same ambient temperature. Same power. Reduced convective cooling.**

Do not claim this is measured.

Label:

**SIMULATION / CALCULATED**

---

# 13. FORGE — PREDICTION MODULE

Create a dedicated page.

Title:

# FORGE

### Physics + residual correction

Show:

```text
MEASURED INPUTS
      ↓
THERMAL RC
      ↓
PASCHEN
      ↓
COFFIN–MANSON
      ↓
BATTERY ECM
      ↓
GP RESIDUAL CORRECTION
      ↓
PREDICTION BAND
```

Outputs:

### Derating Report

### Hardening BOM

### RUL Curve

### Confidence Band

Do not pretend the ML model is trained if no trained model exists.

If no real dataset is connected:

```text
MODEL STATUS
PHYSICS BASELINE

ML RESIDUAL
DEMO / NOT TRAINED
```

This is preferable to fake AI.

---

# 14. GUARD MODULE

Create a dedicated control screen.

Title:

# GUARD

### Embedded protection controller

Show a state machine:

```text
┌─────────┐
│ NOMINAL │
└────┬────┘
     ↓
┌─────────┐
│ DERATED │
└────┬────┘
     ↓
┌─────────┐
│ PROTECT │
└────┬────┘
     ↓
┌─────────┐
│ LOCKOUT │
└─────────┘
```

Each state should have:

* Trigger
* Current limits
* Protective action
* Operator notification

---

# 15. PROTECTIVE ACTIONS

When thresholds are crossed, show:

```text
✓ FAN CONTROL
✓ HEATER FILM
✓ LOAD SHED
✓ CHARGE INHIBIT
✓ COMPUTE DERATE
✓ DEW-POINT POWER-UP HOLD
```

Make these react to simulation conditions.

Example:

If hotspot temperature exceeds threshold:

```text
SYSTEM TRANSITION

DERATED → PROTECT

Reason:
Thermal envelope exceeded

Action:
Compute derate enabled
```

---

# 16. FAULT INJECTION

This is an important demo feature.

Create a:

# FAULT INJECTION

panel with buttons:

```text
[ HIGH ALTITUDE ]

[ SENSOR FAILURE ]

[ OVER-TEMPERATURE ]

[ OVERCURRENT ]

[ LOW BATTERY ]

[ PRESSURE DROP ]

[ FLASHOVER ]

[ COMMUNICATION LOSS ]
```

When activated:

1. Simulation changes
2. Sensor state changes
3. GUARD evaluates condition
4. System state changes
5. Protective action appears
6. Event is logged

This should be one of the strongest live-demo features.

---

# 17. SENSOR TELEMETRY

Create a live telemetry screen.

Sensors:

```text
TC-01   51.2°C   ●
TC-02   53.4°C   ●
TC-03   55.1°C   ●
TC-04   57.2°C   ●
TC-05   61.8°C   ●
TC-06   63.0°C   ●
TC-07   59.2°C   ●
TC-08   56.4°C   ●
```

Also show:

* Pressure
* Temperature
* Voltage
* Current
* Power
* IR hotspot
* Flashover status

Use live updating.

---

# 18. TELEMETRY ARCHITECTURE

Visualize:

```text
STM32G431
     ↓
ESP32-S3
     ↓
MQTT / LoRa
     ↓
STORE & FORWARD
     ↓
FIELD SERVER
     ↓
TIMESCALEDB
     ↓
FLEET UI
```

Show:

**~230 DAY LOCAL BUFFER**

Do not claim this is a measured capacity unless it is actually implemented.

---

# 19. OFFLINE-FIRST DESIGN

The application must visibly communicate:

```text
● AIR-GAPPED

NO CLOUD DEPENDENCY

LOCAL DATA

STORE-AND-FORWARD

OFFLINE INSTALLER
```

The UI should continue working if network connectivity is disabled.

For the web simulation, simulate connectivity loss:

```text
[ DISABLE NETWORK ]
```

Then show:

```text
NETWORK OFFLINE

LOCAL SIMULATION CONTINUES

Telemetry buffered locally

Pending records: 27
```

When connectivity returns:

```text
SYNC COMPLETE
27 records transmitted
```

---

# 20. FLEET VIEW

Create a map-based fleet dashboard.

Use MapLibre or an offline map.

Show assets at different elevations.

Example:

```text
SITE A
5,500 m
● PROTECT

SITE B
4,500 m
● DERATED

SITE C
3,000 m
● NOMINAL
```

Clicking an asset opens:

* Environment
* Thermal state
* GUARD state
* Battery state
* Last telemetry
* Risk
* Maintenance recommendation

---

# 21. RUL / MAINTENANCE

Create a degradation visualization.

Title:

# REMAINING USEFUL LIFE

Show:

```text
100% ┤●
     │ \
 80% ┤  \
     │   \
 60% ┤    ●
     │      \
 40% ┤       ●
     │         \
 20% ┤          ●
     └────────────────
       0   6   12  18 months
```

Show confidence band.

Do not claim real RUL accuracy without validated data.

Use:

**MODELLED ESTIMATE**

when appropriate.

---

# 22. REPORT GENERATION

Create a functional:

**GENERATE DERATING REPORT**

button.

Report should contain:

* Asset ID
* Environment
* Pressure
* Altitude
* Temperature
* Power
* Thermal penalty
* Predicted hotspot
* Risk state
* GUARD state
* Recommended derating
* Maintenance recommendation
* Model confidence
* Timestamp

---

# 23. TECHNOLOGY STACK PAGE

Include a compact technical section:

```text
FRONTEND
React + TypeScript + Plotly + MapLibre

BACKEND
Python + FastAPI

MESSAGING
MQTT / Mosquitto

DATABASE
PostgreSQL + TimescaleDB

CACHE
Redis

AI / ML
scikit-learn
Gaussian Process residual correction
Isolation Forest
RLS Thévenin model

EDGE
STM32G431
ESP32-S3

INFRASTRUCTURE
Docker
Offline installer
Air-gapped deployment
```

Keep AI visually equal to other components.

The project is fundamentally **physics-driven**.

---

# 24. RESPONSIVE DESIGN

Primary target:

**1920 × 1080 desktop engineering display**

Also support:

* 1440 × 900
* Laptop
* Tablet

Desktop should be the priority.

Do not sacrifice information density for mobile-first cards.

---

# 25. INTERACTION DESIGN

The application should feel alive.

Examples:

### Changing altitude

Automatically updates:

* Pressure
* Density
* Thermal penalty
* Hotspot prediction
* Risk
* GUARD state

### Increasing power

Updates:

* Heat generation
* Hotspot
* Derating requirement

### Triggering sensor failure

Updates:

* Sensor status
* Confidence
* GUARD behaviour
* Alert log

### Triggering communication loss

Updates:

* Connectivity state
* Local buffer
* Sync queue

---

# 26. DEMO MODE

Create a prominent:

**DEMO MODE**

button.

Demo mode should load a controlled scenario:

```text
ALTITUDE: 5,500 m
PRESSURE: 50.5 kPa
AMBIENT: 25°C
LOAD: 15 W
COOLING: FORCED
HOTSPOT: ≈63°C
STATE: PROTECT
```

Then allow the operator to trigger:

```text
NORMAL
→ HIGH ALTITUDE
→ THERMAL RISK
→ PROTECT
→ SENSOR FAULT
→ LOCKOUT
→ RECOVERY
```

This should provide a complete 2-minute SIH demonstration.

---

# 27. ENGINEERING CREDIBILITY

Never create fake functionality just to make the interface look complete.

If a component is simulated:

Clearly label it:

**SIMULATION**

If a model is not trained:

Show:

**PHYSICS BASELINE**

If hardware is not connected:

Show:

**HARDWARE OFFLINE**

If data is synthetic:

Show:

**SYNTHETIC DATA**

The application should demonstrate engineering honesty.

---

# 28. VISUAL HIERARCHY

The most important information should always be visually dominant:

### 1.

Current system state

### 2.

Altitude / environment

### 3.

Hotspot temperature

### 4.

Thermal prediction

### 5.

Protection action

### 6.

Underlying telemetry

The user should understand system health within 3 seconds.

---

# 29. MICRO-ANIMATIONS

Use restrained engineering animations:

* Telemetry values updating
* Graph traces moving
* State transitions
* Sensor heartbeat indicators
* Data packets moving through architecture
* Alert pulse
* Synchronization progress

Avoid:

* Particle backgrounds
* Floating 3D objects
* Excessive motion
* Decorative animations

Every animation should communicate system activity.

---

# 30. DESIGN LANGUAGE

The entire platform should visually feel like:

**"A real engineering system that happens to have an excellent UI."**

Not:

**"A website pretending to be an engineering system."**

Use:

* Technical labels
* Units everywhere
* Timestamps
* Device IDs
* Status indicators
* Engineering equations
* Calibration information
* Model confidence
* Measured vs calculated distinction
* Audit events

These details create credibility.

---

# 31. FINAL PRODUCT STRUCTURE

Build the following routes/pages:

```text
/
├── Overview
├── Simulation
├── Validation
├── FORGE
├── GUARD
├── Telemetry
├── Fleet
├── Maintenance
└── Reports
```

The most important pages are:

1. Overview
2. Simulation
3. FORGE
4. GUARD
5. Fleet

Prioritize these if development time is limited.

---

# 32. IMPLEMENTATION PRIORITY

Build in this order:

### P0

Functional simulation engine

### P0

Overview dashboard

### P0

Thermal prediction graph

### P0

GUARD state machine

### P0

Fault injection

### P1

Telemetry simulation

### P1

FORGE prediction page

### P1

Fleet view

### P1

Report generation

### P2

Advanced RUL

### P2

Advanced analytics

Do NOT spend time polishing low-priority pages before the core simulation works.

---

# 33. FINAL REQUIREMENT

The final application should make it possible for someone to perform this complete sequence:

```text
SET ALTITUDE
      ↓
SYSTEM CALCULATES PRESSURE
      ↓
AIR DENSITY CHANGES
      ↓
THERMAL PENALTY INCREASES
      ↓
HOTSPOT TEMPERATURE RISES
      ↓
FORGE PREDICTS RISK
      ↓
GUARD CHANGES STATE
      ↓
PROTECTIVE ACTION ACTIVATES
      ↓
EVENT IS LOGGED
      ↓
FIELD SERVER STORES TELEMETRY
      ↓
FLEET UI UPDATES
      ↓
MAINTENANCE ACTION GENERATED
```

That sequence is the **core demonstration of the product**.

Make it work end-to-end.

---

# FINAL DESIGN PRINCIPLE

The visual theme should communicate:

> **HIGH ALTITUDE. HARSH ENVIRONMENT. MEASURABLE PHYSICS. PREDICTIVE ENGINEERING. AUTONOMOUS PROTECTION.**

The UI should feel:

**Precise. Calm. Scientific. Reliable. Mission-critical.**

Not flashy.

Not gimmicky.

Not "AI-looking."

Build the simulation so that the **engineering itself is the visual hero.**

</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-09-21T13:37:49+05:30.

The user's current state is as follows:
Browser State:
  Page 8B9E51454AF26187D5971A78D5662755 (HIMVAJRA — High-Altitude Electronics Reliability Simulator) - file:///C:/Users/Harsh/Desktop/SIH%20simulation/index.html [ACTIVE]
    Viewport: 1536x730, Page Height: 2251
</ADDITIONAL_METADATA>