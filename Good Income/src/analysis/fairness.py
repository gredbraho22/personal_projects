import pandas as pd
from src.data.loader import load_data
from src.features.engineering import engineer_features

def fairness_analysis():
    df = load_data()
    df = engineer_features(df)
    
    print("=== Fairness Analysis by Sex ===")
    for sex in df["sex"].unique():
        subset = df[df["sex"] == sex]
        pos_rate = subset["income"].mean()
        print(f"Sex {sex}: Positive rate = {pos_rate:.4f}")
    
    print("\n=== Fairness Analysis by Race ===")
    for race in df["race"].unique():
        subset = df[df["race"] == race]
        pos_rate = subset["income"].mean()
        print(f"Race {race}: Positive rate = {pos_rate:.4f}")
