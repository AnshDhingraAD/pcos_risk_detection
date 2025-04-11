import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('pcos_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Set the background color of the whole page
st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;  # Light blue background
    }
    </style>
""", unsafe_allow_html=True)

# Set up the Streamlit app title and description
st.title("PCOS Risk Prediction")
st.markdown("""
    This is a PCOS risk prediction tool. 
    Fill in the details below to check your risk level.
    ### Instructions:
    - Provide values for each input parameter.
    - The model will predict whether you are at risk of PCOS.
""")

# Add some space
st.markdown("<br>", unsafe_allow_html=True)

# Create a form to take user input
with st.form("prediction_form"):
    st.subheader("Enter Your Details")

    age = st.number_input("Age (Years)", min_value=15, max_value=100, value=25)
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=24.5)
    fsh = st.number_input("FSH (mIU/mL)", min_value=0.0, max_value=50.0, value=6.3)
    lh = st.number_input("LH (mIU/mL)", min_value=0.0, max_value=50.0, value=8.2)

    # Calculate FSH/LH ratio based on user inputs
    fsh_lh_ratio = fsh / lh if lh != 0 else 0  # Avoid division by zero

    amh = st.number_input("AMH (ng/mL)", min_value=0.0, max_value=10.0, value=2.5)
    rbs = st.number_input("RBS (mg/dl)", min_value=50, max_value=300, value=95)

    weight_gain = st.selectbox("Weight Gain?", options=["Yes", "No"])
    hair_growth = st.selectbox("Hair Growth?", options=["Yes", "No"])
    skin_darkening = st.selectbox("Skin Darkening?", options=["Yes", "No"])
    hair_loss = st.selectbox("Hair Loss?", options=["Yes", "No"])
    pimples = st.selectbox("Pimples?", options=["Yes", "No"])

    fast_food = st.selectbox("Do you consume fast food regularly?", options=["Yes", "No"])
    regular_exercise = st.selectbox("Do you exercise regularly?", options=["Yes", "No"])
    bp_diastolic = st.number_input("BP Diastolic (mmHg)", min_value=50, max_value=120, value=80)

    # Submit button
    submit_button = st.form_submit_button("Predict PCOS Risk")

# Predict when button is pressed
if submit_button:
    # Convert Yes/No inputs to 1/0 for model
    input_data = np.array([[
        age, bmi, fsh, lh, fsh_lh_ratio, amh, rbs,
        1 if weight_gain == "Yes" else 0,
        1 if hair_growth == "Yes" else 0,
        1 if skin_darkening == "Yes" else 0,
        1 if hair_loss == "Yes" else 0,
        1 if pimples == "Yes" else 0,
        1 if fast_food == "Yes" else 0,
        1 if regular_exercise == "Yes" else 0,
        bp_diastolic
    ]])

    # Make prediction
    prediction = model.predict(input_data)
    risk = "Yes" if prediction[0] == 1 else "No"

    # Display the result with some styling
    st.markdown(f"### **PCOS Risk Prediction: {risk}**", unsafe_allow_html=True)

    if risk == "Yes":
        st.markdown("""
            <style>
            .stMarkdown {
                color: red;
                font-size: 24px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stMarkdown {
                color: green;
                font-size: 24px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
