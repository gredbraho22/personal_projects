# QuantForge – Modular Quantitative Research & Trading Toolkit

Production-style quantitative research framework demonstrating:

- Data ingestion (yfinance + Finnhub sentiment)
- Feature engineering (technical indicators)
- Vectorized backtesting engine
- Simple ML signal generation
- Portfolio optimization (via PyPortfolioOpt)
- Interactive Streamlit dashboard
- Clean modular structure & configuration

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yourusername/QuantForge.git
cd QuantForge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get a free Finnhub API key → https://finnhub.io/register
#    Put it in config.yaml or as environment variable FINNHUB_API_KEY

# 4. Run the dashboard
streamlit run src/dashboard/app.py
