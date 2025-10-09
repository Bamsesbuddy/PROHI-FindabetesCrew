import streamlit as st

st.set_page_config(
    page_title="Findabetes CDS Tool",
    page_icon="assets/Logofindabetes.png",
)

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Welcome to Findabetes,")



st.write("## Every Clinician's favorite screening tool for predicting risk for diabetes.")
st.markdown("<br>", unsafe_allow_html=True)
st.write("Our tool is meant to help clinicians digitally and more easily recieve data from patients and predict whether the patients have a risk of developing diabetes type 2. Our prediction is based on different features, asked in the patient questionnaire.")
    
st.markdown("<br>", unsafe_allow_html=True)

st.write("To explore the data you can view the descriptive page, to see more about how the statistical analysis has been performed. Our diagnostic page will give insights into how the statistical analysis is applied to the data set. To see patient instances, view predictive analytics, as well as prescriptive analytics explaining the prediction for that specific instance.")
        

## Button that redirects us to Prescriptive Analytics, page 4
if st.button("Get started"): 
    st.switch_page("pages/1_Descriptive_Analytics.py")
