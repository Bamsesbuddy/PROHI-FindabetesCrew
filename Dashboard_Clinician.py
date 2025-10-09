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


st.write("## Every Clinician's favorite screening tool for predicting diabetes risk.")
st.markdown("<br>", unsafe_allow_html=True)
st.write("Findabetes is designed to support your clinical workflow by providing fast, data-driven insights into your patients’ diabetes risk. Our prediction model is powered by machine learning, using information gathered from each patient’s questionnaire to deliver accurate and interpretable results.")
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
You can explore the system through the following sections:  

**Descriptive Analysis** - Discover the characteristics of the dataset used to train our model.  
**Diagnostic Insights** - Understand how statistical and analytical methods are applied to the data.  
**Predictive & Prescriptive Tools** - View personalized predictions for your patients and explore potential clinical actions.  
""")

st.markdown("<br>", unsafe_allow_html=True)
st.write("Findabetes brings together data science and clinical expertise - helping you make informed decisions, faster.")

## Button that redirects us to Prescriptive Analytics, page 4
if st.button("Get started"): 
    st.switch_page("pages/1_Descriptive_Analytics.py")
