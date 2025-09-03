import streamlit as st
import joblib
import numpy as np

# Load trained model and encoder
model = joblib.load("cyber_model.pkl")
label_encoder = joblib.load("attack_label_encoder.pkl")

st.title("🛡️ Cyberattack Type Predictor")

# Dropdown choices (you can expand based on your dataset)
country_options = {"USA": 0, "India": 1, "UK": 2, "Germany": 3, "China": 4}
industry_options = {"IT": 0, "Healthcare": 1, "Banking": 2, "Government": 3}
source_options = {"Hacker Group": 0, "Insider": 1, "Botnet": 2}
vulnerability_options = {"Unpatched Software": 0, "Weak Passwords": 1, "Social Engineering": 2}
defense_options = {"Firewall": 0, "Antivirus": 1, "AI Monitoring": 2}

# User Inputs
year = st.number_input("Year of Incident", min_value=2015, max_value=2024, step=1)

# Use dropdowns instead of raw number inputs
country = st.selectbox("Country", list(country_options.keys()))
industry = st.selectbox("Target Industry", list(industry_options.keys()))
source = st.selectbox("Attack Source", list(source_options.keys()))
vulnerability = st.selectbox("Vulnerability Type", list(vulnerability_options.keys()))
defense = st.selectbox("Defense Mechanism Used", list(defense_options.keys()))

# Scaled inputs (enter manually or from sliders if desired)
loss = st.number_input("Financial Loss (standardized)", format="%.2f")
users = st.number_input("Affected Users (standardized)", format="%.2f")
time = st.number_input("Resolution Time (standardized)", format="%.2f")

# Predict button
if st.button("Predict Attack Type"):
    # Convert dropdown text to their encoded values
    input_data = np.array([[
        year,
        country_options[country],
        industry_options[industry],
        loss,
        users,
        source_options[source],
        vulnerability_options[vulnerability],
        defense_options[defense],
        time
    ]])

    # Predict and decode the output
    prediction = model.predict(input_data)
    attack_type = label_encoder.inverse_transform(prediction)

    st.success(f"🔍 Predicted Attack Type: {attack_type[0]}")
