import streamlit as st

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

st.write("# Questionnaire")
st.write(" ### Fill out the form below. The answers will be sent to your physician for further assessment.")

option = st.selectbox(
    "By proceeding, you consent to your responses being collected and used for medical purposes in accordance with Findabetes' data handling and privacy policy. Please read more at XXX",
    ("Yes"),
    index=None,
    placeholder="Required*",
)

option = st.selectbox(
    "Do you consume fruit 1 or more times per day?",
    ("Yes", "No"),
    index=None,
    placeholder="Choose one",
)

option = st.selectbox(
    "Do you consume fruit 1 or more times per day?",
    ("Yes", "No"),
    index=None,
    placeholder="Choose one",
)