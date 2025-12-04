import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import feedparser

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="MarketPulse Intelligence")

# --- HELPER FUNCTIONS ---

@st.cache_data
def convert_df(df):
    """Converts a dataframe to CSV for download."""
    return df.to_csv().encode('utf-8')

def format_large_number(num):
    if num is None: return "N/A"
    if num >= 1_000_000_000_000: return f"${num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000: return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000: return f"${num / 1_000_000:.2f}M"
    else: return f"${num:,.2f}"

def calculate_metrics(data, window=14):
    # RSI (Momentum/Sentiment)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Volatility (Standard Deviation)
    returns = data['Close'].pct_change()
    volatility = returns.rolling(window=14).std() * 100 
    
    return rsi, volatility

def get_market_news(ticker_filter=None):
    try:
        rss_url = "https://www.cnbc.com/id/15839069/device/rss/rss.html"
        feed = feedparser.parse(rss_url)
        market_keywords = ["business", "economy", "regulation", "policy", "growth", 
                           "earnings", "revenue", "strategy", "tech", "sector", "tax"]
        if ticker_filter:
            market_keywords.append(ticker_filter.lower())
        
        filtered_news = []
        for entry in feed.entries:
            title_lower = entry.title.lower()
            if any(keyword in title_lower for keyword in market_keywords):
                filtered_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "source": "CNBC"
                })
        return filtered_news[:5]
    except Exception:
        return []

# --- SIDEBAR ---
if 'ticker' not in st.session_state: st.session_state.ticker = "NVDA"
def update_ticker(): st.session_state.ticker = st.session_state.quick_select

st.sidebar.title("📊 MarketPulse Logic")
st.sidebar.caption("Strategic Intelligence Dashboard")

# Refresh
if st.sidebar.button("🔄 Refresh Analysis"): st.rerun()

st.sidebar.markdown("---")

# Asset Selector
st.sidebar.subheader("🔎 Asset Selector")
popular_tickers = ["NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "SPY", "JPM", "GS", "XOM"]
st.sidebar.selectbox("Quick Select:", options=popular_tickers, key="quick_select", index=None, on_change=update_ticker)
ticker_symbol = st.sidebar.text_input("Ticker Symbol:", key="ticker", help="Enter symbol (e.g., META, JPM)").upper()
time_period = st.sidebar.selectbox("Analysis Horizon", ["3mo", "6mo", "1y", "5y"], index=1)

# --- MAIN APP ---
st.title(f"🏛 {ticker_symbol} Strategic Overview")

ticker = yf.Ticker(ticker_symbol)

try:
    hist = ticker.history(period=time_period)
    # Generate CSV for download immediately if data exists
    if not hist.empty:
        csv_data = convert_df(hist)
        st.sidebar.markdown("---")
        st.sidebar.download_button(
            label="📥 Download Data (CSV)",
            data=csv_data,
            file_name=f"{ticker_symbol}_marketpulse_data.csv",
            mime="text/csv",
            help="Export raw data for Excel analysis."
        )

    try:
        info = ticker.info 
        sector = info.get('sector', 'Diversified')
        market_cap_raw = info.get('marketCap')
        long_name = info.get('longName', ticker_symbol)
        beta = info.get('beta', 1.0)
    except:
        sector = "Unknown"
        market_cap_raw = None
        long_name = ticker_symbol
        beta = 1.0
except Exception:
    st.error("Data unavailable. Check ticker symbol.")
    st.stop()

if not hist.empty:
    st.caption(f"{long_name} | Sector: {sector}")
    
    # --- CALCULATIONS ---
    hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
    hist['RSI'], hist['Volatility'] = calculate_metrics(hist)
    
    current_price = hist['Close'].iloc[-1]
    pct_change = ((current_price - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
    sma_50 = hist['SMA_50'].iloc[-1]
    rsi_val = hist['RSI'].iloc[-1]
    vol_val = hist['Volatility'].iloc[-1]

    # --- TOP METRICS ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Asset Price", f"${current_price:,.2f}", f"{pct_change:.2f}%")
    c2.metric("Market Cap", format_large_number(market_cap_raw))
    c3.metric("Beta (Risk)", f"{beta:.2f}")
    c4.metric("Volatility (14d)", f"{vol_val:.2f}%")
    st.markdown("---")

    # --- STRATEGIC CONTEXT ENGINE ---
    st.subheader("🧩 Strategic Context Analysis")
    
    if len(hist) < 50:
        st.warning("Insufficient data for full trend analysis.")
    else:
        # Trend
        if current_price > sma_50:
            trend_status = "EXPANSION (Growth Phase)"
            trend_desc = "Asset is trading above its 50-day baseline, indicating positive structural momentum."
            trend_color = "#09AB3B"
        else:
            trend_status = "CONTRACTION (Pressure Phase)"
            trend_desc = "Asset is trading below its 50-day baseline, indicating structural headwinds."
            trend_color = "#FF4B4B"

        # Sentiment
        if rsi_val > 70:
            sent_status = "HEATED / ELEVATED ATTENTION"
            sent_desc = "Sentiment is historically stretched. Often correlates with news cycles or hype spikes."
            sent_color = "orange"
        elif rsi_val < 30:
            sent_status = "DEPRESSED / VALUE ZONE"
            sent_desc = "Sentiment is historically low. May indicate over-reaction to negative news."
            sent_color = "#09AB3B" 
        else:
            sent_status = "STABLE / NORMALIZED"
            sent_desc = "Sentiment is within standard deviation. Price movement is likely rational."
            sent_color = "gray"

        # Volatility
        if vol_val > 2.5:
            risk_status = "HIGH VOLATILITY"
            risk_color = "red"
        else:
            risk_status = "STABLE"
            risk_color = "gray"

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"**Structural Trend**<br><h4 style='color:{trend_color}'>{trend_status}</h4>", unsafe_allow_html=True)
            st.caption(trend_desc)
        with col_b:
            st.markdown(f"**Market Sentiment**<br><h4 style='color:{sent_color}'>{sent_status}</h4>", unsafe_allow_html=True)
            st.caption(sent_desc)
        with col_c:
            st.markdown(f"**Volatility Profile**<br><h4 style='color:{risk_color}'>{risk_status}</h4>", unsafe_allow_html=True)
            st.caption(f"Short-term variance is {vol_val:.2f}%.")

    st.markdown("---")

    # --- CHART VISUALIZATION (FIXED) ---
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                        subplot_titles=(f'{ticker_symbol} Price vs Trend', 'Sentiment Index (RSI)'), 
                        row_heights=[0.7, 0.3])

    # 1. Price Chart (Candlestick)
    fig.add_trace(go.Candlestick(x=hist.index,
                                 open=hist['Open'], high=hist['High'],
                                 low=hist['Low'], close=hist['Close'],
                                 name='Price'), row=1, col=1)
    
    # 2. SMA Line (Orange)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_50'], 
                             line=dict(color='orange', width=2), 
                             name='50-Day Trend'), row=1, col=1)

    # 3. RSI Line (Purple)
    fig.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], 
                             line=dict(color='#636EFA', width=2), 
                             name='RSI Sentiment'), row=2, col=1)
    
    # RSI Zones (30/70)
    fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1, annotation_text="Heated (70)")
    fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1, annotation_text="Value (30)")

    # Layout Fixes for "Wonkiness"
    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=False, # Hides the bottom slider that squishes the chart
        showlegend=True,                 # Shows the legend (Price, SMA, RSI)
        legend=dict(orientation="h", y=1.02, xanchor="right", x=1), # Positions legend nicely at top
        template="plotly_white",         # Removes distracting grey background grid
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Lock RSI scale 0-100
    fig.update_yaxes(range=[0, 100], row=2, col=1)

    st.plotly_chart(fig, use_container_width=True)

    # --- NEWS ---
    st.subheader(f"📰 Contextual Drivers: {ticker_symbol}")
    news = get_market_news(ticker_filter=ticker_symbol)
    if news:
        for item in news:
            st.markdown(f"**[{item['title']}]({item['link']})**")
            st.caption(f"{item['source']} • {item['published']}")
            st.write("---")
    else:
        st.info("No specific news drivers found.")

else:
    st.error("Ticker not found.")
