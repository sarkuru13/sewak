import os
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    table = ""
    class_avg = {}
    toppers = {}
    plot_url = None

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)

            # Basic summary table
            table = df.describe().to_html(classes='data', header="true")

            # Class average
            subjects = df.columns[2:]  # skip StudentID and Name
            for subject in subjects:
                class_avg[subject] = round(df[subject].mean(), 2)

            # Toppers
            for subject in subjects:
                top_index = df[subject].idxmax()
                toppers[subject] = df.loc[top_index, 'Name']

            # Plotting - subject wise average bar chart
            plt.figure(figsize=(8, 5))
            plt.bar(class_avg.keys(), class_avg.values())
            plt.ylabel("Average Marks")
            plt.title("Subject-wise Class Average")
            plt.xticks(rotation=45)
            plot_path = os.path.join(PLOT_FOLDER, 'average_plot.png')
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            plot_url = plot_path

    return render_template("index.html", table=table, class_avg=class_avg, toppers=toppers, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
