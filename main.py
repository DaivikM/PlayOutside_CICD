import sys
import pickle
import pandas as pd
from src.logger import setup_logger
from src.exception import ProjectException

# Initialize logger
logger = setup_logger()

try:
    # Predicting the result
    with open('model_training/model.pkl', 'rb') as file:
        model = pickle.load(file)
    with open('model_training/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)

    input_sample = {
        'Outlook': 'Raain',
        'Temperature': 'Cool',
        'Humidity': 'Normal',
        'Windy': 'Weak'
    }

    # Encode using same label encoders
    encoded_sample = {col: label_encoders[col].transform([val])[0] for col, val in input_sample.items()}
    input_df = pd.DataFrame([encoded_sample])

    prediction = model.predict(input_df)

    # Decode the prediction back to "Yes"/"No"
    result = label_encoders['Play'].inverse_transform(prediction)

    print("Can play outside?", result[0])

    # Log the prediction
    logger.info(f"Input: {input_sample} | Prediction: {prediction}")

except Exception as e:
    raise ProjectException(e, sys)
