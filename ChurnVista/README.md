# ChurnVista – Advanced Customer Churn Analysis Platform

Complex end-to-end data science project demonstrating production-level analysis for customer retention.

**Key Components**
- Data ingestion & cleaning (customer + transaction merge)
- Deep EDA + statistical tests + cohort analysis
- Feature engineering (RFM, LTV, interaction terms)
- Survival analysis (lifelines)
- ML pipeline with Optuna hyperparameter tuning
- Explainability (SHAP) + fairness
- Causal inference (DoWhy)
- Customer segmentation (KMeans)
- Interactive Streamlit dashboard (6 tabs)

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ChurnVista.git
cd ChurnVista
pip install -r requirements.txt
streamlit run src/dashboard/app.py
