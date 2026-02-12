from dowhy import CausalModel
import pandas as pd
from src.data.loader import merge_data

def run_causal_analysis():
    df = merge_data()
    df["Promotion"] = (df["MonthlyCharges"] < df["MonthlyCharges"].median()).astype(int)  # proxy

    model = CausalModel(
        data=df,
        treatment="Promotion",
        outcome="Churn",
        common_causes=["tenure", "Contract", "SeniorCitizen"]
    )
    identified = model.identify_effect()
    estimate = model.estimate_effect(identified, method_name="backdoor.linear_regression")
    print("Average Treatment Effect of Promotion on Churn:", estimate.value)
