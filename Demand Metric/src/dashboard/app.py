import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data.loader import load_raw_data
from src.data.preprocessor import add_time_features
from src.config import config

st.set_page_config(page_title="Demand Metric Dashboard", layout="wide")

st.title("Demand Metric – Demand Forecasting & Monitoring")

# Load data
@st.cache_data
def get_data():
    df = load_raw_data()
    df = add_time_features(df)
    return df

df = get_data()

# Filters
group_key = st.selectbox(
    "Select series",
    options=df.groupby(config.data["group_cols"]).size().index.map(lambda x: "-".join(map(str, x))),
    index=0
)

group_filter = group_key.split("-")
filtered_df = df[
    (df[config.data["group_cols"][0]] == group_filter[0]) &
    (df[config.data["group_cols"][1]] == group_filter[1])
]

st.subheader(f"Sales history – {group_key}")

fig_hist = px.line(filtered_df, x=config.data["date_col"], y=config.data["target_col"],
                   title="Historical Sales")
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Forecast Placeholder")
st.info("Connect Prophet / LightGBM forecasts here. Add quantile fan chart.")

# Simple future dates placeholder
horizon = st.slider("Forecast horizon (days)", 7, 90, config.forecast["horizon_days"])
future_dates = pd.date_range(filtered_df[config.data["date_col"]].max() + pd.Timedelta(days=1), periods=horizon)

st.caption("Forecast visualization would appear here with upper/lower bounds")

st.markdown("---")
st.caption("Demand Metric v0.1 | Add models & SHAP in production version")
