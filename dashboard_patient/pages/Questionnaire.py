import streamlit as st

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

with st.form("my_form"):
    st.write("# Questionnaire")
    st.write(" ### Fill out the form below. The answers will be sent to your physician for further assessment.")
    st.write("By proceeding, you consent to your responses being collected and used for medical purposes in accordance with Findabetes' data handling and privacy policy. Please read more at XXX.")
    st.checkbox("I agree to the terms.")

    
    option = st.radio(
    "Select the level of your blood pressure",
    ["Low", "High"],
    index=None,
    key=10,
)

## Insert BMI calculator here!

    option = st.radio(
    "Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]",
    ["No", "Yes"],
    index=None,
    key=9,
)

## Note that in the data set the question is "(Ever told) you had a stroke".
    option = st.radio(
    "Have you had a stroke?",
    ["No", "Yes"],
    index=None,
    key=8,
)

## Might be rephrased
    option = st.radio(
    "Have you had or do you have Coronary Heart Disease (CHD) or myocardial infarction?",
    ["No", "Yes"],
    index=None,
    key=7,
)
    option = st.radio(
    "Have you performed physical activity in the past 30 days? (Not including your job)",
    ["No", "Yes"],
    index=None,
    key=6,
)

    option = st.radio(
    "Do you consume fruit 1 or more times per day??",
    ["No", "Yes"],
    index=None,
    key=5,
)

    option = st.radio(
    "Do you consume vegetables 1 or more times per day??",
    ["No", "Yes"],
    index=None,
    key=4,
)

    option = st.radio(
    "Do you drink more than 14 drinks (as a man) or 7 drinks (as a woman) per week?",
    ["No", "Yes"],
    index=None,
    key=3,
)
    options = ["1 = Excellent", "2 = Very good", "3 = Good", "4 = Fair","5 = Poor"]
    selection = st.pills(
        "Would you say that in general your health is on a scale 1-5?", 
        options, 
        selection_mode="multi")

    ##  A slider may not be the best option, but we'll go with that for now. 
    option = st.select_slider(
        "Now thinking about your mental health, which includes stress, depression, and problems with emotions, for how many days during the past 30 days was your mental health ***not*** good?",
        options=[
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
    ],
)

    option = st.select_slider(
        "Now thinking about your physical health, which includes physical illness and injury, for how many days during the past 30 days was your physical health ***not*** good?",
        options=[
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
    ],
)
    option = st.radio(
    "Do you have serious difficulty walking or climbing stairs?",
    ["No", "Yes"],
    index=None,
    key=2,
)

    option = st.radio(
    "Choose your gender.",
    ["Female", "Male"],
    index=None,
    key=1,
)
    #Should be decided on an acceptable interval!
    number = st.number_input(
    "Enter your age", value=None,
)
    
    submitted = st.form_submit_button("Submit")
    ## Have to enter more code in this button once the dataset is loaded!


