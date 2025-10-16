import streamlit as st
import joblib
import pandas as pd
import altair as alt
from utils.helper import make_donut
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(layout="wide")

st.markdown("# Predictive Analytics")

st.sidebar.image("./assets/LogoFindabetes.png")

button_press = False

st.markdown("""
    This page provides a predictive analytics interface designed to support clinical 
    decision-making in the assessment of Type-2 Diabetes risk. The underlying 
    machine learning model evaluates patient-specific features — including demographic and
    lifestyle factors — to generate an individualized risk estimation.

    By integrating data-driven insights with traditional clinical parameters, the tool 
    enables early identification of patients at elevated risk for Type-2 diabetes, 
    facilitating timely preventive interventions and personalized management strategies.
            
    **By pressing the button below the prediction is started and the patient's parameters 
    along with the risk probability are shown**.
""")

def get_age_group_mapping(age):
    if age < 18: return None
    elif age <= 24: return 1
    elif age <= 29: return 2
    elif age <= 34: return 3
    elif age <= 39: return 4
    elif age <= 44: return 5
    elif age <= 49: return 6
    elif age <= 54: return 7
    elif age <= 59: return 8
    elif age <= 64: return 9
    elif age <= 69: return 10
    elif age <= 74: return 11
    elif age <= 79: return 12
    else: return 13

# Load model
pre_trained_model_path = "./jupyter-notebooks/hgb_classifier_V2.pkl"
loaded_model = joblib.load(pre_trained_model_path)

button_press_bool = st.button('Predict!')
if button_press_bool:
    user_data = pd.read_csv('data/input_data.csv')
    X = user_data.copy()
    X["Age"] = get_age_group_mapping(user_data["Age"].to_numpy())

    prediction = loaded_model.predict_proba(X)[0]
    # st.write(f"The predicted value is {prediction}")

    # COLUMNS
    left_column, right_column = st.columns([0.6, 1.4])
    with left_column:
        if int(prediction[1] * 100) > 50:
            st.image("./assets/FindabetesHighrisk.png", width=400)
        elif int(prediction[1] * 100) > 30: 
            st.image("./assets/FindabetesModeraterisk.png", width=400)
        else:
            st.image("./assets/image.png", width=400)
    with right_column:
        with st.container(border=True):
            # Donut chart for diabetes risk
            if int(prediction[1] * 100) > 50:
                donut_class_one = make_donut(int(prediction[1] * 100), 'Risk of Type-2 Diabetes', 'red')
                st.altair_chart(donut_class_one, use_container_width=True)
            elif int(prediction[1] * 100) > 30:
                donut_class_one = make_donut(int(prediction[1] * 100), 'Risk of Type-2 Diabetes', 'orange')
                st.altair_chart(donut_class_one, use_container_width=True)
            else:
                donut_class_one = make_donut(int(prediction[1] * 100), 'Risk of Type-2 Diabetes', 'green')
                st.altair_chart(donut_class_one, use_container_width=True)
            st.markdown("<h2 style='text-align: center;'>Risk of Type-2 Diabetes</h2>", unsafe_allow_html=True)
                

    # --- Mappings ---
    bool_map = {0: "No", 1: "Yes"}
    gender_map = {0: "Female", 1: "Male"}

    user = user_data.iloc[0]  # shorthand

    # --- Container for Patient Metrics ---
    with st.container(border=True):
        st.markdown("### 🧍 Patient Overview")

        # --- Row 1: Demographics + Conditions ---
        row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])

        with row1_col1:
            st.subheader("👤 Demographics")
            st.metric("Gender", gender_map[user[11]])
            st.metric("Age", int(user[12]))
            st.metric("BMI", f"{user[1]}")

        with row1_col2:
            st.subheader("🩺 Conditions")
            st.metric("High Blood Pressure", bool_map[user[0]])
            st.metric("Heart Disease", bool_map[user[4]])
            st.metric("Stroke", bool_map[user[3]])

        with row1_col3:
            st.subheader("🏃 Lifestyle")
            st.metric("Fruits", bool_map[user[6]])
            st.metric("Veggies", bool_map[user[7]])
            st.metric("Smoker", bool_map[user[2]])

        st.markdown("---")

        # --- Row 2: Health Scores ---
        row2_col1, row2_col2 = st.columns(2)

        if user[8] == 1:
            tmp = 'Excellent'
        elif user[8] == 2:
            tmp = 'Very good'
        elif user[8] == 3:
            tmp = 'Good'
        elif user[8] == 4:
            tmp = 'Fair'
        elif user[8] == 5:
            tmp = 'Poor' 

        with row2_col1:
            st.subheader("🧠 Mental & Physical")
            st.metric("General Health", tmp)
            st.metric("Mental Health", user[9])

        with row2_col2:
            st.subheader("🚶 Mobility")
            st.metric("Physical Activity", bool_map[user[5]])
            st.metric("Difficulty Walking", bool_map[user[10]])

        # --- Style all metrics consistently ---
        style_metric_cards(
            background_color="#F8FAFC",     # light gray/white
            border_left_color="#4682b4",    # blue accent
            border_color="#CBD5E1",
            box_shadow=True,
        )

    ## Button that redirects us to Prescriptive Analytics, page 4
    button_press = st.button("See detailed view")
        
if button_press:
    button_press_bool = False
    st.switch_page("pages/4_Prescriptive_Analytics.py")



