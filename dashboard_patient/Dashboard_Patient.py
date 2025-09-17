import streamlit as st

st.set_page_config(
    page_title="Findabetes CDS Tool",
    page_icon="assets/Logofindabetes.png",
)

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Findabetes CDS Tool")

st.markdown(
"""
    ## Welcome to the patient's view! Please navigate to Questionnaire in the sidebar.
    
"""
)

st.caption("Welcome to the patient's view! Please navigate to Questionnaire in the sidebar")

