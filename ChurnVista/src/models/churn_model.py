import optuna
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, f1_score
import joblib
from src.features.engineering import engineer_features
from src.data.loader import merge_data

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 800),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
    }
    model = XGBClassifier(**params, random_state=42, eval_metric="auc")
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_val)[:, 1]
    return roc_auc_score(y_val, preds)

def train_model():
    df = merge_data()
    df = engineer_features(df)

    feature_cols = [c for c in df.columns if c not in ["customerID", "Churn"]]
    X = df[feature_cols]
    y = df["Churn"]

    global X_train, X_val, y_train, y_val
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=30)

    best_model = XGBClassifier(**study.best_params, random_state=42)
    best_model.fit(X_train, y_train)

    joblib.dump(best_model, "models/best_xgboost.pkl")
    print("Best AUC:", study.best_value)
    return best_model
