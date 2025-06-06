import streamlit as st
import requests

# API_URL = "http://127.0.0.1:8000/predict/"  # Change if your FastAPI runs elsewhere
import os
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict/")

st.title("Play Outside Predictor")
st.write("Enter the weather conditions to predict if you can play outside.")

# Define options for dropdowns matching your Literal types
outlook_options = ["Sunny", "Overcast", "Rain"]
temperature_options = ["Hot", "Mild", "Cool"]
humidity_options = ["High", "Normal"]
windy_options = ["Weak", "Strong"]

# Create form inputs
with st.form(key="weather_form"):
    outlook = st.selectbox("Outlook", outlook_options, index=0)
    temperature = st.selectbox("Temperature", temperature_options, index=2)
    humidity = st.selectbox("Humidity", humidity_options, index=1)
    windy = st.selectbox("Windy", windy_options, index=0)

    submit_button = st.form_submit_button(label="Predict")

if submit_button:
    # Prepare JSON payload
    payload = {
        "Outlook": outlook,
        "Temperature": temperature,
        "Humidity": humidity,
        "Windy": windy
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        prediction = response.json().get("Prediction")
        if prediction=="Yes":
            st.success("Enjoy, You can play Outside")
        else:
            st.success("Sorry, You can not play Outside")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
