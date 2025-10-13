import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


#Added theme colors for the bar charts.
THEME_COLORS = {
    "borderColor": "#4682b4",
    "chartCategoricalColors": ["#4682b4", "#B22222"]
}
st.set_page_config(layout="wide")

st.sidebar.markdown("# Descriptive Analytics")
st.sidebar.image("./assets/LogoFindabetes.png",)

st.markdown("# Descriptive Analytics")

st.markdown("## Statistical analytics performed on the data set")
st.markdown("In this section you will gather more information about the statistical analysis performed on the data set.")

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")
df = load_data()

# Target and available features
target = "Diabetes_binary"
features = [
    "HighBP", "Smoker", "Stroke", "PhysActivity",
    "Fruits", "Veggies", "HvyAlcoholConsump", "HeartDiseaseorAttack",
    "Sex", "DiffWalk"
]

col1, col2 = st.columns(2)

with col1:
    # ---- Q5: Displaying prevalence of diabetes yes/no -----
    st.markdown("## Prevalence of diabetes in the dataset")
    st.markdown("It is also interesting to see how our target class of diabetes distribution within the data set. It is clear that there is a class imbalance, which will be accounted for when training the model.")
    labels = df["Diabetes_binary"].map({0: "No diabetes", 1: "Diabetes"})

    fig = px.pie(
        names=labels,                 
        color=labels,
        color_discrete_map={"No diabetes": "#4682b4", "Diabetes": "#B22222"},
        hole=0.3,                     
        title="Proportion of Participants with and without Diabetes"
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="%{label}: %{percent} (%{value:,})<extra></extra>"
    )

    fig.update_layout(width=500, height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    #Q1: Stacked horizontal diabetes yes/no
    st.markdown("## Diabetes prevalence in every feature")
    st.markdown("We found it useful to understand the percentage of people with diabetes and how they reported the features mentioned. This selectbox allows you to view each feature and the prevalence of diabetes in these features.")

    # Let user select which features to display
    selected_features = st.multiselect(
        label="Choose the features for display:",
        options=features,
        default=['Smoker', 'Stroke', 'HighBP']
    )

    # Only proceed if at least one feature is selected
    if selected_features:
        plot_df = pd.DataFrame()

        # --- Calculate percentage of diabetes vs no diabetes per selected feature ---
        for f in selected_features:
            counts = df[df[f] == 1][target].value_counts(normalize=True) * 100
            plot_df.loc[f, "No Diabetes"] = counts.get(0, 0)
            plot_df.loc[f, "Diabetes"] = counts.get(1, 0)

        # --- Create stacked horizontal bar chart ---
        colors = THEME_COLORS["chartCategoricalColors"][:2]  # keep your color theme
        fig = go.Figure()

        for col, color in zip(plot_df.columns, colors):
            fig.add_trace(go.Bar(
                y=plot_df.index,
                x=plot_df[col],
                name=col,
                orientation='h',
                marker=dict(color=color),
                text=[f"{v:.1f}%" if v > 3 else "" for v in plot_df[col]],
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(color='white', size=11, family='Arial'),
            ))

        # --- Layout adjustments ---
        fig.update_layout(
            barmode='stack',
            xaxis=dict(
                range=[0, 100],
                title="Percent (%)",
                showgrid=False
            ),
            yaxis=dict(
                title="",
                categoryorder='total ascending'
            ),
            title=dict(
                text="Share of patients with and without diabetes (100% stacked)",
                x=0.5,
                xanchor='center'
            ),
            legend=dict(
                title="Diabetes",
                x=1.02,
                y=1,
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=80, r=150, t=60, b=40),
            plot_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one feature to display.")


    # # Q2  What is the distribution of diabetes vs. no diabetes in lifestyle-related features?
    # st.markdown("More interestingly we looked specifically at the distribution of diabetes related to different lifestyle features.")

    # Lifestyle_features = [
    #     "HighBP", "Smoker", "PhysActivity",
    #     "Fruits", "Veggies", "HvyAlcoholConsump",
    # ]

    # chosen_lifestyle_features = st.multiselect(
    #     options=Lifestyle_features, 
    #     label="Select the lifestyle feature to see distribution", 
    #     default=None)

    # if chosen_lifestyle_features:
    #     # Create a crosstab to see the relationship between the chosen feature and Diabetes_binary
    #     crosstab = pd.crosstab((chosen_lifestyle_features), df["Diabetes_binary"])

    #     # Plot the crosstab
    #     crosstab.plot(kind="bar", stacked=True)

    #     plt.title("Proportion of Diabetes cases by lifestyle-related feature of your choice")
    #     plt.xlabel("Lifestyle feature")
    #     plt.ylabel("Count")
    #     plt.legend(title="Diabetes")
    #     plt.grid(False)
    #     st.pyplot(plt)
    # else: 
    #     st.warning("Please select at least one feature to display.")


col1, col2 = st.columns(2)

with col1:
    # ------ Q3: Diabetes prevalence in different age groups ------- 
    st.markdown("## Diabetes prevalence across age groups")
    st.markdown("We were also interested to see how the age affected the prevalence of diabetes. First we seperated our data into groups of age as shown in the table below.")
    age_groups = ['18–24', '25–29', '30–34', '35–39', '40–44', '45–49',
                '50–54', '55–59', '60–64', '65–69', '70–74', '75–79', '80+']
    prev = df.groupby('Age')['Diabetes_binary'].mean().reindex(range(1,14)) * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=age_groups,
            y=prev.values,
            mode="lines+markers",
            line=dict(color="royalblue", width=2),
            marker=dict(size=6, symbol="circle"),
            name="Prevalence",
        )
    )
    fig.update_layout(
        title="Diabetes Prevalence by Age Group",
        xaxis_title="Age Group",
        yaxis_title="Prevalence (%)",
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
        title_font=dict(size=18),
    )
    fig.update_xaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)

    st.plotly_chart(fig, use_container_width=True)

# ----- Q4: The prevalence of diabetes at different BMI-values -----
with col2:
    # Display BMI 
    st.markdown("## Diabetes prevalence across BMI")
    st.markdown("An increased BMI is a known risk for diabetes. We decided to check our dataset to see if this was also supported by our data.")
    # Calculate IQR (Interquartile Range)
    Q1 = df["BMI"].quantile(0.25)
    Q3 = df["BMI"].quantile(0.75)
    IQR = Q3 - Q1

    # Filter the data to keep only BMI values within [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    filtered_df = df[(df["BMI"] >= Q1 - 1.5*IQR) & (df["BMI"] <= Q3 + 1.5*IQR)]

    # Group and calculate diabetes prevalence (%)
    bmi_diabetes = filtered_df.groupby("BMI")["Diabetes_binary"].mean() * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=bmi_diabetes.index,
            y=bmi_diabetes.values,
            mode="lines+markers",
            line=dict(color="royalblue", width=2),
            marker=dict(size=6, symbol="circle"),
            name="Prevalence",
        )
    )
    fig.update_layout(
        title="Diabetes Prevalence by BMI",
        xaxis_title="BMI",
        yaxis_title="Prevalence (%)",
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
        title_font=dict(size=18),
    )
    fig.update_xaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)

    st.plotly_chart(fig, use_container_width=True)


# ------ Boxplot Distribution Plot ------
st.markdown("## Distribution of BMI values per age group grouped by diabetes in the dataset")
st.markdown("How is the BMI distributed per age group related to our target class of diabetes")

age_bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, float('inf')]
age_labels = ['18–24', '25–29', '30–34', '35–39', '40–44', '45–49',
            '50–54', '55–59', '60–64', '65–69', '70–74', '75–79', '80+']
df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=True, ordered=True)


### ------- BMI over Age Groups Boxplot -------

fig = px.box(
    df,
    x="AgeGroup",
    y="BMI",
    color="Diabetes_binary",
    color_discrete_map={0: "#4682b4", 1: "#B22222"},  # custom palette
    points="outliers",  # show outliers as individual points
    category_orders={"AgeGroup": age_labels},  # <-- optional explicit order
    labels={
        "AgeGroup": "Age Group",
        "BMI": "BMI",
        "Diabetes": "Diabetes Status"
    },
    title="BMI Distribution by Age Group and Diabetes Status",
)

# --- Customize layout ---
fig.update_layout(
    boxmode="group",  # side-by-side boxes per age group
    xaxis_title="Age Group",
    yaxis_title="BMI",
    legend_title="Diabetes",
    legend=dict(
        x=1.02,
        y=1,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    title_font=dict(size=16, family="Arial", color="black"),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# --- Optional: tidy gridlines ---
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)



### ------- Mental Health over Age Groups Boxplot -------

fig = px.box(
    df,
    x="AgeGroup",
    y="MentHlth",
    color="Diabetes_binary",
    color_discrete_map={0: "#4682b4", 1: "#B22222"},  # custom palette
    points="outliers",  # show outliers as individual points
    category_orders={"AgeGroup": age_labels},  # <-- optional explicit order
    labels={
        "AgeGroup": "Age Group",
        "MentHlth": "Mental Health",
        "Diabetes": "Diabetes Status"
    },
    title="Mental Health Distribution by Age Group and Diabetes Status",
)

# --- Customize layout ---
fig.update_layout(
    boxmode="group",  # side-by-side boxes per age group
    xaxis_title="Age Group",
    yaxis_title="Mental Health",
    legend_title="Diabetes",
    legend=dict(
        x=1.02,
        y=1,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    title_font=dict(size=16, family="Arial", color="black"),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# --- Optional: tidy gridlines ---
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)



### ------- General Health over Age Groups Boxplot -------

fig = px.box(
    df,
    x="AgeGroup",
    y="GenHlth",
    color="Diabetes_binary",
    color_discrete_map={0: "#4682b4", 1: "#B22222"},  # custom palette
    points="outliers",  # show outliers as individual points
    category_orders={"AgeGroup": age_labels},  # <-- optional explicit order
    labels={
        "AgeGroup": "Age Group",
        "GenHlth": "General Health",
        "Diabetes": "Diabetes Status"
    },
    title="General Health Distribution by Age Group and Diabetes Status",
)

# --- Customize layout ---
fig.update_layout(
    boxmode="group",  # side-by-side boxes per age group
    xaxis_title="Age Group",
    yaxis_title="General Health",
    legend_title="Diabetes",
    legend=dict(
        x=1.02,
        y=1,
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    title_font=dict(size=16, family="Arial", color="black"),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# --- Optional: tidy gridlines ---
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgrey')

# --- Display in Streamlit ---
st.plotly_chart(fig, use_container_width=True)