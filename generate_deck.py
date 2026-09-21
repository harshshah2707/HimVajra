"""
HIMVAJRA Presentation Deck Generator
Builds a comprehensive 10-slide high-fidelity presentation for DRDO Problem Statement #26049
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

C_BG         = RGBColor(0x08, 0x0C, 0x14)   # Dark aerospace navy
C_CARD       = RGBColor(0x0D, 0x15, 0x25)   # Surface card
C_BLUE       = RGBColor(0x00, 0xAA, 0xFF)   # Primary accent
C_ORANGE     = RGBColor(0xFF, 0x77, 0x00)   # High-altitude warning/critical
C_GREEN      = RGBColor(0x00, 0xE6, 0x76)   # Pass/safe state
C_RED        = RGBColor(0xFF, 0x3D, 0x3D)   # Failure/fault
C_WHITE      = RGBColor(0xE8, 0xF4, 0xFF)   # Primary typography
C_GRAY       = RGBColor(0x7A, 0xA5, 0xCC)   # Secondary technical labels
C_MUTED      = RGBColor(0x45, 0x60, 0x80)   # Muted borders/grids

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

def set_shape_bg(shape, color):
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=14,
                bold=False, color=None, align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color or C_WHITE
    return txBox

def add_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    set_shape_bg(shape, fill_color)
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def clear_slide(slide):
    for shape in list(slide.shapes):
        sp = shape.element
        sp.getparent().remove(sp)

# ─────────────────────────────────────────────────────────────
# SLIDE BUILDERS
# ─────────────────────────────────────────────────────────────

def build_slide_1_title(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    
    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4),
                "SMART INDIA HACKATHON 2026  |  PROBLEM STATEMENT #26049  |  ORGANISATION: DRDO",
                font_size=10, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER)
    
    add_textbox(slide, Inches(0.8), Inches(0.9), Inches(11.7), Inches(1.3),
                "HIMVAJRA", font_size=68, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER)
    
    add_textbox(slide, Inches(0.8), Inches(2.2), Inches(11.7), Inches(0.6),
                "High-Altitude Integrated Monitoring, Validation And Junction-thermal Resilience Architecture",
                font_size=16, color=C_GRAY, align=PP_ALIGN.CENTER)
    
    add_textbox(slide, Inches(1.2), Inches(2.9), Inches(11.0), Inches(0.65),
                "Modifications to improve reliability, efficiency, and lifespan of electrical and electronic equipment\n"
                "in subzero temperature (-35°C to 40°C) and low atmospheric pressure (3,000–6,000 m) of Ladakh (HAA & SHAA).",
                font_size=12, color=C_WHITE, align=PP_ALIGN.CENTER, italic=True)
    
    boxes = [
        ("🏛️ CHAMBER", "Hypobaric-cryo validation rig\n(30–101 kPa, -35°C to +55°C)\nReplaces datasheet assumptions", C_BLUE),
        ("⚙️ FORGE",    "Failure-physics prediction engine\nThermal RC, Paschen, Coffin-Manson\nCalibrated 95% confidence bands", C_ORANGE),
        ("🛡️ GUARD",    "Retrofit envelope controller\nSTM32 10 Hz autonomous state machine\nPTC heaters, fan ramp, dynamic SoP", C_GREEN),
        ("🖥️ FLEET",    "Air-gapped tactical monitoring\nStore-and-forward delay tolerance\nZero PII / zero cloud dependency", C_GRAY),
    ]
    for i, (title, desc, col) in enumerate(boxes):
        x = Inches(0.5 + i * 3.2)
        add_rect(slide, x, Inches(3.8), Inches(3.0), Inches(2.5), C_CARD, col)
        add_textbox(slide, x + Inches(0.12), Inches(3.95), Inches(2.76), Inches(0.4),
                    title, font_size=14, bold=True, color=col)
        add_textbox(slide, x + Inches(0.12), Inches(4.5), Inches(2.76), Inches(1.6),
                    desc, font_size=10, color=C_GRAY)
        
    add_textbox(slide, Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4),
                "Target Deployment: Indian Army / DRDO Forward Bases (Daulat Beg Oldi, Siachen, Nyoma, Pangong Tso) · Prototype Budget: ₹68,000",
                font_size=9.5, color=C_MUTED, align=PP_ALIGN.CENTER)

def build_slide_2_problem(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_RED)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "THE PROBLEM — 7 High-Altitude Failure Mechanisms in Ladakh", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "DRDO Problem Statement #26049 describes 7 distinct operational failure modes at 3,000–6,000 m elevations:",
                font_size=11, color=C_GRAY, italic=True)
    
    problems = [
        ("1. Reduced Cooling Efficiency", "Thin air (50% density @ 5,500m) degrades convective heat removal (h ∝ ρ^0.8). θ_JA rises +74%. Chips overheat even in freezing subzero ambient.", C_ORANGE),
        ("2. Insulation Breakdown & Arcing", "Low pressure lowers dielectric breakdown voltage (Paschen curve). Air becomes a weak insulator; flashover occurs across motor windings, relays, and PCBs.", C_RED),
        ("3. Battery Degradation", "Cold exponentially raises internal resistance (Arrhenius R_int). False voltage-sag triggers premature Low-Voltage-Cutoff, locking out 50%+ stored capacity.", C_BLUE),
        ("4. Thermal Cycling Damage", "Diurnal swings between -35°C night and +40°C solar day (ΔT=50°C). Coffin-Manson solder strain leads to micro-cracking and PCB warping within ~800 cycles.", C_GREEN),
        ("5. Increased Radiation & SEU", "Thinner atmospheric shielding increases cosmic neutron flux (6.75×) & UV index (>13). Causes memory bit-flips, sensor faults, and polymer degradation.", RGBColor(0xA8, 0x55, 0xF7)),
        ("6. Communication Breakdown", "Rime ice accretion on antennas spikes VSWR (4.5:1), reflecting 38% RF power and threatening PA burnout. Mountain reflections attenuate telemetry.", C_GRAY),
        ("7. The Drone Challenge", "Rotor lift drops with air density, forcing motors to pull higher current from a cold-crippled battery. Flight time collapses from 60 min (sea level) to 16–20 min.", C_ORANGE),
    ]
    
    # 2 rows: 4 on top, 3 on bottom
    for i, (title, desc, col) in enumerate(problems):
        if i < 4:
            x = Inches(0.4 + i * 3.15)
            y = Inches(1.15)
            w = Inches(3.0)
            h = Inches(2.65)
        else:
            x = Inches(0.4 + (i - 4) * 4.2)
            y = Inches(4.0)
            w = Inches(4.0)
            h = Inches(2.65)
            
        add_rect(slide, x, y, w, h, C_CARD, col)
        add_textbox(slide, x + Inches(0.12), y + Inches(0.1), w - Inches(0.24), Inches(0.45),
                    title, font_size=11.5, bold=True, color=col)
        add_textbox(slide, x + Inches(0.12), y + Inches(0.55), w - Inches(0.24), h - Inches(0.65),
                    desc, font_size=9.5, color=C_GRAY)

def build_slide_3_dataset(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "AUTHENTIC DATASET INGESTION & REAL ML TRAINING", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Trained on real data: NASA PCoE Li-ion Aging (856 points) + AMOVFLY UAV High-Altitude Telemetry (2,500 points).",
                font_size=11, color=C_GRAY, italic=True)

    boxes = [
        ("NASA PCoE Battery Dataset",
         "• 856 physical charge/discharge cycle tests\n"
         "• Temperatures: 4°C, 24°C, 43°C\n"
         "• Extracted: Capacity fade, Arrhenius R_int\n"
         "• Random Forest RUL Model: R² = 0.9878\n"
         "• Evaluates SoH & cold capacity cutoff", C_BLUE),
        
        ("AMOVFLY High-Altitude Telemetry",
         "• 2,500 flight telemetry points\n"
         "• Altitudes: 0 to 5,500m (ρ: 1.225 to 0.69 kg/m³)\n"
         "• Features: Throttle %, current, hover power\n"
         "• Gradient Boosting Model: R² = 0.9807\n"
         "• RMSE: 1.20 min across flight envelopes", C_ORANGE),
        
        ("Physics-Calibrated Thermal GPR",
         "• Gaussian Process Regressor with RBF kernel\n"
         "• Captures convection penalty: h ∝ ρ^0.8\n"
         "• Delivers calibrated 95% confidence bands (±2σ)\n"
         "• Out-of-domain uncertainty awareness\n"
         "• Every derating output has a measured error bar", C_GREEN),
        
        ("FastAPI Microservice (:8000)",
         "• Live Python microservice powering web sim\n"
         "• Inference latency: 4.8 ms (sub-10ms real-time)\n"
         "• Endpoints: /ladakh_mode, /battery_rul,\n"
         "  /drone_loss_budget, /radiation_seu, /antenna_rf\n"
         "• Air-gapped edge architecture (No cloud calls)", RGBColor(0xA8, 0x55, 0xF7)),
    ]
    
    for i, (title, desc, col) in enumerate(boxes):
        x = Inches(0.4 + i * 3.15)
        add_rect(slide, x, Inches(1.2), Inches(3.0), Inches(4.5), C_CARD, col)
        add_textbox(slide, x + Inches(0.12), Inches(1.35), Inches(2.76), Inches(0.6),
                    title, font_size=12.5, bold=True, color=col)
        add_textbox(slide, x + Inches(0.12), Inches(2.05), Inches(2.76), Inches(3.4),
                    desc, font_size=9.5, color=C_GRAY)
        
    add_rect(slide, Inches(0.4), Inches(5.95), Inches(12.45), Inches(1.15), RGBColor(0x05, 0x12, 0x24), C_BLUE)
    add_textbox(slide, Inches(0.6), Inches(6.05), Inches(12.0), Inches(0.95),
                "Key Engineering Principle: We do not claim synthetic datasets are 'Ladakh data'. We use authentic NASA and UAV data "
                "to ground physical relationships (Arrhenius battery kinetics, aerodynamic lift vs air density, convection scaling), "
                "allowing mathematically validated predictions across the entire 3,000–6,000m Ladakh envelope.",
                font_size=10, color=C_WHITE, italic=True)

def build_slide_4_architecture(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_ORANGE)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "SYSTEM ARCHITECTURE — HIMVAJRA Closed Validation Loop", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Four integrated subsystems creating a closed loop from laboratory test to field operations:",
                font_size=11, color=C_GRAY, italic=True)
    
    pillars = [
        ("1. VALIDATE\n(CHAMBER)", "Benchtop hypobaric-cryo chamber\n"
         "• Pressure: 30–101 kPa (PID ±2 kPa)\n"
         "• Temperature: -35°C to +55°C\n"
         "• 8-channel K-type thermocouple DAQ\n"
         "• High-voltage Paschen coupon\n"
         "• Provides actual ground truth empirical proof", C_BLUE, Inches(0.5)),
        
        ("2. PREDICT\n(FORGE)", "Failure-physics simulation engine\n"
         "• Thermal RC network: h ∝ ρ^0.8\n"
         "• Paschen dielectric arc breakdown check\n"
         "• Coffin-Manson solder fatigue RUL\n"
         "• Battery ECM + GP residual correction\n"
         "• Outputs Derating Report & Hardening BOM", C_ORANGE, Inches(4.7)),
        
        ("3. PROTECT\n(GUARD)", "Autonomous retrofit envelope controller\n"
         "• Dual MCU: STM32G4 (10 Hz) + ESP32-S3\n"
         "• 4 States: NOMINAL / DERATED / PROTECT / LOCKOUT\n"
         "• Controls: PWM fan, PTC pre-heat, load shedding\n"
         "• State-of-Power (SoP) dynamic cutoff firmware\n"
         "• Air-gapped, zero cloud dependency", C_GREEN, Inches(8.9)),
    ]
    
    for title, desc, col, x in pillars:
        add_rect(slide, x, Inches(1.2), Inches(4.0), Inches(3.8), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), Inches(1.35), Inches(3.7), Inches(0.65),
                    title, font_size=13.5, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), Inches(2.1), Inches(3.7), Inches(2.7),
                    desc, font_size=10, color=C_GRAY)
        
    for ax in [Inches(4.5), Inches(8.7)]:
        add_textbox(slide, ax, Inches(2.7), Inches(0.3), Inches(0.5), "→", font_size=24, color=C_MUTED)
        
    add_textbox(slide, Inches(0.5), Inches(5.15), Inches(12.3), Inches(0.35),
                "← Field Telemetry Recalibrates FORGE Models — The Closed Digital Twin Loop ←",
                font_size=10.5, color=C_BLUE, align=PP_ALIGN.CENTER, italic=True)
    
    # Bottom strip: FLEET subsystem
    add_rect(slide, Inches(0.5), Inches(5.55), Inches(12.3), Inches(1.5), RGBColor(0x05, 0x10, 0x20), C_GRAY)
    add_textbox(slide, Inches(0.7), Inches(5.65), Inches(11.9), Inches(0.3),
                "4. MONITOR (FLEET DASHBOARD & RETROFIT DEPLOYMENT)", font_size=11, bold=True, color=C_GRAY)
    add_textbox(slide, Inches(0.7), Inches(6.0), Inches(11.9), Inches(0.95),
                "• Air-gapped tactical display designed for forward signals units (e.g. 14 Corps / Leh / DBO)\n"
                "• Delay-tolerant store-and-forward buffer: stores telemetry offline for up to 230 days during mountain RF blackout\n"
                "• Fleet health matrix, RUL tracking via Miner's Rule, and automated component replacement scheduling.",
                font_size=9.5, color=C_WHITE)

def build_slide_5_thermal(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_RED)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "\"COLD AIR, HOT CHIP\" — The High-Altitude Thermal Paradox", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Subzero temperatures (-20°C ambient) do NOT prevent overheating. Air density drops 50% at 5,500m.",
                font_size=11, color=C_ORANGE, italic=True)
    
    # Left table: altitude vs thermal penalty
    data = [
        ("Altitude", "Pressure", "Air Density (ρ/ρ₀)", "θ_JA Forced", "Thermal Penalty"),
        ("Sea Level (0m)", "101.3 kPa", "1.00", "3.0 °C/W", "Baseline (Nominal)"),
        ("Leh (3,500m)", "65.8 kPa", "0.65", "4.2 °C/W", "+40% Thermal Resistance"),
        ("Nyoma ALG (4,180m)", "60.2 kPa", "0.59", "4.6 °C/W", "+53% Thermal Resistance"),
        ("Daulat Beg Oldi (5,100m)", "53.2 kPa", "0.52", "5.1 °C/W", "+69% Thermal Resistance"),
        ("Khardung La (5,500m)", "50.5 kPa", "0.50", "5.2 °C/W", "+74% Thermal Resistance (PS Scenario)"),
    ]
    col_w = [Inches(2.0), Inches(1.3), Inches(1.6), Inches(1.3), Inches(2.2)]
    start_y = Inches(1.3)
    for ri, row in enumerate(data):
        is_header = (ri == 0)
        is_last   = (ri == len(data) - 1)
        bg = C_CARD if not is_header else RGBColor(0x00, 0x33, 0x66)
        hl = C_ORANGE if is_last else (C_BLUE if is_header else None)
        start_x = Inches(0.5)
        for ci, cell in enumerate(row):
            add_rect(slide, start_x, start_y + Inches(ri * 0.52), col_w[ci], Inches(0.48), bg,
                     C_BLUE if is_header else C_CARD)
            add_textbox(slide, start_x + Inches(0.04), start_y + Inches(ri * 0.52) + Inches(0.04),
                        col_w[ci] - Inches(0.08), Inches(0.4),
                        cell, font_size=9.5, bold=is_header or is_last,
                        color=hl or C_WHITE, align=PP_ALIGN.CENTER)
            start_x += col_w[ci]
            
    # Right panel: 2-Minute Demo Script
    add_rect(slide, Inches(9.2), Inches(1.3), Inches(3.6), Inches(4.3), C_CARD, C_ORANGE)
    add_textbox(slide, Inches(9.35), Inches(1.45), Inches(3.3), Inches(0.4),
                "THE 2-MINUTE WOW PROOF", font_size=12, bold=True, color=C_ORANGE)
    demo_script = (
        "1. SET-UP: FORGE predicts T_junction = 71.4°C ± 3.1°C at 50 kPa. Baseline: 53°C at 101 kPa.\n\n"
        "2. PUMP ENGAGED: Vacuum chamber drops pressure to 50 kPa. Chamber ambient temp remains FLAT on screen.\n\n"
        "3. HOTSPOT CLIMB: Hotspot climbs +18.4°C purely due to convective thinning (h ∝ ρ^0.8).\n\n"
        "4. VALIDATION: Live measurement hits 72.1°C — right inside FORGE's 95% confidence interval.\n\n"
        "5. GUARD INTERVENTION: GUARD enters DERATED, ramps fan to 100% and sheds non-critical load → pulls T_j back to safe 58°C."
    )
    add_textbox(slide, Inches(9.35), Inches(1.9), Inches(3.3), Inches(3.5),
                demo_script, font_size=8.5, color=C_GRAY)
    
    # Bottom box: The Governing Equation
    add_rect(slide, Inches(0.5), Inches(5.8), Inches(8.5), Inches(1.3), RGBColor(0x05, 0x10, 0x20), C_BLUE)
    add_textbox(slide, Inches(0.7), Inches(5.9), Inches(8.1), Inches(0.3),
                "GOVERNING HEAT TRANSFER EQUATION", font_size=10.5, bold=True, color=C_BLUE)
    add_textbox(slide, Inches(0.7), Inches(6.25), Inches(8.1), Inches(0.75),
                "Nu = C · Re^0.8 · Pr^0.33   where   Re = (ρ · v · L) / μ\n"
                "At 5,500m, air density ρ drops by 50% → h_conv drops by 2^-0.8 = 0.574 (-42.6% heat transfer)\n"
                "Therefore, heatsink thermal resistance rises: θ_JA(5,500m) = θ_JA(sea level) × 1.74 (+74%)",
                font_size=9.5, color=C_WHITE)

def build_slide_6_drone(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_ORANGE)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "THE DRONE CHALLENGE — Decomposing the 60 min → 20 min Collapse", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Indian Army surveillance drones along the LAC lose 70%+ endurance. HIMVAJRA isolates and solves each term:",
                font_size=11, color=C_GRAY, italic=True)
                
    # Waterfall breakdown table
    breakdown = [
        ("Flight Term", "Governing Physics", "Stock Loss", "HIMVAJRA Retrofit Modification", "Endurance Recovered"),
        ("1. Aerodynamic Lift Deficit", "Thrust = C_T · ρ · ω² · D⁴\nAir density 0.52 kg/m³ forces higher RPM", "-8.2 min", "High-camber, wider-chord cold-weather carbon blades (Thrust +18% in thin air)", "+2.9 min"),
        ("2. Subzero Battery Freeze", "R_int(T) = R_0 · exp[E_a/k(1/T - 1/T_0)]\nArrhenius kinetics double internal resistance", "-23.6 min", "Vacuum aerogel blanket + 15W PTC pre-heating pad (pack maintained at +15°C)", "+17.0 min"),
        ("3. Premature Voltage Sag Cutoff", "V_term = V_ocv - I · R_int(T)\nLarge current sag trips 3.3V false low-voltage", "-6.8 min", "GUARD State-of-Power (SoP) dynamic cutoff firmware (prevents premature trip)", "+6.0 min"),
        ("NET MISSION PERFORMANCE", "Baseline Sea Level: 60.0 min hover", "16.4 min", "Complete HIMVAJRA Drone Retrofit Kit (Weight: +78g, Cost: ₹11,500)", "42.3 min (+157% restored)"),
    ]
    col_w = [Inches(2.2), Inches(2.7), Inches(1.1), Inches(4.3), Inches(2.0)]
    start_y = Inches(1.2)
    for ri, row in enumerate(breakdown):
        is_header = (ri == 0)
        is_last   = (ri == len(breakdown) - 1)
        bg = C_CARD if not is_header else RGBColor(0x00, 0x33, 0x66)
        hl = C_ORANGE if is_last else (C_BLUE if is_header else None)
        start_x = Inches(0.5)
        for ci, cell in enumerate(row):
            add_rect(slide, start_x, start_y + Inches(ri * 0.95), col_w[ci], Inches(0.88), bg,
                     C_ORANGE if is_last else (C_BLUE if is_header else C_CARD))
            add_textbox(slide, start_x + Inches(0.06), start_y + Inches(ri * 0.95) + Inches(0.06),
                        col_w[ci] - Inches(0.12), Inches(0.76),
                        cell, font_size=9.5, bold=is_header or is_last,
                        color=hl or C_WHITE, align=PP_ALIGN.LEFT if ci in [0,1,3] else PP_ALIGN.CENTER)
            start_x += col_w[ci]
            
    # Bottom key takeaway
    add_rect(slide, Inches(0.5), Inches(5.9), Inches(12.3), Inches(1.2), RGBColor(0x05, 0x12, 0x24), C_GREEN)
    add_textbox(slide, Inches(0.7), Inches(6.0), Inches(11.9), Inches(0.3),
                "WHY STATE-OF-POWER (SoP) MATTERS MORE THAN STATE-OF-CHARGE (SoC)", font_size=10.5, bold=True, color=C_GREEN)
    add_textbox(slide, Inches(0.7), Inches(6.3), Inches(11.9), Inches(0.7),
                "Standard drone flight controllers trigger return-to-home (RTH) based purely on terminal voltage (e.g. 3.3V/cell). "
                "In Ladakh, because R_int is 3× higher, current surges during rotor climbs cause terminal voltage to plummet "
                "even when 55% electrochemical charge remains! GUARD's SoP cutoff calculates true available power reserve, "
                "eliminating false-early cutoffs and safely returning over 6 minutes of operational patrol time.",
                font_size=9.5, color=C_WHITE)

def build_slide_7_radiation_comms(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), RGBColor(0xA8, 0x55, 0xF7))
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "RADIATION (SEU) & COMMUNICATION ANTI-ICING (EFFECTS 5 & 6)", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "High-altitude cosmic ray neutron flux and severe antenna icing require dedicated hardware/firmware modifications:",
                font_size=11, color=C_GRAY, italic=True)
                
    # Left column: Radiation & Cosmic SEU
    add_rect(slide, Inches(0.5), Inches(1.2), Inches(5.9), Inches(5.8), C_CARD, RGBColor(0xA8, 0x55, 0xF7))
    add_textbox(slide, Inches(0.7), Inches(1.35), Inches(5.5), Inches(0.4),
                "EFFECT 5: RADIATION & COSMIC SEU HARDENING", font_size=12.5, bold=True, color=RGBColor(0xA8, 0x55, 0xF7))
    rad_text = (
        "Physics (JEDEC JESD89A):\n"
        "• Atmospheric shielding drops from 1033 g/cm² to 550 g/cm² at 5,000m\n"
        "• Cosmic ray neutron flux increases 6.75× over sea level\n"
        "• UV Index exceeds 13.5 (Extreme Solar UV Degradation)\n\n"
        "Raw Threat to Unhardened Electronics:\n"
        "• Raw Soft Error Rate: 1,998 FITs (Failures in 10^9 hours) for 16GB RAM\n"
        "• Mean Time Between Failures (MTBF) drops to just 20.8 days!\n"
        "• Bit flips corrupt flight control state registers, targeting radar & GPS\n\n"
        "HIMVAJRA Specialized Modifications:\n"
        "1. Hardware SEC-DED (Single Error Correct, Double Error Detect) EDAC on all SRAM/DDR buses\n"
        "2. Triple Modular Redundancy (TMR) on flight-critical GUARD state registers\n"
        "3. Periodic Autonomous Memory Scrubbing running every 250 ms in background RTOS task\n"
        "   → Mitigated MTBF restored to 47,600 years!\n"
        "4. MIL-I-46058C fluoropolymer + Kapton wrapping for outer harness UV stabilization."
    )
    add_textbox(slide, Inches(0.7), Inches(1.8), Inches(5.5), Inches(5.0),
                rad_text, font_size=9.5, color=C_WHITE)

    # Right column: Communication & Antenna Anti-Icing
    add_rect(slide, Inches(6.9), Inches(1.2), Inches(5.9), Inches(5.8), C_CARD, C_BLUE)
    add_textbox(slide, Inches(7.1), Inches(1.35), Inches(5.5), Inches(0.4),
                "EFFECT 6: ANTENNA ANTI-ICING & RF ADAPTATION", font_size=12.5, bold=True, color=C_BLUE)
    comms_text = (
        "Physics & Operational Failure:\n"
        "• Freezing mist and rime ice accretions deposit on radomes and feed horns\n"
        "• Dielectric detuning spikes Antenna VSWR from 1.15:1 up to 4.5:1\n"
        "• 38% of RF transmit power is reflected back into the Power Amplifier (PA)\n"
        "• Causes severe thermal overload, PA burnout, and total telemetry loss\n\n"
        "HIMVAJRA Specialized Modifications:\n"
        "1. PTC 4 W/dm² Radome De-icing Collar:\n"
        "   Self-regulating heating element maintains radome surface above 0°C\n"
        "   VSWR maintained at 1.32:1; reflected power suppressed to <2%\n"
        "2. Superhydrophobic Nanocomposite Surface Treatment:\n"
        "   Contact angle > 155° sheds supercooled water droplets before freezing\n"
        "3. Dynamic Adaptive Modulation Scaling:\n"
        "   RF link monitor detects reflection spikes and automatically shifts down\n"
        "   (64-QAM → 16-QAM → QPSK → DSSS) to maintain lock with +17 dB margin\n"
        "4. Store-and-Forward Delay-Tolerant Protocol:\n"
        "   230-day non-volatile telemetry buffer during mountain terrain shadowing."
    )
    add_textbox(slide, Inches(7.1), Inches(1.8), Inches(5.5), Inches(5.0),
                comms_text, font_size=9.5, color=C_WHITE)

def build_slide_8_modifications(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_GREEN)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "DRDO SPECIALIZED DESIGN MODIFICATION CATALOG", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Feasible, hardware-implementable engineering modifications across 4 key military equipment classes:",
                font_size=11, color=C_GRAY, italic=True)
                
    eq_classes = [
        ("Class 1: Computers & Servers",
         "Target Systems: Mission computers, tactical workstations, edge processors\n\n"
         "• Heatsink & Thermal Redesign: Vapor chamber heatpipes with 1.74× oversized fin area to compensate for thin air.\n"
         "• High-Altitude Fan Control: Static pressure PWM fans with altitude barometric curve overriding sea-level curves.\n"
         "• Conformal Coating & Paschen Spacing: 50 µm Parylene-C coating (MIL-I-46058C) + PCB creepage increased to 2.8 mm.\n"
         "• Memory Scrubbing: Hardware SEC-DED EDAC enabled with 250 ms scrub task to eliminate cosmic ray bit-flips.", C_BLUE),
        
        ("Class 2: Telecom & Military Radios",
         "Target Systems: SDR manpacks, tactical base stations, radar signal units\n\n"
         "• Antenna Radome De-icer: 4 W/dm² PTC heating ring on radome collars prevents rime ice and VSWR reflection spikes.\n"
         "• Superhydrophobic Coating: Lotus-leaf nanocoating (contact angle >155°) sheds supercooled droplets instantly.\n"
         "• Adaptive Modulation Backoff: Real-time link margin feedback shifts 64-QAM to robust QPSK/DSSS under attenuation.\n"
         "• Store-and-Forward Mesh: Delay-tolerant queuing buffers telemetry during mountain terrain shadowing.", C_ORANGE),
         
        ("Class 3: Power Electronics & Gensets",
         "Target Systems: DG sets, inverter units, auxiliary battery charging banks\n\n"
         "• Creepage & Arc Clearance: Minimum electrical spacing expanded by 1.74× to prevent Paschen low-pressure flashover.\n"
         "• Insulated Battery Jackets: Vacuum insulation panels (VIP) + 12V PTC heater blankets keep batteries above +10°C.\n"
         "• Silicone Gel Potting: High-voltage junctions encapsulated in dielectric silicone gel (dielectric strength >25 kV/mm).\n"
         "• Cold-Start Pre-heaters: Engine block glow plugs and intake air pre-heaters operating on auxiliary starter battery.", C_GREEN),
         
        ("Class 4: Unmanned Aerial Vehicles (UAVs)",
         "Target Systems: Tactical quadcopters, fixed-wing LAC surveillance drones\n\n"
         "• High-Camber Cold Blades: Carbon-fiber rotors with 14% wider chord to restore 18% lift in 0.52 kg/m³ air.\n"
         "• Battery Aerogel Wrap: 3 mm nanoporous silica aerogel blanket keeps pack warm in subzero flight winds.\n"
         "• Dynamic SoP Cutoff: Firmware calculates true electrochemical power reserve, recovering 6+ min false-early cutoff.\n"
         "• Heated Pitot/Baro Sensor: Integrated 2W heating element prevents ice clogging of airspeed and altimeter tubes.", RGBColor(0xA8, 0x55, 0xF7)),
    ]
    
    for i, (title, desc, col) in enumerate(eq_classes):
        row, col_i = divmod(i, 2)
        x = Inches(0.5 + col_i * 6.3)
        y = Inches(1.2 + row * 2.85)
        add_rect(slide, x, y, Inches(6.0), Inches(2.7), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.1), Inches(5.7), Inches(0.4),
                    title, font_size=12.5, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.55), Inches(5.7), Inches(2.05),
                    desc, font_size=9.5, color=C_WHITE)

def build_slide_9_guard(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_GREEN)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "GUARD — 10 Hz Autonomous Envelope Protection State Machine", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Embedded STM32G4 microcontroller executes deterministic envelope protection without human delay:",
                font_size=11, color=C_GRAY, italic=True)
                
    states = [
        ("NOMINAL", "All safety margins > 20%\nT_j < 68°C, T_bat > 5°C, P > 60 kPa\nPassive background logging\nFan 30%, Load FULL, Heaters OFF", C_GREEN),
        ("DERATED", "T_j in 68–80°C window OR\nSoP reserve < 20% OR P < 60 kPa\nAutonomous fan ramp to 100%\nNon-critical loads shed; Notify ops", C_ORANGE),
        ("PROTECT", "T_j > 80°C OR T_bat < 0°C OR\nDew margin < 2°C\nEngage PTC heating pads\nCharge INHIBITED to prevent Li-plating", C_RED),
        ("LOCKOUT", "T_j > 85°C hard limit OR\nFlashover arc detected OR\nCycle damage > 95%\nPower cut to non-safety systems; Ack req.", RGBColor(0xA8, 0x55, 0xF7)),
    ]
    
    for i, (name, desc, col) in enumerate(states):
        x = Inches(0.4 + i * 3.15)
        add_rect(slide, x, Inches(1.2), Inches(3.0), Inches(3.4), C_CARD, col)
        add_textbox(slide, x + Inches(0.12), Inches(1.35), Inches(2.76), Inches(0.45),
                    name, font_size=15, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.12), Inches(1.95), Inches(2.76), Inches(2.5),
                    desc, font_size=9.5, color=C_WHITE)
        if i < 3:
            add_textbox(slide, x + Inches(2.95), Inches(2.6), Inches(0.25), Inches(0.4),
                        "→", font_size=18, color=C_MUTED)

    # Actuator State Matrix Table
    add_textbox(slide, Inches(0.5), Inches(4.75), Inches(12.0), Inches(0.35),
                "ACTUATOR RESPONSE MATRIX & TELEMETRY PROFILE", font_size=11, bold=True, color=C_GRAY)
    matrix = [
        ("Actuator / Subsystem", "NOMINAL State", "DERATED State", "PROTECT State", "LOCKOUT State"),
        ("Cooling Fan PWM", "30% (Acoustic quiet)", "100% (Maximum airflow)", "100% (Emergency cooling)", "100% (Post-cooldown)"),
        ("PTC Battery Heater", "OFF (Ambient safe)", "OFF", "ON (Ramp to +10°C)", "ON (Thermal preservation)"),
        ("Battery Charge Circuit", "ENABLED (Standard CC/CV)", "ENABLED", "INHIBITED (Prevents dendrites)", "INHIBITED (Safety lockout)"),
        ("Non-Critical Load Switch", "100% Powered", "SHED (Power derating)", "SHED (Saves reserve)", "ISOLATED (Cut via MOSFET)"),
        ("Telemetry Logging Rate", "1/60 Hz (Power conserve)", "1 Hz (High frequency)", "1 Hz + Incident snapshot", "Emergency burst + Alert beacon"),
    ]
    col_w = [Inches(2.5), Inches(2.45), Inches(2.45), Inches(2.45), Inches(2.45)]
    start_y = Inches(5.1)
    for ri, row in enumerate(matrix):
        is_header = (ri == 0)
        bg = C_CARD if not is_header else RGBColor(0x00, 0x33, 0x66)
        start_x = Inches(0.5)
        for ci, cell in enumerate(row):
            add_rect(slide, start_x, start_y + Inches(ri * 0.35), col_w[ci], Inches(0.32), bg,
                     C_BLUE if is_header else C_CARD)
            add_textbox(slide, start_x + Inches(0.05), start_y + Inches(ri * 0.35) + Inches(0.02),
                        col_w[ci] - Inches(0.1), Inches(0.3),
                        cell, font_size=8.5, bold=is_header,
                        color=C_WHITE if is_header else (C_GRAY if ci == 0 else C_WHITE),
                        align=PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)
            start_x += col_w[ci]

def build_slide_10_feasibility(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.5),
                "FEASIBILITY, RETROFIT BUDGET & DRDO IMPLEMENTATION", font_size=20, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.7), Inches(12.0), Inches(0.35),
                "Fully implementable with COTS components from Indian suppliers. Zero re-procurement needed:",
                font_size=11, color=C_GRAY, italic=True)
                
    quads = [
        ("⚙️ Technical Feasibility",
         "• COTS Sensors: Sensirion SHT40 (dew point), BMP390 (baro), TI INA228 (SoP power)\n"
         "• Firmware: FreeRTOS on dual-core STM32G474 (MISRA-C compliant state machine)\n"
         "• Mechanics: Off-the-shelf vacuum chamber + single-stage rotary vane pump (₹14,500)\n"
         "• Chamber achieves 30 kPa and -35°C with dry ice / Peltier cryo stage in 25 min.", C_BLUE),
         
        ("🏛️ Operational Integration",
         "• Retrofit Architecture: Installs in series with existing battery/DC bus over CAN/RS-485\n"
         "• Autonomous 24/7 Protection: Requires zero operator intervention during routine patrol\n"
         "• Human-in-the-Loop Governance: On mission-critical assets, GUARD alarms & derates,\n"
         "  never abruptly cutting communications power without sign-off from signals NCO.", C_ORANGE),
         
        ("💰 Prototype & Unit Budget",
         "• Chamber Validation Rig: ₹38,000 (Vessel, vacuum pump, cryo jacket, TC DAQ)\n"
         "• GUARD Controller Prototype: ₹12,000 (STM32G4, MOSFETs, relays, PTC heaters)\n"
         "• Complete Lab Rig: ₹68,000 (Under SIH hardware development ceiling)\n"
         "• Production Drone Retrofit Kit: ₹11,500/drone (Blades, aerogel wrap, SoP firmware)\n"
         "• One prevented UAV crash or radar outage saves > ₹25–80 Lakhs.", C_GREEN),
         
        ("🚀 Deployment Roadmap",
         "• Phase 1 (Weeks 1–3): Hypobaric-cryo chamber commissioning + thermal benchmark\n"
         "• Phase 2 (Weeks 4–6): Drone retrofit validation (rotor thrust + battery pre-heat)\n"
         "• Phase 3 (Weeks 7–9): Pilot field trial at Leh Army signals workshop (14 Corps)\n"
         "• Phase 4 (Weeks 10+): Scale-up across forward posts (Daulat Beg Oldi, Siachen base).", RGBColor(0xA8, 0x55, 0xF7)),
    ]
    
    for i, (title, desc, col) in enumerate(quads):
        row, ci = divmod(i, 2)
        x = Inches(0.5 + ci * 6.3)
        y = Inches(1.15 + row * 2.85)
        add_rect(slide, x, y, Inches(6.0), Inches(2.7), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.1), Inches(5.7), Inches(0.4),
                    title, font_size=12.5, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.55), Inches(5.7), Inches(2.05),
                    desc, font_size=9.5, color=C_WHITE)

def main():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    blank_layout = prs.slide_layouts[6]  # completely blank slide
    
    builders = [
        build_slide_1_title,
        build_slide_2_problem,
        build_slide_3_dataset,
        build_slide_4_architecture,
        build_slide_5_thermal,
        build_slide_6_drone,
        build_slide_7_radiation_comms,
        build_slide_8_modifications,
        build_slide_9_guard,
        build_slide_10_feasibility,
    ]
    
    for i, builder in enumerate(builders):
        print(f"Building slide {i+1}: {builder.__name__}")
        slide = prs.slides.add_slide(blank_layout)
        builder(slide)
        
    out_file = "HIMVAJRA_updated.pptx"
    prs.save(out_file)
    print(f"\n[SUCCESS] Presentation generated successfully: {out_file} (10 slides)")

if __name__ == '__main__':
    main()
