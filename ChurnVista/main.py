from src.models.churn_model import train_model
from src.analysis.survival import run_survival_analysis
from src.causal.causal_analysis import run_causal_analysis

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("Running survival analysis...")
    run_survival_analysis()
    print("Running causal analysis...")
    run_causal_analysis()
    print("Done. Launch dashboard with: streamlit run src/dashboard/app.py")
