import streamlit as st

st.set_page_config(
    page_title="Findabetes CDS Tool",
    page_icon="assets/Logofindabetes.png",
    layout='wide'
)

# Sidebar configuration
st.sidebar.image("./assets/LogoFindabetes.png",)
st.sidebar.success("Select a tab above.")

st.header("Welcome to Your Diabetes Risk Check!")

col1, col2 = st.columns([1.2, 0.8])

with col1:
    with st.container(border=False):
        st.markdown(
            """
            ### 🩺 Type-2 Diabetes Risk Assessment

            Type-2 Diabetes often develops slowly — many people don’t notice symptoms until complications arise. Early awareness is key to prevention and better long-term health.

            This short questionnaire helps your doctor understand your personal risk of developing Type-2 Diabetes based on lifestyle, medical history, and health factors.

            By identifying your risk early, you can take meaningful steps such as:

            - Improving your diet and physical activity  
            - Monitoring your blood glucose more regularly  
            - Discussing preventive options with your healthcare provider  

            Your answers will generate a personalized risk score that is securely sent to your physician.
            """
        )

with col2: 
    with st.container(border=False):
        st.image('https://images.everydayhealth.com/images/seo-graphic-content-initiative/eh-how-type-2-diabetes-affects-the-body-seo-graphics-gs.png?w=1110', caption='How Type-2 Diabetes Affects the Body - Typical Symptoms')


st.divider()

st.markdown("""
### ⚠️ Important Notice

This questionnaire is intended for early risk screening of Type-2 diabetes and should not be used as a substitute for 
professional medical advice or diagnosis.  

If you are currently experiencing severe of the above shown symptoms such as extreme unexplained weight loss, 
frequent urination, fatigue, blurred vision, or any other serious health concerns, 
please **seek immediate medical attention** or **visit a physician** without delay.
""")

st.divider()

st.markdown(
    """
    ### 🔒 Privacy and Data Use

    Before you begin the questionnaire, please take a moment to understand how your information will be handled.  
    The responses you provide will help calculate your **individual risk of developing Type-2 Diabetes**.  
    Your results will be securely shared with your **physician**, who may contact you for **follow-up or preventive advice** if needed.  

    All data is handled **confidentially**, in accordance with **health privacy and data protection regulations**.  
    Your information will be used **solely for your medical care** and will not be shared with third parties.  

    If you have any questions, please contact **RandomName Primary Care Central**.
    """
)

if st.button("Start questionnaire"): 
    st.switch_page("pages/Questionnaire.py")