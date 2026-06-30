from fpdf import FPDF
from datetime import datetime

def generate_report():

    pdf = FPDF()

    pdf.add_page()

    # =========================
    # TITLE
    # =========================

    pdf.set_font("Arial", "B", 20)

    pdf.cell(
        200,
        10,
        "AI-Powered Smart Waste Intelligence Platform",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # =========================
    # OVERVIEW
    # =========================

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        200,
        10,
        "Project Overview",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    overview = """
This platform combines computer vision,
explainable AI, sustainability analytics,
and environmental intelligence systems
to improve recycling awareness and
waste management efficiency.
"""

    pdf.multi_cell(
        0,
        8,
        overview
    )

    pdf.ln(5)

    # =========================
    # AI PERFORMANCE
    # =========================

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        200,
        10,
        "AI Performance",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    performance = """
EfficientNet-B0 achieved:

- Validation Accuracy: 98.5%
- Strong explainability localization
- Stable real-time inference
- Edge-AI deployment suitability
"""

    pdf.multi_cell(
        0,
        8,
        performance
    )

    pdf.ln(5)

    # =========================
    # SUSTAINABILITY
    # =========================

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        200,
        10,
        "Sustainability Impact",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    sustainability = """
The system estimates:
- CO2 reduction impact
- Recycling efficiency
- Waste distribution trends
- Environmental awareness metrics
"""

    pdf.multi_cell(
        0,
        8,
        sustainability
    )

    pdf.ln(5)

    # =========================
    # RESEARCH
    # =========================

    pdf.set_font("Arial", "B", 14)

    pdf.cell(
        200,
        10,
        "Research Contributions",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    research = """
- Multi-model benchmarking
- Explainable AI experimentation
- Human-centered AI design
- Sustainability-oriented analytics
- Real-time intelligent classification
"""

    pdf.multi_cell(
        0,
        8,
        research
    )

    pdf.ln(10)

    # =========================
    # FOOTER
    # =========================

    pdf.set_font("Arial", "I", 10)

    pdf.cell(
        200,
        10,
        f"Generated: {datetime.now()}",
        ln=True
    )

    # =========================
    # SAVE
    # =========================

    pdf.output("AI_Waste_Report.pdf")

    return "AI_Waste_Report.pdf"