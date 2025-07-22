import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Load the saved model
with open("rainfall_model.pkl", "rb") as f:
    model = pickle.load(f)

# Assumed maximum rainfall for % calculation
MAX_RAINFALL_MM = 100.0  # Change this to actual max from your dataset if known

# Function to determine chance of rain based on mm
def get_chance_of_rain(mm):
    if mm < 1:
        return 10
    elif mm < 5:
        return 30
    elif mm < 10:
        return 60
    elif mm < 20:
        return 80
    else:
        return 95

# Streamlit UI
st.set_page_config(page_title="Rainfall Predictor", page_icon="🌧️", layout="centered")

st.title("🌧️ Rainfall Prediction Based on Date")
st.markdown(
    """
    Predict the **rainfall (in mm)**, **rainfall percentage**, and **chance of rain** for any date using a trained ML model.
    """
)

# Date input
selected_date = st.date_input("Select a date to predict rainfall")

# Predict button
if st.button("Predict Rainfall"):
    # Extract features
    day = selected_date.day
    month = selected_date.month
    weekday = selected_date.weekday()

    input_df = pd.DataFrame({
        'day': [day],
        'month': [month],
        'weekday': [weekday]
    })

    # Predict rainfall in mm
    prediction_mm = model.predict(input_df)[0]

    # Calculate rainfall percentage
    prediction_percent = min((prediction_mm / MAX_RAINFALL_MM) * 100, 100)

    # Get chance of rain based on mm
    chance_of_rain = get_chance_of_rain(prediction_mm)

    # Display results
    st.success(f"""
    📅 **Date**: {selected_date.strftime('%Y-%m-%d')}

    🌧️ **Predicted Rainfall**: {prediction_mm:.2f} mm  
    💧 **Rainfall Percentage**: {prediction_percent:.1f}% of max  
    ☔ **Chance of Rain**: {chance_of_rain}%
    """)
