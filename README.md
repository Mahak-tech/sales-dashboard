# 📊 Sales Dashboard with Sentiment Analysis

An interactive sales analytics dashboard built with **Streamlit**, **Plotly**, and **TextBlob** (for customer
review sentiment analysis). Runs locally in VS Code and opens in your browser at `localhost`.

---

## 📁 Project Structure

```
sales_dashboard/
│
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── generate_data.py           # Script used to generate the sample dataset (optional, already run)
├── README.md                  # This file
│
├── data/
│   └── sales_data.csv         # Sample sales + customer review dataset (400 records)
│
└── utils/
    ├── __init__.py
    └── sentiment.py           # TextBlob sentiment analysis helper functions
```

---

## ✅ Prerequisites

- **Python 3.9+** installed ([python.org/downloads](https://www.python.org/downloads/))
- **VS Code** installed ([code.visualstudio.com](https://code.visualstudio.com/))
- VS Code **Python extension** installed (from the Extensions marketplace, search "Python" by Microsoft)

---

## 🚀 Step-by-Step: Run in VS Code

### 1. Unzip and open the project
- Unzip `sales_dashboard.zip` to a folder of your choice.
- Open **VS Code** → `File` → `Open Folder` → select the unzipped `sales_dashboard` folder.

### 2. Open a terminal in VS Code
- Go to `Terminal` → `New Terminal` (or press `` Ctrl+` ``).

### 3. Create a virtual environment (recommended)

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

> In VS Code, you can also select this environment as your interpreter:
> `Ctrl+Shift+P` → `Python: Select Interpreter` → choose the `venv` one.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download TextBlob's corpora (one-time setup)
TextBlob needs some NLTK corpora for text processing:
```bash
python -m textblob.download_corpora
```

### 6. Run the Streamlit app
```bash
streamlit run app.py
```

### 7. View the dashboard
- Streamlit will automatically open your default browser at:
  ```
  http://localhost:8501
  ```
- If it doesn't open automatically, copy that URL into your browser manually.
- The terminal will also show a **Network URL** if you want to access it from another device on the same network.

### 8. Stop the app
- Go back to the VS Code terminal and press `Ctrl + C`.

---

## 🧩 What the Dashboard Includes

- **Sidebar filters**: date range, category, region, salesperson
- **KPI cards**: total revenue, units sold, average order value, % positive reviews, average sentiment polarity
- **Revenue trend** line chart (weekly)
- **Revenue by category** donut chart
- **Revenue by region** bar chart
- **Top 5 products** by units sold
- **Sentiment distribution** (Positive / Neutral / Negative) via TextBlob polarity scoring
- **Sentiment by category** stacked bar chart
- **Polarity vs. Subjectivity** scatter plot (hover to see the review text)
- **Detailed data table** with a CSV download button

---

## 🔄 Using Your Own Data

Replace `data/sales_data.csv` with your own file, keeping these column names (or update `app.py` accordingly):

| Column           | Type   | Description                          |
|------------------|--------|---------------------------------------|
| Date             | date   | Sale date (YYYY-MM-DD)                |
| Product          | text   | Product name                          |
| Category         | text   | Product category                      |
| Region           | text   | Sales region                          |
| Salesperson      | text   | Name of salesperson                   |
| Units Sold       | number | Quantity sold                         |
| Unit Price       | number | Price per unit                        |
| Revenue          | number | Total revenue for that record         |
| Customer Review  | text   | Free-text customer review for sentiment analysis |

If you only want to regenerate the sample data, run:
```bash
python generate_data.py
```

---

## 🛠️ Troubleshooting

- **`streamlit: command not found`** → Make sure your virtual environment is activated and dependencies are installed.
- **Port already in use** → Run `streamlit run app.py --server.port 8502` to use a different port.
- **TextBlob errors about missing corpora** → Re-run `python -m textblob.download_corpora`.
- **Blank dashboard / no data** → Ensure `data/sales_data.csv` exists relative to `app.py`.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — interactive charts
- [TextBlob](https://textblob.readthedocs.io/) — sentiment analysis (polarity & subjectivity)
- [Pandas](https://pandas.pydata.org/) — data handling
