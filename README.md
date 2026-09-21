# HIMVAJRA — High-Altitude Reliability & Prognostics Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

**HIMVAJRA** is an aerospace and defense-grade engineering simulation, prognostics, and fleet monitoring platform designed for high-altitude UAV electronics and energy storage systems operating under extreme sub-zero, rarefied atmosphere conditions (e.g., Ladakh / Siachen sectors).

---

## Key Capabilities

- **Physics-Based Environmental Simulation**:
  - ISA Barometric pressure and density altitude computation.
  - Convective thermal dissipation penalties and component hotspot temperature prediction.
  - Paschen's Law electrical breakdown & partial discharge clearance derating.
  - Battery capacity shrinkage and electrochemical internal resistance scaling under sub-zero temperatures.

- **Dual-Domain Machine Learning Prognostics**:
  - **AMOVFLY UAV High-Altitude Telemetry**: Flight endurance estimation and operational risk classification.
  - **NASA PCoE Battery Aging Dataset**: Remaining Useful Life (RUL) estimation with Gaussian Process Regression (GPR) confidence intervals.
  - Autonomous "Ladakh Mode" switching and GUARD state transitions.

- **Interactive Engineering Dashboard**:
  - Built with clean, scientific instrumentation aesthetics (HTML5, Vanilla CSS, Vanilla JS).
  - Real-time thermal gradient visualizations, state machine monitoring, fault injection, and telemetry replays.

- **FastAPI ML Microservice**:
  - High-throughput REST API serving live inferences and telemetry evaluation to web dashboards and edge controllers.

---

## System Architecture

```text
CONTROLLED VALIDATION
        ↓
PHYSICS-BASED PREDICTION (ISA + Thermal + Electrochemical)
        ↓
THERMAL & ELECTRICAL RISK ANALYSIS
        ↓
EMBEDDED PROTECTION (GUARD State Machine)
        ↓
FIELD TELEMETRY & EDGE LOGGING
        ↓
FLEET MONITORING & PROGNOSTICS (NASA + AMOVFLY ML Models)
        ↓
MAINTENANCE & MISSION DISPATCH DECISION
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10 or later
- Modern Web Browser (Chrome / Edge / Firefox)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/harshshah2707/HimVajra.git
cd HimVajra

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the ML Inference Microservice
```bash
python ml_service.py
# Or with uvicorn directly:
uvicorn ml_service:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be available at: `http://127.0.0.1:8000/docs`

### 4. Launch the Web Simulation Dashboard
Open `index.html` directly in your browser or serve using Python:
```bash
python -m http.server 3000
```
Then navigate to `http://localhost:3000`.

---

## Repository Structure

```
HimVajra/
├── data/
│   ├── amovfly_uav_high_altitude_dataset.csv  # AMOVFLY UAV telemetry
│   └── nasa_battery_pcoe_dataset.csv          # NASA PCoE battery aging data
├── models/
│   ├── flight_endurance_model.joblib          # Trained endurance estimator
│   ├── nasa_battery_rul_model.joblib          # NASA RUL model
│   ├── recommendation_model.joblib            # Operational mode classifier
│   ├── thermal_gpr_model.joblib               # Gaussian Process thermal model
│   ├── usable_capacity_model.joblib           # Cold-temperature capacity model
│   ├── model_metrics.json                     # Training benchmark scores
│   └── scaler.joblib / gp_scaler.joblib       # Feature transformers
├── index.html                                 # Engineering dashboard UI
├── style.css                                  # Scientific/aerospace instrumentation theme
├── app.js                                     # Real-time simulation & state engine
├── ml_service.py                              # FastAPI prognostics backend
├── train_models.py                            # Model training & evaluation pipeline
├── test_ml_api.py                             # Automated API verification test suite
├── generate_deck.py / update_ppt.py           # Presentation automation scripts
├── HIMVAJRA.pptx                              # Project presentation deck
├── requirements.txt                           # Project dependencies
└── README.md                                  # Platform overview & quickstart
```

---

## License

Developed for high-altitude UAV electronics reliability and prognostics. Released under the MIT License.
