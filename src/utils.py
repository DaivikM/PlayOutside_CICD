# src/utils.py

import pickle
import sys
import pandas as pd
from typing import Dict
from src.config import MODEL_PATH, ENCODER_PATH
from src.exception import ProjectException


def load_pickle_file(path: str):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise ProjectException(e, sys)

def load_model_and_encoders():
    model = load_pickle_file(MODEL_PATH)
    encoders = load_pickle_file(ENCODER_PATH)
    return model, encoders

def preprocess_and_predict(input_sample: Dict[str, str], model, label_encoders) -> str:
    """
    Encodes the input, performs prediction, and decodes the output.
    """
    try:
        # Encode input
        encoded_sample = {
            col: label_encoders[col].transform([val])[0]
            for col, val in input_sample.items()
        }

        df = pd.DataFrame([encoded_sample])

        # Predict and decode
        prediction = model.predict(df)
        result = label_encoders['Play'].inverse_transform(prediction)[0]
        return result

    except Exception as e:
        raise ProjectException(e, sys)
