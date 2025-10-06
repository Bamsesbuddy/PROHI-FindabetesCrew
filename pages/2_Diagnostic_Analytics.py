import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown("# Diagnostic Analytics")

st.sidebar.markdown("# Diagnostic Analytics")
st.sidebar.image("./assets/LogoFindabetes.png",)

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("jupyter-notebooks/data.csv")
X = load_data()

st.subheader("Interactive correlation heatmap")

cols = st.multiselect("Select what features you wish to see in the heatmap.", X.columns.tolist(), default=X.columns.tolist())
corr = X[cols].corr()


fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Matrix"
)
st.plotly_chart(fig, use_container_width=True)