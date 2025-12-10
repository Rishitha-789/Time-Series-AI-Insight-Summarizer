from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from database import init_db, save_dataset, save_analysis

app = Flask(__name__)
UPLOAD_FOLDER = 'sample_data'
PLOT_FOLDER = 'static/plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

init_db()

#AI Agent Functions

def run_time_series_agent(df):
    """Generate narrative insights for time-series numeric data"""
    insights = []

    # Detect time column
    time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if not time_cols:
        return "No time column detected. Provide a timestamp column."

    time_col = time_cols[0]
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df = df.sort_values(by=time_col)

    insights.append(f"Time column: {time_col}")
    insights.append(f"Dataset range: {df[time_col].min().date()} to {df[time_col].max().date()}")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if numeric_cols.empty:
        return "No numeric columns found for analysis."

    for col in numeric_cols:
        series = df[col].fillna(method='ffill')
        z = (series - series.mean()) / series.std()
        anomalies = series[np.abs(z) > 2]

        trend = np.polyfit(range(len(series)), series.values, 1)
        slope = trend[0]

        insights.append(f"\nColumn: {col}")
        insights.append(f"  Mean: {series.mean():.2f}, Std: {series.std():.2f}")
        insights.append(f"  Trend slope: {slope:.4f}")
        insights.append(f"  Anomalies detected: {len(anomalies)}")

    return "\n".join(insights)

def generate_time_series_plots(df):
    """Generate time-series plots with rolling average and anomaly detection"""
    plot_files = []

    time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if not time_cols:
        return plot_files

    time_col = time_cols[0]
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df = df.sort_values(by=time_col)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    for col in numeric_cols:
        series = df[col].fillna(method='ffill')
        plt.figure(figsize=(10,5))
        plt.plot(df[time_col], series, label='Original', color='blue')

        # Rolling average
        rolling = series.rolling(7).mean()
        plt.plot(df[time_col], rolling, label='7-day Rolling Avg', color='orange')

        # Anomalies
        z = (series - series.mean()) / series.std()
        anomalies = df[time_col][np.abs(z) > 2]
        anomaly_vals = series[np.abs(z) > 2]
        plt.scatter(anomalies, anomaly_vals, color='red', label='Anomalies')

        plt.title(f"Time Series: {col}")
        plt.xlabel(time_col)
        plt.ylabel(col)
        plt.legend()

        f = f"ts_{col}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
        plt.savefig(os.path.join(PLOT_FOLDER, f))
        plt.close()
        plot_files.append(f)

    return plot_files

#Flask Routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'dataset' not in request.files:
        return redirect(url_for('index'))

    file = request.files['dataset']
    if file.filename == '':
        return redirect(url_for('index'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    # Save dataset in DB
    dataset_id = save_dataset(file.filename)

    # Run AI agent
    insights = run_time_series_agent(df)
    plots = generate_time_series_plots(df)

    # Save analysis in DB
    save_analysis(dataset_id, insights, plots)

    return render_template('results.html', insights=insights, plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
