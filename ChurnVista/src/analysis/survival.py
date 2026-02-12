from lifelines import KaplanMeierFitter, CoxPHFitter
import pandas as pd
from src.data.loader import merge_data

def run_survival_analysis():
    df = merge_data()
    kmf = KaplanMeierFitter()
    kmf.fit(durations=df["tenure"], event_observed=df["Churn"] == "Yes")
    print("Median survival time:", kmf.median_survival_time_)

    cph = CoxPHFitter()
    cph.fit(df, duration_col="tenure", event_col="Churn", formula="MonthlyCharges + Contract + SeniorCitizen")
    cph.print_summary()
