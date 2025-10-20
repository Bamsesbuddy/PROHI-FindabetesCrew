import streamlit as st
import pandas as pd
import os

# -----------------------------
# Sidebar configuration
# -----------------------------
st.sidebar.image("./assets/LogoFindabetes.png")

# -----------------------------
# Helper functions for encoding
# -----------------------------
def encode_binary(option):
    """Encode Yes/No as 1/0"""
    return 1 if option == "Yes" else 0

def encode_gender(option):
    """Encode gender: Male=1, Female=0"""
    return 1 if option == "Male" else 0

def calculate_BMI(weight, height):
    """Calculate BMI from weight (kg) and height (cm)"""
    height_meter = height / 100
    return weight / (height_meter ** 2)

# -----------------------------
# Page title and disclaimer
# -----------------------------
st.title("Questionnaire")
st.write(
    "### Please complete the form below. Your responses will be sent to your physician for assessment."
)
st.warning(
    "⚠️ If you are experiencing severe symptoms such as extreme thirst, unexplained weight loss, frequent urination, fatigue, or blurred vision, "
    "please visit a physician immediately before proceeding."
)
st.write(
    "By proceeding, you consent to your responses being collected and used for medical purposes in accordance with Findabetes' data handling and privacy policy."
)

agree_terms = st.checkbox("I agree to the terms and conditions.")

st.divider()

# -----------------------------
# Form
# -----------------------------
if agree_terms:

    with st.form("questionnaire_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio("Gender", ["Female", "Male"])
        with col2:
            age = st.number_input("Age", min_value=18, max_value=120, step=1, format="%d")

        st.subheader("Health Information")
        col1, col2 = st.columns(2)
        with col1:
            highbp = st.radio("Blood Pressure Level", ["Normal", "High"])
            weight = st.number_input("Weight (kg)", step=1, format="%d")
            height = st.number_input("Height (cm)", step=1, format="%d")
        with col2:
            smoker = st.radio("Have you smoked at least 100 cigarettes in your life?", ["No", "Yes"])
            stroke = st.radio("Have you had a stroke?", ["No", "Yes"])
            HeartDiseaseorAttack = st.radio(
                "Have you had or do you have Coronary Heart Disease (CHD) or myocardial infarction?",
                ["No", "Yes"]
            )
        if height and weight is not None:
            bmi = calculate_BMI(weight, height)
            st.info(f"Your calculated BMI is **{bmi:.1f}**")
        else:
            bmi = 0

        st.subheader("Lifestyle")
        col1, col2 = st.columns(2)
        with col1:
            PhysAct = st.radio("Physical activity in the past 30 days (not including work)?", ["No", "Yes"])
            Fruits = st.radio("Consume fruit at least once per day?", ["No", "Yes"])
            Veggies = st.radio("Consume vegetables at least once per day?", ["No", "Yes"])
        with col2:
            DiffWalk = st.radio("Do you have serious difficulty walking or climbing stairs?", ["No", "Yes"])
            GenHlth = st.selectbox(
                "General health (1=Excellent, 5=Poor)",
                ["Excellent", "Very good", "Good", "Fair", "Poor"]
            )
            MenHlth = st.slider(
                "Number of past 30 days with mental health problems",
                min_value=0, max_value=30, value=0
            )

        # -----------------------------
        # Encode responses and create DataFrame
        # -----------------------------
        gen_health_map = {"Excellent": 1, "Very good": 2, "Good": 3, "Fair": 4, "Poor": 5}
        df = pd.DataFrame({
            "High BP": [1 if highbp == "High" else 0],
            "BMI": [round(bmi, 1)],
            "Smoker": [encode_binary(smoker)],
            "Stroke": [encode_binary(stroke)],
            "Heart Disease or Attack": [encode_binary(HeartDiseaseorAttack)],
            "Physical Activity": [encode_binary(PhysAct)],
            "Fruits": [encode_binary(Fruits)],
            "Veggies": [encode_binary(Veggies)],
            "General Health": [gen_health_map[GenHlth]],
            "Mental Health": [MenHlth],
            "Difficulties Walking": [encode_binary(DiffWalk)],
            "Gender": [encode_gender(gender)],
            "Age": [int(age)]
        })

        # -----------------------------
        # Submit button
        # -----------------------------
        submitted = st.form_submit_button("Submit")

        if submitted:
            if df.isna().any(axis=1).values[0]:
                st.error("Please fill out all fields before submitting.", icon="⚠️")
            else:
                # Append to CSV instead of overwriting
                file_path = './data/input_data.csv'
                df.to_csv(file_path, index=False)

                st.success("Your data has been successfully transmitted!", icon="✅")