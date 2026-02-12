import pytest
import numpy as np
from src.portfolio.risk_parity import risk_parity_weights

def test_risk_parity():
    cov = np.eye(3) * 0.04  # identity cov → equal weights expected
    w = risk_parity_weights(cov)
    assert np.allclose(w, [1/3, 1/3, 1/3], atol=1e-4)
