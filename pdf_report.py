from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table

def generate_pdf_report(df, output="Executive_Report.pdf"):

    doc = SimpleDocTemplate(output)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AWS Security Executive Summary", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    severity_counts = df["Severity"].value_counts()

    data = [["Severity", "Count"]]

    for sev, count in severity_counts.items():
        data.append([sev, str(count)])

    table = Table(data)
    elements.append(table)

    doc.build(elements)

    return output
