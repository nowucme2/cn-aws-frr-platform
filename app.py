from flask import Flask, render_template, request
import pandas as pd
from engine2 import analyze
from graph_generator import generate_network_graph
from pdf_report import generate_pdf_report

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        df = pd.read_excel(file)
        analyzed, attack_chain_df = analyze(df)

        graph_file = generate_network_graph(analyzed)
        pdf_file = generate_pdf_report(analyzed)

        return render_template("report.html",
                               graph=graph_file,
                               pdf=pdf_file)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
