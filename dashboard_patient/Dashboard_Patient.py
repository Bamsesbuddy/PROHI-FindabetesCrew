import streamlit as st

st.set_page_config(
    page_title="Findabetes CDS Tool",
    page_icon="👋",
)

# Sidebar configuration
st.sidebar.image("./assets/project-logo.jpg",)
st.sidebar.success("Select a tab above.")

# # Page information

st.write("# Findabetes CDS Tool")

st.markdown(
"""
    ## Welcome to the patient's view!
    
"""
)

fruit = st.radio("Do you consume fruit 1 or more times per day?", "[Yes]","[No]")