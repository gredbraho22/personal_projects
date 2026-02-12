# Demand Metric – Retail Demand Forecasting & Monitoring System

End-to-end probabilistic demand forecasting pipeline for retail/e-commerce time series.

**Focus areas demonstrated:**
- Multi-horizon forecasting with uncertainty quantification
- Classical (Prophet) + gradient boosting (LightGBM) + simple ensemble
- Rich feature engineering (calendar, lags, promotions)
- Model explainability via SHAP
- Basic causal inference stub (synthetic control style)
- Interactive monitoring dashboard (forecasts, residuals, drift alerts)
- Clean, modular, config-driven structure

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/Demand-Metric.git
cd Demand-Metric
pip install -r requirements.txt
# Put your data in data/ or adjust config.yaml
streamlit run src/dashboard/app.py
