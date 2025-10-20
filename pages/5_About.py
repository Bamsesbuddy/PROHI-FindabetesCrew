import streamlit as st

st.sidebar.markdown("# About us")
st.sidebar.image("./assets/LogoFindabetes.png")

st.markdown("# About Findabetes")

st.markdown(" ## Information about the dataset")
"""This application is based on the dataset from the U.S. Centers for Disease Control and Prevention. Click on this link to read more about the dataset: CDC Diabetes Health Indicators https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
.

We have developed a machine learning model using our own algorithm to predict whether a patient may be at risk for diabetes. The model has been evaluated on real-world data and currently achieves an accuracy of 70.9%, with strong performance across other metrics such as precision (29.7%) and recall (79.4%).

The goal of this tool is to support both patients and physicians in identifying potential risks early and guiding further clinical actions."""

st.divider()

st.markdown(" ## References")
"""
1. UCI Machine Learning Repository. (2017). CDC Diabetes Health Indicators [Dataset]. Retrieved September 25, 2023, from https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators  

2. Centers for Disease Control and Prevention. (2022, April 29). CDC – 2014 BRFSS Survey Data and Documentation. Retrieved from https://www.cdc.gov/brfss/annual_data/annual_2014.html 
"""

st.divider()

st.markdown(""" 
            ## Group members & Contact Information
            * Amanda Jacobsson - amanda.jacobsson@findabetes.com
            * Anna Larsen - anna.larsen@findabetes.com
            * Anton Altmeyer - anton.altmeyer@findabetes.com
            * Elina Nordlund - elina.nordlund@findabetes.com
            * Vikrant Nigam - vikrant.nigam@findabetes.com
""")