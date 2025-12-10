# Time-Series AI Insight Summarizer

A Flask web application that provides **AI-assisted time-series data analysis**.  
Upload your CSV dataset with a timestamp column, and the app will automatically:

- Detect trends in numeric columns  
- Identify anomalies using z-score  
- Generate rolling averages  
- Produce narrative insights  
- Generate time-series plots with anomalies highlighted  
- Store uploaded datasets and analyses in **SQLite** for easy retrieval  

---

## **Project Structure**

```

flask-ts-ai-insights/
├── app.py                 # Main Flask app + AI agent logic
├── database.py            # SQLite helper functions
├── requirements.txt
├── Procfile               # For deployment (Heroku / Render)
├── Dockerfile
├── .gitignore
├── README.md
├── templates/
│   ├── index.html
│   └── results.html
├── static/
│   ├── plots/             # Generated plot PNGs
│   └── css/
│       └── styles.css
└── sample_data/
└── sample.csv

````

---

## **Features**

- **Time-Series Analysis**: Automatically detects the time column and analyzes numeric data.  
- **Trend Detection**: Linear trend slope per numeric column.  
- **Anomaly Detection**: Highlights values with z-score > 2.  
- **Rolling Averages**: Default 7-day rolling average visualizations.  
- **SQLite Database**: Stores uploaded datasets and AI-generated analyses.  
- **Interactive Plots**: View results in a simple Flask UI.  

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/Rishitha-789/Time-Series-AI-Insight-Summarizer.git
cd flask-ts-ai-insights
````

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run the App Locally**

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## **Usage**

1. Click **“Choose File”** and upload a CSV file containing a time column (e.g., `date` or `timestamp`).
2. Click **Analyze**.
3. View AI-generated insights and plots highlighting trends, anomalies, and rolling averages.

**Example CSV:**

```csv
date,sales,temperature
2023-01-01,100,30
2023-01-02,120,31
2023-01-03,115,29
2023-01-04,130,32
2023-01-05,90,28
```

---

## **Deployment**

### **1. Using Gunicorn (Production)**

```bash
gunicorn app:app
```

### **2. Docker Deployment**

```bash
docker build -t flask-ts-ai-insights .
docker run -p 5000:5000 flask-ts-ai-insights
```
---

## **Database**

* `data.db` (SQLite) is created automatically on first run.
* Tables:

  * `datasets`: Stores uploaded dataset filenames and upload timestamps.
  * `analyses`: Stores insights, plot file names, and timestamps.

---

## **Future Enhancements**

* Generate **PDF/HTML reports** automatically combining plots and insights.
* Detect **seasonality** using autocorrelation or Fourier analysis.
* Allow user-defined **rolling window and anomaly thresholds**.
* Integrate LLM (e.g., OpenAI GPT) for richer narrative insights.

---
