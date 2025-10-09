import streamlit as st
import joblib
import pandas as pd
import altair as alt
from pages.helper import make_donut

st.set_page_config(layout="wide")

st.markdown("# Patient prediction")

st.sidebar.markdown("# Patient prediction")
st.sidebar.image("./assets/LogoFindabetes.png")

"""
⚠️ Add here some predictive analytics with Widgets and Plots 
"""

st.write("# Example of model prediction")


# Load model
pre_trained_model_path = "./jupyter-notebooks/hgb_classifier.pkl"
loaded_model = joblib.load(pre_trained_model_path)

if st.button('Predict!'):
    user_data = pd.read_csv('data/input_data.csv')

    prediction = loaded_model.predict_proba(user_data)[0]
    # st.write(f"The predicted value is {prediction}")

    # COLUMNS
    left_column, right_column = st.columns(2)
    with left_column:
        if int(prediction[1] * 100) > 50:
            st.image("./assets/FindabetesHighrisk.png", width=500)
        elif int(prediction[1] * 100) > 30: 
            st.image("./assets/FindabetesModeraterisk.png", width=500)
        else:
            st.image("./assets/FindabetesLowrisk.png", width=500)
    with right_column:
        donut_class_zero = make_donut(int(prediction[0] * 100), 'Outbound Migration', 'green')
        st.altair_chart(donut_class_zero)
        donut_class_one = make_donut(int(prediction[1] * 100), 'Outbound Migration', 'red')
        st.altair_chart(donut_class_one)

    with st.container(border=True):
        bool_map = {0: "No", 1: "Yes"}
        gender_map = {0: "Female", 1: "Male"}
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(label="High Blood Pressure", value=bool_map[user_data.iloc[0, 0]])
            st.metric(label="Body Mass Index", value=user_data.iloc[0, 1])
            st.metric(label="Blood Pressure", value=bool_map[user_data.iloc[0, 2]])
        with col2:
            st.metric(label="Stroke", value=bool_map[user_data.iloc[0, 3]])
            st.metric(label="Heart Disease", value=bool_map[user_data.iloc[0, 4]])
            st.metric(label="Physical Activity", value=bool_map[user_data.iloc[0, 5]])
        with col3:
            st.metric(label="Fruits", value=bool_map[user_data.iloc[0, 6]])
            st.metric(label="Veggies", value=bool_map[user_data.iloc[0, 7]])
            st.metric(label="Alcohol Abuse", value=bool_map[user_data.iloc[0, 8]])
        with col4:
            st.metric(label="General Health", value=user_data.iloc[0,9])
            st.metric(label="Mental Health", value=user_data.iloc[0,10])
        with col5:
            st.metric(label="Difficulty Walking", value=bool_map[user_data.iloc[0, 11]])
            st.metric(label="Gender", value=gender_map[user_data.iloc[0, 12]])
            st.metric(label="Age", value=user_data.iloc[0,13])

## Button that redirects us to Prescriptive Analytics, page 4
if st.button("See detailed view"): 
    st.switch_page("pages/4_Prescriptive_Analytics.py")



