import streamlit as st

st.sidebar.markdown("# About us")
st.sidebar.image("./assets/LogoFindabetes.png")

st.markdown("# About Findabetes")

st.markdown(" ## Information about the dataset")
"""This application is based on the dataset from the U.S. Centers for Disease Control and Prevention. Click on this link to read more about the dataset: CDC Diabetes Health Indicators https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators
.

We have developed a machine learning model using our own algorithm to predict whether a patient may be at risk for diabetes. The model has been evaluated on real-world data and currently achieves an accuracy of X %, with strong performance across other metrics such as precision (X %) and recall (X %).

The goal of this tool is to support both patients and physicians in identifying potential risks early and guiding further clinical actions."""

st.markdown(" ## References")
"""1. https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators  2. https://www.cdc.gov/brfss/annual_data/annual_2014.html"""
st.markdown(" ## Group members")
"""Amanda Jacobsson  
Anna Larsen  
Anton Altmeyer  
Elina Nordlund  
Vikrant Nigam"""

st.markdown(" ## Contact information")