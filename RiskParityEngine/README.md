# RiskParityEngine

Modern risk-parity portfolio construction & realistic backtesting framework.

**Key features**
- Classic risk parity (equal risk contribution)
- Hierarchical Risk Parity (HRP) – often outperforms classical RP in real markets
- Volatility targeting + dynamic leverage
- Transaction cost & slippage modeling
- Drawdown control & rebalancing rules
- Realistic performance metrics (Calmar, ulcer index, rolling Sharpe, etc.)
- Interactive Streamlit dashboard

**Quick start**

```bash
git clone https://github.com/YOUR_USERNAME/RiskParityEngine.git
cd RiskParityEngine
pip install -r requirements.txt
streamlit run src/dashboard/app.py
