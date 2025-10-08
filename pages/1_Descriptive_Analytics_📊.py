import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.markdown("# Descriptive Analytics 📊")

st.sidebar.markdown("# Descriptive Analytics")
st.sidebar.image("./assets/LogoFindabetes.png",)

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")
df = load_data()


#Q1: Stacked horizontal diabetes yes/no
# Target and available features
target = "Diabetes_binary"
features = [
    "HighBP", "Smoker", "Stroke", "PhysActivity",
    "Fruits", "Veggies", "HvyAlcoholConsump", "HeartDiseaseorAttack",
    "Sex", "DiffWalk"
]

# Let user select which features to display
selected_features = st.multiselect(
    label="Choose the features for display:",
    options=features,
    default=None  # optional: pre-select allstr
)

# Only proceed if at least one feature is selected
if selected_features:
    plot_df = pd.DataFrame()

    # Calculate percentage of diabetes vs no diabetes per selected feature
    for f in selected_features:
        counts = df[df[f] == 1][target].value_counts(normalize=True) * 100
        plot_df.loc[f, "No diabetes"] = counts.get(0, 0)
        plot_df.loc[f, "Diabetes"] = counts.get(1, 0)

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(9, 6))
    plot_df.plot(kind="barh", stacked=True, ax=ax)

    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent (%)")
    ax.set_title("Share of patients with and without diabetes (100% stacked)")
    ax.legend(title="Diabetes", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.grid(False)
    plt.tight_layout()

    st.pyplot(fig)

else:
    st.warning("Please select at least one feature to display.")



# Q2  What is the distribution of diabetes vs. no diabetes in lifestyle-related features?
st.markdown("## Distribution of Diabetes yes/no realted to different lifestyle features.")

Lifestyle_features = [
    "HighBP", "Smoker", "PhysActivity",
    "Fruits", "Veggies", "HvyAlcoholConsump",
]

chosen_lifestyle_features = st.selectbox(options=Lifestyle_features, label="Select the lifestyle feature to see distribution")

# Create a crosstab to see the relationship between HighBP and Diabetes_binary
crosstab = pd.crosstab((chosen_lifestyle_features), df["Diabetes_binary"])

# Plot the crosstab
crosstab.plot(kind="bar", stacked=True)

plt.title("Proportion of Diabetes cases by lifestyle-related feature of your choice")
plt.xlabel("Lifestyle feature")
plt.ylabel("Count")
plt.legend(title="Diabetes")
plt.grid(False)
st.pyplot(plt)

#Q3 
st.markdown("## Diabetes prevalence in different age groups")
age_groups = ['18–24', '25–29', '30–34', '35–39', '40–44', '45–49',
              '50–54', '55–59', '60–64', '65–69', '70–74', '75–79', '80+']
prev = df.groupby('Age')['Diabetes_binary'].mean().reindex(range(1,14)) * 100

# Style
import seaborn as sns
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10,6))

# Line + markers
sns.lineplot(x=age_groups,
             y=prev.values,
             marker="o",
             linewidth=2.5,
             color="#1f77b4",
             markerfacecolor="#1f77b4",
             markeredgewidth=2)

# Labels & title
plt.title("Diabetes Prevalence by Age Group", fontsize=16, weight="bold", pad=15)
plt.xlabel("Age Group", fontsize=13)
plt.ylabel("Prevalence (%)", fontsize=13)

# Y-axis formatting
plt.ylim(0, prev.max() + 5)
plt.yticks(range(0, int(prev.max())+10, 5))

# Rotate x-labels slightly for readability
plt.xticks(rotation=30)

# Add data labels on each point
for x, y in zip(age_groups, prev.values):
    plt.text(x, y + 1, f"{y:.1f}%", ha="center", va="bottom", fontsize=10)

plt.tight_layout()
st.pyplot(plt)

#Q4
# Display BMI 
st.markdown("## The prevalence of diabetes at different BMI-values")
# Calculate IQR (Interquartile Range)
Q1 = df["BMI"].quantile(0.25)
Q3 = df["BMI"].quantile(0.75)
IQR = Q3 - Q1

# Filter the data to keep only BMI values within [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
filtered_df = df[(df["BMI"] >= Q1 - 1.5*IQR) & (df["BMI"] <= Q3 + 1.5*IQR)]

# Group and calculate diabetes prevalence (%)
bmi_diabetes = filtered_df.groupby("BMI")["Diabetes_binary"].mean() * 100

# Plot
plt.figure(figsize=(8, 5))
plt.plot(bmi_diabetes.index, bmi_diabetes.values, color='tab:blue', marker='o')

plt.title("Diabetes Prevalence by BMI")
plt.xlabel("BMI")
plt.ylabel("Prevalence (%)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(plt)

#Q5: Displaying prevalence of diabetes yes/no 
st.markdown("## Prevalence of diabetes in the dataset")
labels = df["Diabetes_binary"].map({0: "No diabetes", 1: "Diabetes"})

fig = px.pie(
    names=labels,                 
    color=labels,
    color_discrete_map={"No diabetes": "#1f77b4", "Diabetes": "#ff7f0e"},
    hole=0.3,                     
    title="Proportion of Participants with and without Diabetes"
)

fig.update_traces(
    textinfo="percent+label",
    hovertemplate="%{label}: %{percent} (%{value:,})<extra></extra>"
)

fig.update_layout(width=500, height=500, showlegend=False)
st.plotly_chart(fig, use_container_width=True)
# Add here some descriptive analytics with Widgets and Plots

### ⚠️ In-class exercise: Integrate a plot from plotly examples

# 🔗 Link: <https://plotly.com/python/scientific-charts/>

# import plotly.figure_factory as ff

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
# list_of_selected_features = st.multiselect("Select the features you want displayed", X.columns.tolist(), default=X.columns.tolist())
# features to pick shouldnt contain target diabetes. 

fig = px.bar(
    df,
    x= st.selectbox("Select the features you want displayed", options=df.columns),
    y= counts("percentage"),
    color="Diabetes_binary",
    barmode="stack",
    orientation="h",
    labels={
        "feature": "features",
        "Diabetes_binary": "Diabetes (0=No, 1=Yes)",
        "percentage": "Percentage (%)"
    },
    text="percentage"
)


st.subheader("Diabetes distribution for features (100% stacked, single bar per feature)")

features = ["HighBP", "Smoker", "PhysActivity", "HvyAlcoholConsump", "Sex", "DiffWalk", "Stroke", "Fruits", "Veggies"]

# Melt: reshape into long form
df_long = df.melt(
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

