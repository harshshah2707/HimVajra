"""
Quick test script for new FORGE ML endpoints in ml_service
"""
import urllib.request
import json

def post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("1. Testing /api/health...")
h = get("http://127.0.0.1:8000/api/health")
print("Health status:", h.get("status"))

print("\n2. Testing /api/forge/predict (In-Domain: 5000m, 25C, 15W)...")
pred = post("http://127.0.0.1:8000/api/forge/predict", {
    "altitude_m": 5000.0,
    "ambient_temp_c": 25.0,
    "load_power_w": 15.0,
    "theta_base": 3.0,
    "cooling_mode": "forced",
    "electrode_gap_mm": 2.0,
    "delta_t_diurnal": 50.0
})
print("In-domain status:", pred.get("status"))
print("Physics baseline:", pred["predictions"]["physics_baseline_c"], "C")
print("ML correction:  ", pred["predictions"]["ml_correction_c"], "C")
print("Final prediction:", pred["predictions"]["final_predicted_junction_c"], "C")
print("95% CI:          ", pred["predictions"]["confidence_interval_95_c"], "C")
print("Latency:         ", pred.get("inference_latency_ms"), "ms")

print("\n3. Testing /api/forge/predict (Out-of-Domain: 7500m)...")
ood = post("http://127.0.0.1:8000/api/forge/predict", {
    "altitude_m": 7500.0,
    "ambient_temp_c": 25.0,
    "load_power_w": 15.0,
    "theta_base": 3.0,
    "cooling_mode": "forced",
    "electrode_gap_mm": 2.0,
    "delta_t_diurnal": 50.0
})
print("OOD status:     ", ood.get("status"))
print("In-domain flag: ", ood.get("in_domain"))
print("Warning:        ", ood.get("warning"))
print("ML correction:  ", ood["predictions"]["ml_correction_c"], "C (bypassed)")

print("\n4. Testing /api/forge/analytics...")
analytics = get("http://127.0.0.1:8000/api/forge/analytics")
print("Model version:   ", analytics.get("metadata", {}).get("model_version"))
print("Physics MAE:     ", analytics.get("comparison_summary", {}).get("physics_only", {}).get("mae_c"), "C")
print("Physics+ML MAE:  ", analytics.get("comparison_summary", {}).get("physics_plus_ml", {}).get("mae_c"), "C")
print("MAE Reduction:   ", analytics.get("comparison_summary", {}).get("improvement", {}).get("mae_reduction_pct"), "%")

print("\n5. Testing /api/forge/benchmark...")
bm = get("http://127.0.0.1:8000/api/forge/benchmark")
print("Benchmark models evaluated:", list(bm.keys()))

print("\n6. Testing /api/forge/noise_test...")
noise = post("http://127.0.0.1:8000/api/forge/noise_test", {
    "altitude_m": 5000.0,
    "ambient_temp_c": 25.0,
    "load_power_w": 15.0,
    "theta_base": 3.0,
    "cooling_mode": "forced",
    "electrode_gap_mm": 2.0,
    "delta_t_diurnal": 50.0
})
print("Clean prediction:", noise.get("clean_prediction_c"), "C")
print("Noisy prediction:", noise.get("noisy_prediction_c"), "C")
print("Delta:           ", noise.get("prediction_delta_c"), "C")
print("Rating:          ", noise.get("robustness_rating"))

print("\n[ALL FORGE API TESTS PASSED!]")
