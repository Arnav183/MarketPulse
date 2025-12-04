# MarketPulse 📊

**Strategic Market Intelligence Dashboard**
*Built with Python, Streamlit, Plotly, & yFinance*

## 📖 Overview
MarketPulse is a financial analytics tool designed to bridge the gap between raw price data and actionable business insights. It supports analysis across 8,000+ equities, utilizing a custom "Business Phase" engine to determine market states.

## 🚀 Key Features
* **Business Phase Engine:** Automatically translates historical price data into binary "Expansion" vs. "Contraction" states based on technical trend analysis.
* **Strategic Dashboard:** Interactive visualizations using Plotly to track ticker performance against sector benchmarks.
* **Automated ETL Pipeline:** A streamlined data extraction process that reduces manual data aggregation time by ~90%.

## 🛠 Tech Stack
* **Frontend:** Streamlit
* **Data Processing:** Pandas, NumPy, yFinance
* **Visualization:** Plotly Graph Objects

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
