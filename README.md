# MarketPulse 📊

**Strategic Market Intelligence Dashboard**
*Built with Python, Streamlit, Plotly, & yFinance*

## 📖 Overview
MarketPulse is a financial analytics tool designed to bridge the gap between raw price data and actionable business insights. It supports analysis across 8,000+ equities, utilizing a custom "Strategic Context Engine" to determine market states.

## 🚀 Key Features
* **Business Phase Engine:** Algorithmically translates price data into "Expansion" vs. "Contraction" phases using 50-day trend baselines.
* **Sentiment Analysis:** Integrated RSI (Relative Strength Index) logic to detect "Heated" vs. "Value" zones.
* **Automated ETL Pipeline:** One-click CSV extraction reduces manual data aggregation time by ~90%.
* **Contextual News:** Real-time RSS integration fetches specific drivers for the analyzed asset.

## 🛠 Tech Stack
* **Frontend:** Streamlit
* **Data Processing:** Pandas, NumPy, yFinance
* **Visualization:** Plotly Graph Objects
* **External Data:** Feedparser (RSS)

## 💻 How to Run
1.  Clone the repository:
    ```bash
    git clone [https://github.com/arnav183/MarketPulse.git](https://github.com/arnav183/MarketPulse.git)
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the dashboard:
    ```bash
    streamlit run app.py
    ```
