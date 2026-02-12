import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import config
from src.data.collector import DataCollector
from src.features.engineering import engineer_features
from src.backtesting.engine import VectorizedBacktester, simple_momentum_signals


st.set_page_config(page_title="QuantForge Dashboard", layout="wide")

st.title("QuantForge – Quantitative Research Dashboard")
st.markdown("Multi-asset data pipeline, technical features, backtesting & visualization")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    selected_tickers = st.multiselect(
        "Select tickers",
        options=config.tickers,
        default=config.default_dashboard_tickers[:3]
    )
    use_sentiment = st.checkbox("Include Finnhub sentiment (if available)", value=False)
    backtest_window = st.slider("Momentum SMA window (days)", 20, 200, 50)


if not selected_tickers:
    st.warning("Please select at least one ticker.")
    st.stop()


# Data loading
@st.cache_data(ttl=3600)  # cache 1 hour
def load_data(tickers):
    collector = DataCollector()
    prices = collector.get_price_data(tickers)

    sentiment_dfs = []
    if use_sentiment:
        for t in tickers:
            sent = collector.get_sentiment_data(t)
            if not sent.empty:
                sentiment_dfs.append(sent)
    sentiment = pd.concat(sentiment_dfs, axis=1) if sentiment_dfs else None

    return prices, sentiment


prices, sentiment = load_data(selected_tickers)

if prices.empty:
    st.error("No price data retrieved. Check date range or internet connection.")
    st.stop()


# Features & signals
features = engineer_features(prices, include_sentiment=use_sentiment, sentiment_df=sentiment)

# Placeholder strategy: simple momentum
signals = simple_momentum_signals(prices, window=backtest_window)

# Backtest
bt = VectorizedBacktester(prices, signals)
results = bt.run()


# ──────────────────────────────────────────────
#               Visualizations
# ──────────────────────────────────────────────

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Equity Curve")
    fig_eq = px.line(
        results["equity_curve"],
        title="Strategy Equity Curve",
        labels={"value": "Portfolio Value ($)", "index": "Date"}
    )
    fig_eq.update_layout(showlegend=False)
    st.plotly_chart(fig_eq, use_container_width=True)

with col2:
    st.subheader("Performance Metrics")
    m = results["metrics"]
    st.metric("Total Return", f"{m['total_return']:.2%}")
    st.metric("Annualized Return", f"{m['annualized_return']:.2%}")
    st.metric("Sharpe Ratio", f"{m['sharpe_ratio']:.2f}")
    st.metric("Max Drawdown", f"{m['max_drawdown']:.2%}")

st.subheader("Price & Signals (last 2 years)")
recent_prices = prices.tail(504)  # ~2 years trading days

fig_prices = go.Figure()
for col in recent_prices.columns:
    fig_prices.add_trace(go.Scatter(
        x=recent_prices.index,
        y=recent_prices[col],
        name=col,
        mode='lines'
    ))
st.plotly_chart(fig_prices, use_container_width=True)

# Optional: raw data explorer
with st.expander("View raw prices & features (preview)"):
    st.dataframe(prices.tail(10))
    if not features.empty:
        st.dataframe(features.tail(10))

st.markdown("---")
st.caption("QuantForge v0.1 | Built for demonstration | Data: yfinance + Finnhub")
