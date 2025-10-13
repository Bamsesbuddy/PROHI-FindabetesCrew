import streamlit as st

st.set_page_config(
    page_title="Dashboard Clinician",
    page_icon="assets/Logofindabetes.png",
    layout='wide'
)

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Findabetes CDS Tool")

st.markdown(
    """
    ## Screening tool for predicting risk for diabetes. 
    Our tool is meant to help clinicians digitally and more easily receive data from patients and predict whether the patients have a risk of developing Type-2 diabetes.
    """
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            """
            Our prediction is based on the following features, asked in the patient questionnaire:

            - High Blood Pressure - Yes or No?
            - Body Mass Index (BMI)
            - Have you smoked at least 100 cigarettes in your entire life?
            - History of Stroke - Yes or No?
            - Heart Disease or Attack (coronary heart disease or myocardial infarction) - Yes or No?
            - Physical Activity in past 30 days? - Yes or No?
            - Fruits 1 or more times per day - Yes or No?
            - Veggies 1 or more times per day - Yes or No?
            - General Health
            - For how many days during the past 30 days was your physical health not good? 
            - Do you have serious difficulty walking or climbing stairs? 
            - Gender
            - Age
            """
        )

with col2: 
    with st.container(border=False):
        st.image('https://images.everydayhealth.com/images/seo-graphic-content-initiative/eh-how-type-2-diabetes-affects-the-body-seo-graphics-gs.png?w=1110', caption='How Type-2 Diabetes Affects the Body - Typical Symptoms')

# You can also add text right into the web as long comments (""")
"""
To begin exploring patient and cohort data, navigate to the Descriptive Analytics page. This section provides an overview of patient demographics, 
cohort trends, and key distributions, along with an explanation of how the underlying statistical summaries were generated. 
Use this page to understand overall population trends or identify outliers.

The Diagnostic Analytics page allows you to review how statistical models are applied to the dataset. 
Here you can explore correlations between variables and subgroup comparisons using cluster analysis

For individual patient assessment, open the Predictive and Prescriptive Analytics tab. 
This section presents a patient-specific risk score and a breakdown of the contributing clinical factors. 
You can also perform a “what-if” counterfactual analysis to simulate how modifying certain parameters 
(e.g., medication adherence or biomarker values) might influence the predicted outcome. Each prediction is 
accompanied by an optional AI-generated clinical interpretation and summary to support decision-making.
"""

