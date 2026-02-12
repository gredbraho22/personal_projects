# Quant Forge
**Modular Quantitative Trading & Portfolio Optimization Platform**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-5B4636?style=flat&logoColor=white)](https://xgboost.readthedocs.io/)
[![PyPortfolioOpt](https://img.shields.io/badge/PyPortfolioOpt-3776AB?style=flat)](https://pyportfolioopt.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

End-to-end quantitative research & trading toolkit built in Python.  
Demonstrates production-grade design: clean modular architecture, real data pipelines, machine learning signals, vectorized backtesting, risk management, portfolio optimization, and an interactive Streamlit dashboard.

Ideal for showcasing skills to quant desks, data science teams, and algorithmic trading roles at top tech & finance firms.

### Key Features

- Multi-asset historical price data via **yfinance** + news sentiment via **Finnhub** (free tier)
- 20+ technical indicators (RSI, MACD, Bollinger Bands, ATR, etc.) using **pandas_ta**
- Custom **vectorized backtester** with transaction costs, realistic position sizing & slippage proxy
- **XGBoost** classifier for next-day directional prediction & signal generation
- Portfolio construction: **Max Sharpe**, **Hierarchical Risk Parity (HRP)**, **Min-CVaR**
- Risk analytics: **VaR**, **CVaR**, max drawdown, rolling Sharpe
- Beautiful, interactive **Streamlit dashboard** with Plotly charts (equity curves, metrics, weights)
- Fully config-driven (YAML) singleton config — no hard-coded values
- Modular OOP structure under `src/` — easy to extend or productionize

### Architecture Overview

```mermaid
graph TD
    A[Raw Data<br>yfinance + Finnhub API] --> B[Data Collector]
    B --> C[Feature Engineering<br>TA indicators + Sentiment]
    C --> D[ML Models<br>XGBoost Classifier]
    D --> E[Signal Generation<br>Long / Short / Neutral]
    A --> F[Portfolio Optimizer<br>Max Sharpe / HRP / Min CVaR]
    E --> G[Vectorized Backtester<br>With costs & position sizing]
    G --> H[Risk Module<br>VaR / CVaR / Drawdown]
    G --> I[Interactive Dashboard<br>Streamlit + Plotly]
    F --> I
    H --> I
    style I fill:#f9f,stroke:#333,stroke-width:2px
