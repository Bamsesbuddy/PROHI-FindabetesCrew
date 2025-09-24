import streamlit as st
import pandas as pd

st.markdown("# Descriptive Analytics 📊")

st.sidebar.markdown("# Descriptive Analytics 📊")

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("jupyter-notebooks/data.csv")
X = load_data()

# Plotting a dataframe
st.markdown("## Tabular dataset of five patients")
st.dataframe(X.head())


"""Add here some descriptive analytics with Widgets and Plots

### ⚠️ In-class exercise: Integrate a plot from plotly examples

🔗 Link: <https://plotly.com/python/scientific-charts/>
"""

import numpy as np
import plotly.figure_factory as ff

st.bar_chart(X.set_index("Smoker"))

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)


## Plot two

import plotly.express as px
import pandas as pd
df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)

st.plotly_chart(fig, use_container_width=True)