import urllib.request
import json

payload = json.dumps({
    'altitude_m': 5000.0,
    'temp_c': -25.0,
    'battery_soh_pct': 80.0,
    'payload_kg': 2.0,
    'current_load_a': 12.0
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:8000/api/predict/ladakh_mode', data=payload, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print("=" * 65)
    print("HIMVAJRA ML INFERENCE — AKSHA_SIH 26.PDF TEST CASE VALIDATION")
    print("=" * 65)
    inp = res['inputs']
    phys = res['environmental_physics']
    pred = res['predictions']
    ml = res['ml_pipeline_info']
    
    print(f"Inputs:\n  Altitude: {inp['altitude_m']:,.0f} m\n  Ambient Temperature: {inp['temp_c']} °C\n  Battery SOH: {inp['battery_soh_pct']:.1f} %\n  Operational Load: {inp['current_load_a']} A\n  Payload: {inp['payload_kg']} kg")
    print("-" * 65)
    print(f"Physics Engine:\n  Tropospheric Pressure: {phys['pressure_kpa']} kPa\n  Air Density: {phys['air_density_kg_m3']} kg/m³ ({phys['density_ratio']} rho_0)\n  Convection Cooling Derate: +{phys['convective_cooling_derating_pct']}%")
    print("-" * 65)
    print(f"Machine Learning Predictions:\n  Flight Endurance: {pred['flight_endurance_min']} min (Sea-Level: {pred['flight_endurance_sea_level_min']} min, Loss: -{pred['endurance_loss_pct']}%)\n  95% Confidence Band: [{pred['confidence_interval_95_min'][0]} – {pred['confidence_interval_95_min'][1]}] min\n  Usable Battery Capacity: {pred['usable_capacity_pct']}% (Arrhenius internal impedance drop)\n  Environmental Stress: {pred['environmental_stress']} (Risk Score: {pred['risk_score']}/100)\n  Recommendation Class: {pred['recommendation']}\n  Recommended Action: {pred['recommended_action']}\n  Hotspot Thermal Rise (GPR): +{pred['predicted_hotspot_rise_c']} °C (Band: {pred['hotspot_confidence_band_c']} °C)")
    print("-" * 65)
    print(f"Pipeline Info:\n  Model: {ml['model_type']}\n  Datasets: {ml['training_datasets']}\n  Inference Latency: {ml['inference_latency_ms']} ms")
    print("=" * 65)
