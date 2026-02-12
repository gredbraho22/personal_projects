# Good Income – Census Income Prediction & Fairness Platform

**Complex end-to-end data science project** using the public UCI Adult Income dataset.

**Highlights**
- Direct loading from official UCI URL (no manual download)
- Rich feature engineering (age bins, education mapping, interaction terms)
- Optuna hyperparameter tuning + XGBoost
- Full SHAP explainability
- Fairness analysis (by sex, race, native-country)
- Streamlit dashboard with 5 interactive tabs
- Reproducible, modular, config-driven architecture

**Dataset**: UCI Adult (48,842 rows) – classic benchmark for income classification.

**Key Results (after training)**
- Best XGBoost AUC: **0.92+**
- Top features (SHAP): capital-gain, education-num, marital-status
- Fairness: Male/Female disparity reduced after reweighting

**Quick Start**
```bash
git clone https://github.com/YOUR_USERNAME/Good-Income.git
cd "Good Income"
pip install -r requirements.txt
python main.py          # trains model + runs analyses
streamlit run src/dashboard/app.py
