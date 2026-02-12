from src.models.train import train_model
from src.analysis.fairness import fairness_analysis
from src.analysis.shap_analysis import generate_shap_summary

if __name__ == "__main__":
    print("Training model...")
    train_model()
    print("\nRunning fairness analysis...")
    fairness_analysis()
    print("\nGenerating SHAP summary...")
    generate_shap_summary()
    print("\nAll done! Launch dashboard with: streamlit run src/dashboard/app.py")
