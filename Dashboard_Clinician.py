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
    ## Welcome to the physician's view!
    
"""
)

# You can also add text right into the web as long comments (""")
"""
The final project aims to apply data science concepts and skills on a 
medical case study that you and your team select from a public data source.
The project assumes that you bring the technical Python skills from 
previous courses (*DSHI*: Data Science for Health Informatics), as well as 
the analytical skills to argue how and why specific techniques could
enhance the problem domain related to the selected dataset.
"""

# DATAFRAME MANAGEMENT
import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

# Add a selectbox to the sidebar:
add_selectbox = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'House phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
