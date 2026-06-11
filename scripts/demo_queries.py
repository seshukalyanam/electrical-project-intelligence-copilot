QUESTIONS = {
    "School": [
        "Which panel serves the 3rd floor HVAC system?",
        "What lighting changes were requested for the cafeteria?",
        "Which RFIs are still unresolved?",
        "Generate a material takeoff for emergency lighting.",
        "Explain the classroom wiring plan to a field technician.",
    ],
    "Hospital": [
        "Which panel supports the operating room isolated power system?",
        "What circuits are connected to emergency backup power?",
        "What changed in the imaging wing backup power change order?",
        "Generate an estimate for critical care room electrical work.",
        "Explain the generator/ATS setup in simple field language.",
    ],
    "Food Mart": [
        "Which panel feeds the walk-in freezer?",
        "What wire and conduit are required for exterior signage?",
        "What changed in the latest signage change order?",
        "Generate a material takeoff for refrigeration power.",
        "Explain the POS low-voltage wiring plan to a technician.",
    ],
}

for project, questions in QUESTIONS.items():
    print(f"\n{project}")
    for question in questions:
        print(f"- {question}")
