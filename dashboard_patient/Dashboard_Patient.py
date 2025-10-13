import streamlit as st

st.set_page_config(
    page_title="Findabetes CDS Tool",
    page_icon="assets/Logofindabetes.png",
)

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Findabetes Decision Support Tool")

st.markdown(
"""
    ## Welcome to the patient's view!
    
"""
)

"""Before you begin filling out the questionnaire, we want you to know how your information will be handled. The answers you provide will be used to calculate your risk of developing diabetes. Your results will be shared with your physician, and you may be contacted for further follow-up if needed.

All information is managed securely and in line with privacy regulations, and will only be used for your medical care.

If you have any questions, please contact RandomName Primary Care Central."""


if st.button("Start questionnaire"): 
    st.switch_page("pages/Questionnaire.py")