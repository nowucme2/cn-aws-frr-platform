from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from engine2 import analyze
from graph_generator import generate_network_graph
from pdf_report import generate_pdf_report

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        file = request.files["file"]

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_excel(filepath)

        analyzed, attack_chain_df = analyze(df)

        output_excel = os.path.join(UPLOAD_FOLDER, "analysis_output.xlsx")

        with pd.ExcelWriter(output_excel) as writer:
            analyzed.to_excel(writer, sheet_name="Detailed Findings", index=False)
            attack_chain_df.to_excel(writer, sheet_name="Attack Chains", index=False)

            summary = analyzed["Severity"].value_counts().reset_index()
            summary.columns = ["Severity", "Count"]
            summary.to_excel(writer, sheet_name="Executive Summary", index=False)

        graph_file = os.path.join(UPLOAD_FOLDER, "network_graph.png")
        generate_network_graph(analyzed, graph_file)

        pdf_file = os.path.join(UPLOAD_FOLDER, "Executive_Report.pdf")
        generate_pdf_report(analyzed, pdf_file)

        severity_counts = analyzed["Severity"].value_counts().to_dict()

        return render_template("report.html",
                               excel="analysis_output.xlsx",
                               pdf="Executive_Report.pdf",
                               graph="network_graph.png",
                               severity=severity_counts)

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
