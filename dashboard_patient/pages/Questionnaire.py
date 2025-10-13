import streamlit as st
import pandas as pd

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

bool_map = {'Yes': 1, 'No': 0}
gender_map = {'Male': 1, 'Female': 0}
bp_map = {'High': 1, 'Low': 0}


with st.form("my_form"):
    st.write("# Questionnaire")
    st.write(" ### Fill out the form below. The answers will be sent to your physician for further assessment.")
    st.write("By proceeding, you consent to your responses being collected and used for medical purposes in accordance with Findabetes' data handling and privacy policy. Please read more at XXX.")
    st.checkbox("I agree to the terms.")

    st.write("-------------------------------------------------------------------------------")

    option = st.radio(
        "Choose your gender.",
        ["Female", "Male"],
        index=None,
        key=1,
    )
    gender = option

    #Should be decided on an acceptable interval!
    age = st.number_input(
        "Enter your age",
        min_value=18,
        max_value=120,
        step=1,
        format="%d",      # ensures whole numbers are displayed
    )
    
    option = st.radio(
        "Select the level of your blood pressure",
        ["Normal", "High"],
        index=None,
        key=10,
    )
    highbp = option

## Insert BMI calculator here!
    weight = st.number_input("Weight (kg)",
                            step=1,
                            format="%d")
    height = st.number_input("Height (cm):",         
                            step=1,
                            format="%d")
    def calculate_BMI(weight, height):
        height_meter = height / 100
        return weight / (height_meter ** 2) 
    
    option = st.radio(
        "Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]",
        ["No", "Yes"],
        index=None,
        key=9,
    )
    smoker = option

## Note that in the data set the question is "(Ever told) you had a stroke".
    option = st.radio(
        "Have you had a stroke?",
        ["No", "Yes"],
        index=None,
        key=8,
    )
    stroke = option

## Might be rephrased
    option = st.radio(
        "Have you had or do you have Coronary Heart Disease (CHD) or myocardial infarction?",
        ["No", "Yes"],
        index=None,
        key=7,
    )
    HeartDiseaseorAttack = option

    option = st.radio(
        "Have you performed physical activity in the past 30 days? (Not including your job)",
        ["No", "Yes"],
        index=None,
        key=6,
    )
    PhysAct = option

    option = st.radio(
        "Do you consume fruit at least one time per day?",
        ["No", "Yes"],
        index=None,
        key=5,
    )
    Fruits = option

    option = st.radio(
        "Do you consume vegetables at least one time per day?",
        ["No", "Yes"],
        index=None,
        key=4,
    )
    Veggies = option

    option = st.radio(
        "Do you drink more than 14 alcoholic beverages (as a man) or 7 alcoholic beverages (as a woman) per week?",
        ["No", "Yes"],
        index=None,
        key=3,
    )
    HeavyAlcConsumption = option

    options = ["1 = Excellent", "2 = Very good", "3 = Good", "4 = Fair","5 = Poor"]
    selection = st.pills(
        "Would you say that in general your health is on a scale 1-5?", 
        options)
    
    if selection:
        # Extract the number before the '='
        GenHlth = int(selection.split('=')[0].strip())

    ##  A slider may not be the best option, but we'll go with that for now. 
    option = st.select_slider(
        "How many of the past 30 days have you experienced any mental health problems?",
        options=[str(i) for i in range(31)],
    )
    MenHlth = option
    
    option = st.radio(
        "Do you have serious difficulty walking or climbing stairs?",
        ["No", "Yes"],
        index=None,
        key=2,
    )
    DiffWalk = option

    
    submitted = st.form_submit_button("Submit")
    ## Have to enter more code in this button once the dataset is loaded!

    if submitted:
        df = pd.DataFrame({
            "High BP": [bp_map[highbp]],
            "BMI": [int(calculate_BMI(weight=weight, height=height))],
            "Smoker": [bool_map[smoker]],
            "Stroke": [bool_map[stroke]],
            "Heart Disease or Attack": [bool_map[HeartDiseaseorAttack]],
            "Physical Activity": [bool_map[PhysAct]],
            "Fruits": [bool_map[Fruits]],
            "Veggies": [bool_map[Veggies]],
            "Heavy Alcohol Consumption": [bool_map[HeavyAlcConsumption]],
            "General Health": [GenHlth],
            "Mental Health": [MenHlth],
            "Difficulties Walking": [bool_map[DiffWalk]],
            "Gender": [gender_map[gender]],
            "Age": [int(age)]
        })

        df.to_csv('././data/input_data.csv', index=False)