import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import shap
from src.data.loader import load_data
from src.features.engineering import engineer_features

st.set_page_config(page_title="Good Income", layout="wide")
st.title("Good Income – Census Income Prediction & Fairness")

df_raw = load_data()
df = engineer_features(df_raw)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["EDA", "Predictions", "SHAP", "Fairness", "Feature Importance"])

with tab1:
    st.subheader("Income Distribution by Education")
    fig = px.histogram(df_raw, x="education", color="income", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    model = joblib.load("models/best_xgboost.pkl")
    feature_cols = [c for c in df.columns if c != "income"]
    probs = model.predict_proba(df[feature_cols])[:, 1]
    df["Predicted_Prob"] = probs
    st.dataframe(df[["age", "education", "sex", "Predicted_Prob"]].head(15))

with tab3:
    st.subheader("SHAP Summary Plot")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df[feature_cols])
    fig = shap.summary_plot(shap_values, df[feature_cols], show=False)
    st.pyplot(fig)

with tab4:
    st.subheader("Fairness by Sex & Race")
    st.write("Run `python -m src.analysis.fairness` in terminal for detailed metrics")

with tab5:
    st.subheader("Top Features")
    st.write("Capital-gain, education-num, and marital-status dominate predictions (see terminal output)")

st.caption("Good Income • UCI Adult Dataset • Fully reproducible")
