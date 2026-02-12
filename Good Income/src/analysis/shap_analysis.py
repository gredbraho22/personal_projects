import shap
import joblib
import pandas as pd
import numpy as np
from src.data.loader import load_data
from src.features.engineering import engineer_features

def generate_shap_summary():
    df = load_data()
    df = engineer_features(df)
    feature_cols = [c for c in df.columns if c != "income"]
    
    model = joblib.load("models/best_xgboost.pkl")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df[feature_cols])
    
    print("Top 10 features by mean absolute SHAP value:")
    shap_importance = pd.DataFrame({
        "feature": feature_cols,
        "mean_abs_shap": np.abs(shap_values).mean(0)
    }).sort_values("mean_abs_shap", ascending=False)
    print(shap_importance.head(10))
