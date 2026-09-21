"""
HIMVAJRA PPT Updater
Updates HIMVAJRA.pptx with corrected slides based on the full solution
from SIH ELITE SOLUTION ARCHITECT.docx and Aksha_SIH 26.pdf
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
import copy, os, re

# ──────────────────────────────────────
# COLOUR PALETTE (dark theme matching the web sim)
# ──────────────────────────────────────
C_BG         = RGBColor(0x08, 0x0C, 0x14)   # dark bg
C_CARD       = RGBColor(0x0D, 0x15, 0x25)   # card bg
C_BLUE       = RGBColor(0x00, 0xAA, 0xFF)   # accent blue
C_ORANGE     = RGBColor(0xFF, 0x77, 0x00)   # accent orange
C_GREEN      = RGBColor(0x00, 0xE6, 0x76)   # accent green
C_RED        = RGBColor(0xFF, 0x3D, 0x3D)   # accent red
C_WHITE      = RGBColor(0xE8, 0xF4, 0xFF)   # primary text
C_GRAY       = RGBColor(0x7A, 0xA5, 0xCC)   # secondary text
C_MUTED      = RGBColor(0x45, 0x60, 0x80)   # muted

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ──────────────────────────────────────
# HELPERS
# ──────────────────────────────────────

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
    """Remove all existing shapes from a slide."""
    for shape in list(slide.shapes):
        sp = shape.element
        sp.getparent().remove(sp)

# ──────────────────────────────────────
# SLIDE BUILDERS
# ──────────────────────────────────────

def build_title_slide(slide):
    clear_slide(slide)
    # Full bg
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    # Top accent bar
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    # Badge
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4),
                "SMART INDIA HACKATHON 2026  |  PROBLEM #26049  |  DRDO",
                font_size=10, color=C_BLUE, align=PP_ALIGN.CENTER)
    # Main title
    add_textbox(slide, Inches(0.8), Inches(1.1), Inches(11.7), Inches(1.5),
                "HIMVAJRA", font_size=72, bold=True, color=C_BLUE, align=PP_ALIGN.CENTER)
    # Subtitle
    add_textbox(slide, Inches(0.8), Inches(2.5), Inches(11.7), Inches(0.7),
                "High-Altitude Integrated Monitoring, Validation And\nJunction-thermal Resilience Architecture",
                font_size=18, color=C_GRAY, align=PP_ALIGN.CENTER)
    # One liner
    add_textbox(slide, Inches(1.2), Inches(3.4), Inches(11.0), Inches(0.6),
                "A failure-physics platform that predicts how electronics degrade at 3,000–6,000 m,\n"
                "proves it in a hypobaric-cryo chamber, and prevents failure with a retrofit controller.",
                font_size=13, color=C_WHITE, align=PP_ALIGN.CENTER, italic=True)
    # 4 subsystems
    boxes = [
        ("🏛️ CHAMBER", "Hypobaric-cryo\nvalidation rig", C_BLUE),
        ("⚙️ FORGE",    "Failure-physics\nprediction engine", C_ORANGE),
        ("🛡️ GUARD",   "Retrofit envelope\ncontroller", C_GREEN),
        ("🖥️ FLEET",   "Air-gapped ops\nmonitoring", C_GRAY),
    ]
    for i, (title, desc, col) in enumerate(boxes):
        x = Inches(0.5 + i * 3.2)
        add_rect(slide, x, Inches(4.3), Inches(3.0), Inches(1.8),
                 RGBColor(0x0D, 0x15, 0x25), col)
        add_textbox(slide, x + Inches(0.1), Inches(4.4), Inches(2.8), Inches(0.5),
                    title, font_size=14, bold=True, color=col)
        add_textbox(slide, x + Inches(0.1), Inches(4.9), Inches(2.8), Inches(0.8),
                    desc, font_size=11, color=C_GRAY)
    # Bottom bar
    add_textbox(slide, Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4),
                "Organisation: DRDO  |  Dataset: NASA Li-ion + AMOVFLY UAV  |  Cost: ₹68,000 Prototype",
                font_size=9, color=C_MUTED, align=PP_ALIGN.CENTER)


def build_problem_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_RED)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "THE PROBLEM — What Ladakh Does to Electronics", font_size=22, bold=True, color=C_WHITE)
    # 6 problem cards
    problems = [
        ("🌡️ Reduced Cooling", "At 5,500 m air density = 50% of sea level.\nh ∝ ρ^0.8 → θ_sa rises 74%.\nSame power, same ambient → chip 18°C hotter.", C_ORANGE),
        ("⚡ Insulation Breakdown", "Low pressure reduces dielectric strength.\nPaschen minimum shifts — arcing at gaps\nsafe at sea level. Radar, motor windings at risk.", C_RED),
        ("🔋 Battery Degradation", "Cold reduces Li-ion capacity & raises R_int.\nDrone: 60 min → 22 min flight.\nPremature voltage-sag cutoff wastes real energy.", C_BLUE),
        ("🔄 Thermal Cycling", "Ladakh: −35°C nights, +40°C days.\nCoffin-Manson: ΔT=50°C → ~800 cycles.\nSolder cracks, PCB warps, BGA fails.", C_GREEN),
        ("☢️ Radiation (SEU)", "Thin atmosphere → more cosmic rays.\nBit flips in memory, config corruption.\nFirmware mitigation + ECC is the fix.", C_GRAY),
        ("🚁 Drone Challenge", "Army drones along LAC: rotors need more power\nin thin air. Combined with cold battery: only\n20-25 min flight vs 60 min at sea level.", C_ORANGE),
    ]
    for i, (title, desc, col) in enumerate(problems):
        row, col_i = divmod(i, 3)
        x = Inches(0.4 + col_i * 4.3)
        y = Inches(1.1 + row * 2.8)
        add_rect(slide, x, y, Inches(4.1), Inches(2.5), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.1), Inches(3.8), Inches(0.5),
                    title, font_size=13, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.6), Inches(3.8), Inches(1.7),
                    desc, font_size=10, color=C_GRAY)


def build_dataset_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "DATASET PIPELINE — From Aksha_SIH 26.pdf", font_size=22, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.85), Inches(12.0), Inches(0.4),
                "We cannot claim NASA's dataset is a 'Ladakh dataset'. Scientifically defensible approach: learn relationships → build altitude model → simulate → predict.",
                font_size=11, color=C_GRAY, italic=True)

    # Pipeline boxes
    pipeline = [
        ("🛸 NASA Li-ion\nBattery Dataset",
         "Charge/discharge cycles at\ndifferent temperatures.\nVoltage, current, capacity,\nRUL. Primary dataset for\nbattery degradation model.",
         C_BLUE),
        ("🚁 AMOVFLY\nUAV Dataset",
         "Flight duration, power\nconsumption, atmospheric\npressure, air density,\ntemperature, wind speed.\nLinks UAV ↔ environment.",
         C_ORANGE),
        ("⚙️ Feature\nEngineering",
         "R_int(T,SoC,age)\nCapacity(T,SoH)\nAir density ρ=P/RT\nConvection derating h∝ρ^n\nPaschen arc-risk",
         C_GREEN),
        ("🧠 Physics-First\nML (GP+RLS+IsoForest)",
         "Gaussian Process residual\nRLS Thévenin battery ECM\nIsolation Forest anomaly\nNO deep learning.\nPhysics is load-bearing.",
         RGBColor(0xA8, 0x55, 0xF7)),
        ("📋 Outputs &\nRecommendations",
         "Battery SOH · RUL\nFailure Risk\nFlight Endurance\nContinue / Pre-heat\nReduce Load / Replace",
         C_GREEN),
    ]

    for i, (title, desc, col) in enumerate(pipeline):
        x = Inches(0.3 + i * 2.55)
        add_rect(slide, x, Inches(1.5), Inches(2.4), Inches(4.5), C_CARD, col)
        add_textbox(slide, x + Inches(0.1), Inches(1.6), Inches(2.2), Inches(0.7),
                    title, font_size=12, bold=True, color=col)
        add_textbox(slide, x + Inches(0.1), Inches(2.35), Inches(2.2), Inches(3.4),
                    desc, font_size=9.5, color=C_GRAY)
        # Arrow (not last)
        if i < len(pipeline) - 1:
            add_textbox(slide, x + Inches(2.4), Inches(3.5), Inches(0.15), Inches(0.5),
                        "→", font_size=18, color=C_MUTED)

    # Bottom note
    add_textbox(slide, Inches(0.5), Inches(6.5), Inches(12.0), Inches(0.7),
                "Key insight: Existing datasets → learn degradation/performance relationships → "
                "build high-altitude environmental model → simulate Ladakh conditions → predict risk/performance.\n"
                "This is far stronger than pretending training data was collected in Ladakh.",
                font_size=10, color=C_MUTED, italic=True)


def build_architecture_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_ORANGE)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "SYSTEM ARCHITECTURE — HIMVAJRA Closed Validation Loop", font_size=22, bold=True, color=C_WHITE)

    # Three main boxes (VALIDATE, PREDICT, PROTECT)
    arch_boxes = [
        ("VALIDATE\n(CHAMBER)", "Vacuum vessel 30–101 kPa PID\nCryo shell −35…+55°C\n8× K-type TC · INA228 · IR array\nHV coupon · UV-A/B", C_BLUE, Inches(0.5)),
        ("PREDICT\n(FORGE)", "Thermal RC network (h∝ρ^n)\nPaschen arc-risk eval\nCoffin-Manson fatigue\nBattery ECM · GP residual correction\n→ Derating report + Hardening BOM", C_ORANGE, Inches(4.7)),
        ("PROTECT\n(GUARD)", "STM32G4 + ESP32-S3\nNOMINAL → DERATED → PROTECT → LOCKOUT\nFan · Heater · Load shed · Charge inhibit\nLoRa/MQTT · 230-day store-and-forward", C_GREEN, Inches(8.9)),
    ]

    for title, desc, col, x in arch_boxes:
        add_rect(slide, x, Inches(1.0), Inches(4.0), Inches(4.0), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), Inches(1.1), Inches(3.7), Inches(0.7),
                    title, font_size=14, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), Inches(1.85), Inches(3.7), Inches(2.8),
                    desc, font_size=10, color=C_GRAY)

    # Arrows
    for ax in [Inches(4.5), Inches(8.7)]:
        add_textbox(slide, ax, Inches(2.8), Inches(0.3), Inches(0.5), "→", font_size=24, color=C_MUTED)

    # Feedback loop arrow text
    add_textbox(slide, Inches(0.5), Inches(5.3), Inches(12.0), Inches(0.35),
                "← Field telemetry recalibrates FORGE — the earned digital twin loop ←",
                font_size=10, color=C_BLUE, align=PP_ALIGN.CENTER, italic=True)

    # Physics strip
    add_rect(slide, Inches(0.5), Inches(5.7), Inches(12.3), Inches(1.55), RGBColor(0x05, 0x10, 0x20))
    add_textbox(slide, Inches(0.7), Inches(5.8), Inches(12.0), Inches(0.35),
                "GOVERNING PHYSICS", font_size=10, bold=True, color=C_MUTED)
    eqs = [
        "ρ = P/(R·T)    air density",
        "h ∝ ρ^0.5 natural   h ∝ ρ^0.8 forced",
        "V_bd = f(P·d)   Paschen arc",
        "N_f = C·(ΔT)^−n   Coffin-Manson",
        "V_term = V_ocv − I·R_int(T)   SoP cutoff",
    ]
    add_textbox(slide, Inches(0.7), Inches(6.2), Inches(12.0), Inches(0.9),
                "    |    ".join(eqs), font_size=10, color=C_BLUE)


def build_thermal_proof_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_RED)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "\"COLD AIR, HOT CHIP\" — The WOW Demo", font_size=22, bold=True, color=C_WHITE)
    add_textbox(slide, Inches(0.5), Inches(0.85), Inches(12.0), Inches(0.45),
                "Ambient FLAT. Power CONSTANT. Only pressure drops — hotspot climbs 18°C. Prediction set BEFORE run.",
                font_size=13, color=C_ORANGE, italic=True)

    # Table: altitude vs thermal penalty
    data = [
        ("Altitude", "Pressure (kPa)", "ρ/ρ₀", "θ_sa Natural", "θ_sa Forced"),
        ("Sea Level", "101.3", "1.00", "—", "—"),
        ("3,000 m",   "70.1",  "0.69", "+20%", "+33%"),
        ("4,500 m",   "57.7",  "0.57", "+32%", "+56%"),
        ("5,500 m",   "50.5",  "0.50", "+41%", "+74% ← PS scenario"),
    ]
    col_w = [Inches(2.0), Inches(2.2), Inches(1.6), Inches(2.2), Inches(3.5)]
    start_y = Inches(1.5)
    for ri, row in enumerate(data):
        is_header = (ri == 0)
        is_last   = (ri == len(data) - 1)
        bg = C_CARD if not is_header else RGBColor(0x00, 0x44, 0x88)
        hl = C_ORANGE if is_last else (C_BLUE if is_header else None)
        start_x = Inches(0.5)
        for ci, cell in enumerate(row):
            add_rect(slide, start_x, start_y + Inches(ri * 0.55), col_w[ci], Inches(0.52), bg,
                     C_BLUE if is_header else C_CARD)
            add_textbox(slide, start_x + Inches(0.05), start_y + Inches(ri * 0.55) + Inches(0.05),
                        col_w[ci] - Inches(0.1), Inches(0.42),
                        cell, font_size=11, bold=is_header or is_last,
                        color=hl or C_WHITE, align=PP_ALIGN.CENTER)
            start_x += col_w[ci]

    # Key formula
    add_textbox(slide, Inches(0.5), Inches(4.8), Inches(6.0), Inches(0.45),
                "Key: h ∝ Re^0.8, Re ∝ ρ, ρ halves at 5,500m → h × 2^−0.8 = 0.574 → θ_sa × 1.74 = +74%",
                font_size=11, color=C_BLUE)

    # Demo script
    add_rect(slide, Inches(7.0), Inches(1.5), Inches(5.8), Inches(3.8), C_CARD, C_ORANGE)
    add_textbox(slide, Inches(7.15), Inches(1.6), Inches(5.5), Inches(0.4),
                "2-MINUTE DEMO SCRIPT", font_size=11, bold=True, color=C_ORANGE)
    demo_steps = (
        "0:00  FORGE: predicted 71.4°C ± 3.1°C at 54 kPa. Live: 53°C at 101 kPa.\n"
        "0:20  Start pump. Pressure descends. Ambient TC held FLAT on screen.\n"
        "0:50  Hotspot curve climbs.\n"
        "1:30  Pressure stabilises at 54 kPa. Hotspot settles — read vs prediction band.\n"
        "1:45  Enable GUARD → DERATED → fan ramp + load shed → hotspot pulled back.\n"
        "2:00  \"That is the difference between a specification and a proof.\""
    )
    add_textbox(slide, Inches(7.15), Inches(2.1), Inches(5.5), Inches(3.0),
                demo_steps, font_size=10, color=C_GRAY)

    # Worked example
    add_rect(slide, Inches(0.5), Inches(5.2), Inches(6.0), Inches(1.8), C_CARD, C_GREEN)
    add_textbox(slide, Inches(0.65), Inches(5.3), Inches(5.7), Inches(0.35),
                "WORKED EXAMPLE (15 W hotspot, θ_sa = 3.0 °C/W, T_amb = 25°C)", font_size=10, bold=True, color=C_GREEN)
    add_textbox(slide, Inches(0.65), Inches(5.7), Inches(5.7), Inches(1.1),
                "Sea level: ΔT = 15W × 3.0 = 45°C → T_hotspot = 70°C\n"
                "5,500 m:  ΔT = 15W × 3.0 × 1.74 = 78°C → T_hotspot = 103°C  ← OVER LIMIT\n"
                "GUARD DERATED: fan 100%, load shed → ΔT back to 52°C → T_hotspot = 77°C  ✅",
                font_size=10, color=C_GRAY)


def build_battery_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_GREEN)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "BATTERY & DRONE — Energy Physics at High Altitude", font_size=22, bold=True, color=C_WHITE)

    # Drone loss budget waterfall labels
    add_textbox(slide, Inches(0.5), Inches(1.0), Inches(6.5), Inches(0.4),
                "DRONE LOSS BUDGET: 60 min → 22 min DECOMPOSED", font_size=13, bold=True, color=C_ORANGE)
    
    budget_items = [
        ("Baseline (Sea Level)", 60, C_BLUE,   ""),
        ("Aerodynamic Loss",     -14, C_ORANGE,  "MODELLED — thin air, more rotor power"),
        ("Cold Capacity Loss",   -12, C_RED,     "MEASURED — C_usable(T) from NASA dataset"),
        ("Premature Cutoff",      -8, C_RED,     "MEASURED — I·R_int(T) voltage sag"),
        ("Actual Flight Time",    26, RGBColor(0x00,0x44,0x88), ""),
        ("GUARD Recovery",        +8, C_GREEN,   "SoP cutoff + preconditioning"),
    ]

    bar_x = Inches(0.6)
    for i, (label, val, col, note) in enumerate(budget_items):
        y = Inches(1.5 + i * 0.75)
        bar_w = Inches(abs(val) / 70 * 5.5)
        add_rect(slide, bar_x, y + Inches(0.05), bar_w, Inches(0.55), col)
        add_textbox(slide, bar_x + bar_w + Inches(0.1), y + Inches(0.1), Inches(5.0), Inches(0.4),
                    f"{label}: {'+' if val > 0 else ''}{val} min  {note}",
                    font_size=10, color=C_WHITE if val > 0 else C_GRAY)

    # Battery physics column
    add_rect(slide, Inches(7.2), Inches(1.0), Inches(5.8), Inches(6.2), C_CARD, C_BLUE)
    add_textbox(slide, Inches(7.4), Inches(1.1), Inches(5.4), Inches(0.45),
                "BATTERY PHYSICS — NASA Dataset Model", font_size=12, bold=True, color=C_BLUE)
    bat_content = (
        "Capacity vs Temperature:\n"
        "  C(T) = C_rated × (1 − k·(25−T)) × SoH\n"
        "  At −20°C: ≈60–65% of rated capacity\n\n"
        "Internal Resistance (Arrhenius):\n"
        "  R_int(T) = R₀ × exp(Ea/k × (1/T − 1/T_ref))\n"
        "  At −20°C: R_int ≈ 3-4× room temperature\n\n"
        "Voltage Sag:\n"
        "  V_term = V_ocv − I · R_int(T)\n"
        "  Trips LVC not from empty battery — from sag\n\n"
        "SoP Cutoff (GUARD innovation):\n"
        "  V_sop = V_ocv − I · R_int(T)\n"
        "  Terminates when REAL power < mission reserve\n"
        "  Recovers 8–12 min of false-early cutoff\n\n"
        "Preconditioning:\n"
        "  Heater film → T_bat > +10°C before power-up\n"
        "  Runs on shore power, not flight battery"
    )
    add_textbox(slide, Inches(7.4), Inches(1.65), Inches(5.4), Inches(5.3),
                bat_content, font_size=10, color=C_GRAY)


def build_guard_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_GREEN)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "GUARD — Envelope State Machine (STM32, 10 Hz, Fully Autonomous)", font_size=20, bold=True, color=C_WHITE)

    states = [
        ("NOMINAL", "All margins > 20%\nPassive monitor, 1/60 Hz", C_GREEN,   "None"),
        ("DERATED", "T_j within 20% of limit OR\nSoP below reserve OR P low",
                    C_ORANGE, "Notify only\n(fan + load shed)"),
        ("PROTECT", "T_j > limit−5°C OR\nbatt < 0°C OR dew margin < 2°C",
                    C_RED,    "Notify + reason\n(charge inhibit, hold)"),
        ("LOCKOUT", "Hard limit breach OR\nsensor disagree OR damage > 95%",
                    RGBColor(0xA8, 0x55, 0xF7), "Operator ack required\n(cut non-safety power)"),
    ]

    for i, (name, cond, col, human) in enumerate(states):
        x = Inches(0.4 + i * 3.2)
        add_rect(slide, x, Inches(1.2), Inches(3.0), Inches(3.5), C_CARD, col)
        add_textbox(slide, x + Inches(0.12), Inches(1.3), Inches(2.76), Inches(0.5),
                    name, font_size=16, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_textbox(slide, x + Inches(0.12), Inches(1.9), Inches(2.76), Inches(1.5),
                    f"Condition:\n{cond}", font_size=10, color=C_GRAY)
        add_textbox(slide, x + Inches(0.12), Inches(3.45), Inches(2.76), Inches(0.8),
                    f"Human: {human}", font_size=9, color=col)
        # Arrow
        if i < 3:
            add_textbox(slide, x + Inches(3.0), Inches(2.7), Inches(0.2), Inches(0.4),
                        "→", font_size=16, color=C_MUTED)

    # Actuators
    add_textbox(slide, Inches(0.5), Inches(5.0), Inches(12.0), Inches(0.4),
                "ACTUATORS — Per State", font_size=12, bold=True, color=C_MUTED)
    acts = [
        ("🌀 Fan", "30%", "100%", "100%", "100%"),
        ("🔥 Heater Film", "OFF", "OFF", "ON", "ON"),
        ("⚡ Charge Enable", "ON", "ON", "INHIBITED", "INHIBITED"),
        ("🔌 Non-crit Load", "FULL", "SHED", "SHED", "CUT"),
        ("📡 Telemetry Rate", "1/60 Hz", "1 Hz", "1 Hz", "1 Hz"),
    ]
    for ri, row in enumerate(acts):
        y = Inches(5.5 + ri * 0.38)
        for ci, cell in enumerate(row):
            x = Inches(0.5 + ci * 2.55)
            col_c = [C_MUTED, C_GREEN, C_ORANGE, C_RED, RGBColor(0xA8,0x55,0xF7)][ci]
            add_textbox(slide, x, y, Inches(2.5), Inches(0.35),
                        cell, font_size=9.5, color=col_c if ci > 0 else C_GRAY)

    # Criticality governance
    add_textbox(slide, Inches(0.5), Inches(7.1), Inches(12.0), Inches(0.35),
                "⚖️ Governance Rule: mission_critical assets — GUARD never autonomously cuts power; it recommends, alarms, logs. A human acts.",
                font_size=10, color=C_ORANGE, italic=True)


def build_innovation_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_BLUE)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "INNOVATION — What Makes HIMVAJRA Different", font_size=22, bold=True, color=C_WHITE)

    innovations = [
        ("Layer 1\nCore Innovation",
         "Replacing assertion with measurement.\n"
         "\"Hardened for high altitude\" = datasheet claim with no combined P+T validation.\n"
         "HIMVAJRA: affordable hypobaric-cryo chamber brings this capability to unit workshops,\nnot just national labs with ₹15-40 lakh equipment.",
         C_BLUE),
        ("Layer 2\nTechnical Innovation",
         "① Physics-first prediction with GP residual + calibrated uncertainty band\n"
         "   — every derating number ships with a measured error bar.\n"
         "② SoP cutoff vs terminal-voltage cutoff\n"
         "   — recovers real energy lost to false-early cold cutoff.\n"
         "③ Coffin-Manson damage budgeting from measured ΔT\n"
         "   — 'this asset has 22% of thermal-cycle budget left' → scheduled maintenance.",
         C_ORANGE),
        ("Layer 3\nStrategic Innovation",
         "GUARD is a retrofit — no re-procurement of fielded radar, BTS, genset, or drone.\n"
         "Federated model-sharing: sites share correction coefficients, NOT raw telemetry.\n"
         "No data-classification conflict. Scales across Army, BSF, ITBP, BRO.\n"
         "Fully air-gapped, no cloud, no foreign APIs — passes defence security review.",
         C_GREEN),
    ]

    for i, (title, desc, col) in enumerate(innovations):
        y = Inches(1.1 + i * 2.0)
        add_rect(slide, Inches(0.5), y, Inches(12.3), Inches(1.85), C_CARD, col)
        add_textbox(slide, Inches(0.65), y + Inches(0.1), Inches(2.0), Inches(1.6),
                    title, font_size=12, bold=True, color=col)
        add_textbox(slide, Inches(2.8), y + Inches(0.1), Inches(9.8), Inches(1.6),
                    desc, font_size=10, color=C_GRAY)

    # Bottom: NOT doing
    add_rect(slide, Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.42), RGBColor(0x14,0x05,0x05))
    add_textbox(slide, Inches(0.65), Inches(7.05), Inches(12.0), Inches(0.33),
                "❌ No LLM  ❌ No deep learning on non-existent data  ❌ No blockchain  ❌ No flying drone  ❌ No cloud — and we will say why, explicitly, to the judges.",
                font_size=9.5, color=C_RED)


def build_feasibility_slide(slide):
    clear_slide(slide)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, C_BG)
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.08), C_ORANGE)
    add_textbox(slide, Inches(0.5), Inches(0.2), Inches(12.0), Inches(0.6),
                "FEASIBILITY & BUILD PLAN", font_size=22, bold=True, color=C_WHITE)

    quads = [
        ("⚙️ Technical", "Vacuum PID, TC DAQ, FreeRTOS firmware,\nFastAPI — standard undergrad engineering.\nHardest: leak-tight cryo-vacuum mechanical.\nAll parts from Indian suppliers. ✅", C_BLUE),
        ("🏛️ Operational", "GUARD is fully autonomous — zero daily operator input.\nFleet UI designed for signals NCO: read-and-ack.\nMission-critical assets: system recommends, human acts. ✅", C_ORANGE),
        ("💰 Financial", "Prototype: ₹68,000 recommended\nFloor: ₹21,500\nGuard at volume: ₹8-15k/unit\nNo recurring cloud cost.\nOne prevented PSU failure > total project cost. ✅", C_GREEN),
        ("🚀 Deployment", "Retrofit over CAN/RS-485.\nNo re-procurement of any fielded equipment.\nAir-gapped offline installer, no outbound calls.\nZero PII — no data classification concern. ✅", C_GRAY),
    ]

    for i, (title, desc, col) in enumerate(quads):
        row, ci = divmod(i, 2)
        x = Inches(0.5 + ci * 6.4)
        y = Inches(1.1 + row * 2.3)
        add_rect(slide, x, y, Inches(6.1), Inches(2.1), C_CARD, col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.1), Inches(5.8), Inches(0.45),
                    title, font_size=13, bold=True, color=col)
        add_textbox(slide, x + Inches(0.15), y + Inches(0.6), Inches(5.8), Inches(1.35),
                    desc, font_size=10, color=C_GRAY)

    # Timeline strip
    add_rect(slide, Inches(0.5), Inches(5.85), Inches(12.3), Inches(1.35), RGBColor(0x05, 0x10, 0x20))
    add_textbox(slide, Inches(0.65), Inches(5.92), Inches(12.0), Inches(0.35),
                "BUILD TIMELINE", font_size=11, bold=True, color=C_MUTED)
    weeks = [
        ("WK 1", "Order pump + vessel\nSafety SOP\nForge equations"),
        ("WK 2", "Pressure PID ±2kPa\nTC array calibrated\nForge schema FROZEN"),
        ("WK 3", "Cryo integrated\n★ GATE: Cold-Air-Hot-Chip\nPrediction vs measured"),
        ("WK 4", "Guard v1 firmware\nBattery bench SoP\nFleet UI 2 screens"),
        ("WK 5", "End-to-end integration\nFault injection\nDemo rehearsal ×12"),
    ]
    for i, (wk, tasks) in enumerate(weeks):
        x = Inches(0.65 + i * 2.4)
        col_c = C_ORANGE if i == 2 else C_BLUE
        add_textbox(slide, x, Inches(6.35), Inches(2.2), Inches(0.35),
                    wk, font_size=10, bold=True, color=col_c)
        add_textbox(slide, x, Inches(6.72), Inches(2.2), Inches(0.45),
                    tasks, font_size=8.5, color=C_GRAY)


# ──────────────────────────────────────
# MAIN
# ──────────────────────────────────────
def update_pptx():
    src = "HIMVAJRA.pptx"
    dst = "HIMVAJRA_updated.pptx"

    prs = Presentation(src)
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H

    slide_layouts = prs.slide_layouts
    blank_layout  = slide_layouts[0]  # use first available layout

    # We'll rebuild specific slides and append new ones
    # First, let's see how many slides exist
    n_existing = len(prs.slides)
    print(f"Existing slides: {n_existing}")

    # Strategy: replace slides 1-8 with our new content
    # For safety, we'll clear and rebuild each slide
    builders = [
        build_title_slide,
        build_problem_slide,
        build_dataset_slide,
        build_architecture_slide,
        build_thermal_proof_slide,
        build_battery_slide,
        build_guard_slide,
        build_innovation_slide,
        build_feasibility_slide,
    ]

    # Rebuild existing slides (up to what we have)
    for i, builder in enumerate(builders):
        if i < len(prs.slides):
            print(f"  Rebuilding slide {i+1}: {builder.__name__}")
            builder(prs.slides[i])
        else:
            # Add new slide
            print(f"  Adding slide {i+1}: {builder.__name__}")
            slide = prs.slides.add_slide(blank_layout)
            builder(slide)

    prs.save(dst)
    print(f"\n✅ Saved: {dst}")
    return dst


if __name__ == '__main__':
    result = update_pptx()
    print(f"Output: {result}")
