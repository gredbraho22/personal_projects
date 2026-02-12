import streamlit as st
import pandas as pd
import plotly.express as px
from src.data.fetch_prices import get_adjusted_prices
from src.portfolio.risk_parity import risk_parity_weights
from src.portfolio.hrp import hrp_weights
from src.portfolio.backtest import run_backtest
from src.config import config

st.set_page_config(page_title="RiskParityEngine", layout="wide")
st.title("RiskParityEngine – Modern Risk Parity Portfolios")

tickers = st.multiselect("Select assets", config.assets["tickers"], default=config.dashboard["default_tickers"])

if not tickers:
    st.stop()

prices = get_adjusted_prices()[tickers]
returns = prices.pct_change().dropna()

cov = returns.cov() * 252

col1, col2 = st.columns(2)

with col1:
    st.subheader("Classic Risk Parity Weights")
    rp_weights = risk_parity_weights(cov)
    fig_rp = px.pie(names=tickers, values=rp_weights, title="Risk Parity Allocation")
    st.plotly_chart(fig_rp)

with col2:
    st.subheader("Hierarchical Risk Parity Weights")
    hrp_w = hrp_weights(returns)
    fig_hrp = px.pie(names=hrp_w.index, values=hrp_w.values, title="HRP Allocation")
    st.plotly_chart(fig_hrp)

st.subheader("Backtest Comparison")

if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        rp_w_df = pd.DataFrame([rp_weights], index=[returns.index[0]], columns=tickers).reindex(returns.index, method="ffill")
        hrp_w_df = pd.DataFrame([hrp_w], index=[returns.index[0]], columns=tickers).reindex(returns.index, method="ffill")

        rp_result = run_backtest(returns, rp_w_df)
        hrp_result = run_backtest(returns, hrp_w_df)

        eq_df = pd.DataFrame({
            "Risk Parity": rp_result["equity"],
            "HRP": hrp_result["equity"]
        })

        fig_eq = px.line(eq_df, title="Equity Curve Comparison")
        st.plotly_chart(fig_eq, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.json(rp_result["metrics"])
        with col2:
            st.json(hrp_result["metrics"])
