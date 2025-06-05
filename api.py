from fastapi import FastAPI, HTTPException, Body
import pandas as pd
import sys
from src.schema import WeatherInput
from src.exception import ProjectException
from src.utils import load_model_and_encoders, preprocess_and_predict
from src.logger import setup_logger

# Initialize app and logger
app = FastAPI(title="Play Outside Predictor API", description="An API to predict if someone can play outside based on weather conditions.")
logger = setup_logger()

# Load model and encoders
try:
    model, label_encoders = load_model_and_encoders()
except Exception as e:
    logger.error("Failed to load model or encoders.")
    raise ProjectException(e, sys)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running. Use /predict to get a prediction."}

@app.get("/health")
def health_check():
    try:
        assert model is not None
        assert label_encoders is not None
        return {"status": "ok", "message": "Model and encoders are loaded."}
    except Exception:
        raise HTTPException(status_code=503, detail="Model not available")

@app.post("/predict/", summary="Predict playability", description="Predicts whether one can play outside based on weather conditions.")
def predict(
    data: WeatherInput = Body(
        ..., 
        description="Input features for weather condition",
        example={
            "Outlook": "Sunny",
            "Temperature": "Cool",
            "Humidity": "Normal",
            "Windy": "Weak"
        }
    )
):
    try:
        input_sample = data.dict()
        result = preprocess_and_predict(input_sample, model, label_encoders)
        logger.info(f"Input: {input_sample} | Prediction: {result}")
        return {"Prediction": result}

    except Exception as e:
        logger.error("Prediction failed.")
        raise ProjectException(e, sys)
