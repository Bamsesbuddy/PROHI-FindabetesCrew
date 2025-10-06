import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("# Descriptive Analytics 📊")

st.sidebar.markdown("# Descriptive Analytics")
st.sidebar.image("./assets/LogoFindabetes.png",)

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("jupyter-notebooks/data.csv")
X = load_data()

# Plotting a dataframe
st.markdown("## Tabular dataset of five patients")
st.dataframe(X.head())


# Add here some descriptive analytics with Widgets and Plots

### ⚠️ In-class exercise: Integrate a plot from plotly examples

# 🔗 Link: <https://plotly.com/python/scientific-charts/>

# import plotly.figure_factory as ff


st.subheader("Smoker and diabetes")
chart_data = X.groupby(["Smoker", "Diabetes_binary"]).size().reset_index(name="count")
# Plotly bar chart
fig = px.bar(
    chart_data,
    x="Smoker",
    y="count",
    color="Diabetes_binary",
    barmode="group",
    labels={"Smoker": "Smoker (0=No, 1=Yes)", "Diabetes_binary": "Diabetes (0=No, 1=Yes)", "count": "Antal"}
)
st.plotly_chart(fig, use_container_width=True)



st.subheader("High bloodpressure and diabetes")
chart_data = X.groupby(["HighBP", "Diabetes_binary"]).size().reset_index(name="count")
 # Plotly bar chart
fig = px.bar(
    chart_data,
    x="HighBP",
    y="count",
    color="Diabetes_binary",
    barmode="group",
    labels={"HighBP": "HighBloodPressure (0=No, 1=Yes)", "Diabetes_binary": "Diabetes (0=No, 1=Yes)", "count": "Antal"}
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Diabetes distribution for features (100% stacked, single bar per feature)")

features = ["HighBP", "Smoker", "PhysActivity", "HvyAlcoholConsump", "Sex", "DiffWalk", "Stroke", "Fruits", "Veggies"]

# Melt: reshape into long form
df_long = X.melt(
    id_vars=["Diabetes_binary"],
    value_vars=features,
    var_name="feature",
    value_name="value"
)

# Count rows per feature + diabetes status (ignore value=0/1 split)
counts = (
    df_long
    .groupby(["feature", "Diabetes_binary"])
    .size()
    .reset_index(name="count")
)

# Normalize to 100% per feature
counts["percentage"] = (
    counts.groupby("feature")["count"]
    .transform(lambda x: x / x.sum() * 100)
)

# Horizontal 100% stacked bar chart
fig = px.bar(
    counts,
    x="percentage",
    y="feature",
    color="Diabetes_binary",
    barmode="stack",
    orientation="h",
    labels={
        "feature": "Feature",
        "Diabetes_binary": "Diabetes (0=No, 1=Yes)",
        "percentage": "Percentage (%)"
    },
)

# Force x-axis to 0–100%
fig.update_xaxes(range=[0, 100])

st.plotly_chart(fig, use_container_width=True)
# Add histogram data
# x1 = np.random.randn(200) - 2
# x2 = np.random.randn(200)
# x3 = np.random.randn(200) + 2

# Group data together
# hist_data = [x1, x2, x3]

# group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
# fig = ff.create_distplot(
#        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
# st.plotly_chart(fig, use_container_width=True)


## Plot two

# import plotly.express as px
# import pandas as pd
# df = pd.DataFrame(dict(
#     r=[1, 5, 2, 2, 3],
#   theta=['processing cost','mechanical properties','chemical stability',
#          'thermal stability', 'device integration']))
#fig = px.line_polar(df, r='r', theta='theta', line_close=True)

#st.plotly_chart(fig, use_container_width=True)