from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.config import DATA_DIR, DATA_SUBFOLDERS


PROJECTS = {
    "school": {
        "name": "School",
        "areas": "3 floors with classrooms, cafeteria, gym, admin office, and library",
        "panels": "MSB-SCH, LP-1A, LP-2A, LP-3A, EM-LP1, MDP-SCH",
        "facts": [
            "The 3rd floor HVAC system is served from panel MDP-SCH using feeder H3-42.",
            "Emergency lighting is tied to EM-LP1 and covers stairwells, corridors, cafeteria exits, gym exits, and egress doors.",
            "Data rooms are located on each floor and use low-voltage backbone conduit to the MDF.",
            "Lighting revision CO-SCH-002 adds dimmable LED fixtures in the cafeteria and high-bay LED replacements in the gym.",
        ],
        "rfi": [
            {"id": "RFI-SCH-014", "status": "Open", "question": "Confirm ceiling device locations in library reading room.", "answer": ""},
            {"id": "RFI-SCH-021", "status": "Open", "question": "Clarify emergency lighting circuit homeruns for gym exits.", "answer": ""},
            {"id": "RFI-SCH-009", "status": "Closed", "question": "Confirm LP-3A spare breaker count.", "answer": "Provide six 20A spares."},
        ],
        "change": [
            {"id": "CO-SCH-002", "title": "Cafeteria and gym lighting revision", "impact": "Adds fixtures, dimming controls, conduit, wire, and 48 labor hours."}
        ],
        "quantities": [
            ("panels", "PANEL_225A", 4, "School distribution and lighting panels"),
            ("lighting fixtures", "LED_2X4", 188, "Classroom and corridor fixtures"),
            ("emergency lighting", "EM_LIGHT", 42, "EM-LP1 egress lighting"),
            ("conduit", "EMT_3_4", 4200, "Branch conduit"),
            ("wire", "THHN_12", 12500, "Branch circuit conductors"),
            ("low voltage/data", "CAT6_DROP", 260, "Classroom and office drops"),
            ("fire alarm", "FA_DEVICE", 96, "Pulls, strobes, horns, smoke devices"),
            ("HVAC electrical", "HVAC_DISCONNECT", 16, "Rooftop and mechanical equipment"),
        ],
    },
    "hospital": {
        "name": "Hospital",
        "areas": "emergency department, ICU, operating rooms, patient rooms, imaging area, and nurse stations",
        "panels": "MSB-HOSP, CRIT-LP1, EQ-LP2, OR-ISO-1, GEN-EM1",
        "facts": [
            "OR isolated power is supported by panel OR-ISO-1 with line isolation monitoring.",
            "Generator GEN-EM1 backs emergency and critical circuits through ATS-1 and ATS-2.",
            "The MRI requires a dedicated feeder from EQ-LP2 with isolated grounding requirements.",
            "Change order CO-HOSP-004 adds backup power to the imaging wing including ATS tie-in and critical branch circuits.",
            "Nurse call system emergency power is questioned in RFI-HOSP-033 and remains open pending owner direction.",
        ],
        "rfi": [
            {"id": "RFI-HOSP-033", "status": "Open", "question": "Should the nurse call head-end be backed by emergency power?", "answer": ""},
            {"id": "RFI-HOSP-028", "status": "Open", "question": "Confirm isolated power receptacle count in OR-2.", "answer": ""},
            {"id": "RFI-HOSP-011", "status": "Closed", "question": "Confirm generator annunciator location.", "answer": "Install at security desk."},
        ],
        "change": [
            {"id": "CO-HOSP-004", "title": "Imaging wing backup power", "impact": "Adds ATS tie-in, critical branch panel circuits, feeder, testing, and 72 labor hours."}
        ],
        "quantities": [
            ("panels", "PANEL_400A", 6, "Critical, equipment, and normal power panels"),
            ("emergency lighting", "EM_LIGHT", 95, "Life safety egress coverage"),
            ("conduit", "EMT_1", 6100, "Hospital feeders and branch conduit"),
            ("wire", "THHN_10", 18800, "Critical branch and equipment conductors"),
            ("fire alarm", "FA_DEVICE", 220, "Life safety devices"),
            ("low voltage/data", "CAT6_DROP", 420, "Nurse stations and patient rooms"),
            ("HVAC electrical", "HVAC_DISCONNECT", 38, "Air handlers and medical exhaust"),
            ("devices/receptacles", "HOSP_RECEPT", 520, "Hospital-grade receptacles"),
        ],
    },
    "food_mart": {
        "name": "Food Mart",
        "areas": "single-story retail building with sales floor, checkout, refrigeration, storage, office, and exterior signage",
        "panels": "MSB-FM, LP-SALES, LP-REFRIG, LP-HVAC, LV-FM1",
        "facts": [
            "The walk-in freezer is fed from LP-REFRIG circuit RF-7 with a dedicated 40A circuit.",
            "Refrigeration equipment is served by LP-REFRIG and requires local disconnects at each condensing unit.",
            "POS network wiring is served from low-voltage cabinet LV-FM1 with CAT6 home runs to checkout counters.",
            "Exterior LED signage uses LP-SALES circuit SGN-2 with #10 THHN in 3/4 inch EMT.",
            "Change order CO-FM-003 adds the exterior LED signage circuit and photocell control.",
        ],
        "rfi": [
            {"id": "RFI-FM-006", "status": "Open", "question": "Confirm dedicated circuit size for walk-in freezer.", "answer": ""},
            {"id": "RFI-FM-010", "status": "Closed", "question": "Confirm POS cabinet location.", "answer": "Install LV-FM1 in office IT closet."},
        ],
        "change": [
            {"id": "CO-FM-003", "title": "Exterior LED signage circuit", "impact": "Adds SGN-2 circuit, photocell, weatherproof disconnect, #10 THHN, and 12 labor hours."}
        ],
        "quantities": [
            ("panels", "PANEL_225A", 3, "Retail panels"),
            ("lighting fixtures", "LED_2X4", 96, "Sales floor and support area lighting"),
            ("conduit", "EMT_3_4", 1900, "Branch conduit"),
            ("wire", "THHN_10", 5200, "Signage and refrigeration conductors"),
            ("low voltage/data", "CAT6_DROP", 54, "POS and office drops"),
            ("HVAC electrical", "HVAC_DISCONNECT", 6, "Rooftop HVAC disconnects"),
            ("refrigeration electrical", "REFRIG_DISCONNECT", 14, "Cases, freezer, and condensing units"),
            ("signage circuits", "SIGN_CIRCUIT", 2, "Exterior LED sign circuits"),
        ],
    },
}


CATALOG = [
    ("PANEL_225A", "225A lighting/power panel", "each", 1850, 6.5),
    ("PANEL_400A", "400A distribution panel", "each", 4200, 10.0),
    ("LED_2X4", "2x4 LED fixture", "each", 145, 0.55),
    ("EM_LIGHT", "Emergency light/exit combo", "each", 118, 0.8),
    ("EMT_3_4", "3/4 inch EMT conduit", "ft", 1.25, 0.035),
    ("EMT_1", "1 inch EMT conduit", "ft", 1.95, 0.045),
    ("THHN_12", "#12 THHN copper wire", "ft", 0.18, 0.008),
    ("THHN_10", "#10 THHN copper wire", "ft", 0.31, 0.01),
    ("CAT6_DROP", "CAT6 data drop", "each", 92, 0.9),
    ("FA_DEVICE", "Fire alarm device", "each", 135, 0.75),
    ("HVAC_DISCONNECT", "HVAC equipment disconnect", "each", 240, 1.2),
    ("HOSP_RECEPT", "Hospital grade receptacle", "each", 36, 0.22),
    ("REFRIG_DISCONNECT", "Refrigeration disconnect", "each", 260, 1.4),
    ("SIGN_CIRCUIT", "Exterior sign circuit assembly", "each", 640, 4.0),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_pdf(path: Path, project: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 15)
    c.drawString(42, height - 42, f"E-101 Simplified Electrical Layout - {project['name']}")
    c.setFont("Helvetica", 9)
    c.drawString(42, height - 60, f"Areas: {project['areas']}")
    rooms = ["PANEL ROOM", "SALES/CLASS/CARE AREA", "MECHANICAL", "LOW VOLTAGE", "EGRESS", "SERVICE"]
    x, y = 60, height - 135
    for i, room in enumerate(rooms):
        c.setStrokeColor(colors.darkblue)
        c.rect(x + (i % 2) * 245, y - (i // 2) * 120, 210, 82)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12 + (i % 2) * 245, y + 52 - (i // 2) * 120, room)
        c.setFont("Helvetica", 8)
        c.drawString(x + 12 + (i % 2) * 245, y + 32 - (i // 2) * 120, project["panels"][:55])
    c.setStrokeColor(colors.red)
    c.line(110, height - 255, 455, height - 145)
    c.line(120, height - 375, 465, height - 265)
    c.setFillColor(colors.red)
    c.drawString(210, height - 205, "Conduit run / emergency or equipment feeder")
    c.setFillColor(colors.black)
    c.drawString(42, 98, "Key drawing notes:")
    for idx, fact in enumerate(project["facts"][:5], start=1):
        c.drawString(58, 98 - idx * 14, f"{idx}. {fact[:95]}")
    c.showPage()
    c.save()


def main() -> None:
    for folder in DATA_SUBFOLDERS:
        for project_id in PROJECTS:
            (DATA_DIR / project_id / folder).mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "shared").mkdir(parents=True, exist_ok=True)

    with (DATA_DIR / "shared" / "materials_catalog.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item_code", "item_name", "unit", "unit_cost", "labor_hours_per_unit"])
        writer.writerows(CATALOG)
    write(DATA_DIR / "shared" / "labor_rates.json", json.dumps({"journeyman_hourly_rate": 82, "foreman_hourly_rate": 96, "apprentice_hourly_rate": 48}, indent=2))

    for project_id, project in PROJECTS.items():
        base = DATA_DIR / project_id
        facts = "\n".join(f"- {fact}" for fact in project["facts"])
        write(base / "summaries" / "project_summary.md", f"# {project['name']} Electrical Project Summary\n\nAreas: {project['areas']}.\n\nPanels: {project['panels']}.\n\nImportant facts:\n{facts}\n")
        write(base / "specs" / "electrical_specifications.txt", f"Conduit and wiring specification for {project['name']}: EMT conduit in exposed indoor areas, THHN copper conductors, labeled homeruns, NEC-compliant grounding, and updated as-built panel directories.\n\n{facts}\n")
        write(base / "schedules" / "panel_schedule.csv", "panel,served_load,notes\n" + "\n".join([f"{p.strip()},Refer to project summary,Generated sample schedule" for p in project["panels"].split(",")]))
        write(base / "schedules" / "lighting_fixture_schedule.csv", "fixture,type,location,notes\nA1,2x4 LED,Typical interiors,0-10V dimming where shown\nEM1,Emergency light,Egress path,Connected to emergency circuit\n")
        write(base / "rfi" / "rfi_log.json", json.dumps(project["rfi"], indent=2))
        write(base / "change_orders" / "change_order_log.json", json.dumps(project["change"], indent=2))
        write(base / "materials" / "material_list.csv", "category,item_code,quantity,notes\n" + "\n".join(f"{c},{code},{qty},{notes}" for c, code, qty, notes in project["quantities"]))
        write(base / "safety" / "safety_notes.md", "# Safety Notes\n\nUse lockout/tagout, verify panel labels, coordinate shutdowns, follow NEC and local AHJ requirements, and confirm latest approved drawings before work.\n")
        write(base / "estimates" / "project_quantities.json", json.dumps({"items": [{"category": c, "item_code": code, "quantity": qty, "notes": notes} for c, code, qty, notes in project["quantities"]], "assumptions": ["Normal working hours", "Local labor rate table", "Synthetic MVP quantities for demo"], "missing_data_warnings": ["Final stamped drawings should be verified before bid submission"]}, indent=2))
        make_pdf(base / "drawings" / "E-101_simplified_electrical_layout.pdf", project)
    print("Synthetic electrical project dataset generated.")


if __name__ == "__main__":
    main()
