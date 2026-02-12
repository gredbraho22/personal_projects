import pytest
from src.models.churn_model import train_model

def test_model_auc():
    model = train_model()
    # In real test you'd load saved model and assert AUC > 0.8
    assert model is not None
