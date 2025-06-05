import os
import sys
import json
import pickle
import pytest
import pandas as pd
from sklearn.metrics import accuracy_score

# Ensure src directory is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.exception import ProjectException

# Paths
MODEL_PATH = "model_training/model.pkl"
ENCODER_PATH = "model_training/label_encoders.pkl"
METRICS_PATH = "model_training/metrics.json"

# Shared fixture: Load model and encoders once
@pytest.fixture(scope="module")
def model_and_encoders():
    assert os.path.exists(MODEL_PATH), "❌ Model file is missing."
    assert os.path.exists(ENCODER_PATH), "❌ Label encoders file is missing."

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(ENCODER_PATH, "rb") as f:
        encoders = pickle.load(f)

    return model, encoders


# ✅ 1. Test presence of essential files
def test_files_exist():
    assert os.path.exists(MODEL_PATH), "Model file not found."
    assert os.path.exists(ENCODER_PATH), "Encoder file not found."


# ✅ 2. Test prediction with valid input
def test_valid_prediction(model_and_encoders):
    model, encoders = model_and_encoders

    sample = {
        "Outlook": "Sunny",
        "Temperature": "Cool",
        "Humidity": "Normal",
        "Windy": "Weak"
    }

    encoded = {
        col: encoders[col].transform([val])[0]
        for col, val in sample.items()
    }
    df = pd.DataFrame([encoded])
    prediction = model.predict(df)
    result = encoders["Play"].inverse_transform(prediction)[0]

    assert result in ["Yes", "No"], f"Invalid prediction result: {result}"


# ✅ 3. Test invalid input raises custom exception
def test_invalid_input_raises(model_and_encoders):
    model, encoders = model_and_encoders

    invalid_sample = {
        "Outlook": "Raain",  # Misspelled
        "Temperature": "Cool",
        "Humidity": "Normal",
        "Windy": "Weak"
    }

    with pytest.raises(ProjectException):
        try:
            _ = {
                col: encoders[col].transform([val])[0]
                for col, val in invalid_sample.items()
            }
        except Exception as e:
            raise ProjectException(e, sys)


# ✅ 4. Test model accuracy > 60%
def test_saved_accuracy_above_60():
    assert os.path.exists(METRICS_PATH), "metrics.json not found. Run training first."

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    acc = metrics.get("accuracy", 0)
    print(f"📊 Loaded model accuracy: {acc * 100:.2f}%")
    assert acc >= 0.6, f"❌ Model accuracy is too low: {acc:.2f}"
