from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle
from reportlab.lib.units import inch
from datetime import datetime

def generate_pdf_report(df, output):

    doc = SimpleDocTemplate(output)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("AWS Security Executive Summary", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    # Date
    today = datetime.now().strftime("%Y-%m-%d")
    elements.append(Paragraph(f"Report Date: {today}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Severity Summary
    severity_counts = df["Severity"].value_counts()

    data = [["Severity", "Count"]]

    for sev in ["Critical", "High", "Medium", "Low"]:
        data.append([sev, str(severity_counts.get(sev, 0))])

    table = Table(data, colWidths=[2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(1,1),(-1,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),1,colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Executive Risk Statement
    critical_count = severity_counts.get("Critical", 0)

    if critical_count > 0:
        risk_statement = "High Risk Environment – Immediate remediation required."
    else:
        risk_statement = "Moderate Risk Environment – Continuous monitoring recommended."

    elements.append(Paragraph(f"Overall Risk Assessment: {risk_statement}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "Executive Recommendation: Prioritize remediation of publicly exposed "
        "sensitive services and enforce least privilege network segmentation.",
        styles["Normal"]
    ))

    doc.build(elements)
