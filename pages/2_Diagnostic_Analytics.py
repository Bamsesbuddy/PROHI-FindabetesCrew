import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(layout="wide")

st.markdown("# Diagnostic Analytics")

st.sidebar.markdown("# Diagnostic Analytics")
st.sidebar.image("./assets/LogoFindabetes.png")

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")
df = load_data()
df = df.drop(columns=['HvyAlcoholConsump'])

# ---- Heatmap Correlation -----
st.subheader("Interactive correlation heatmap")
# Target and available features
target = "Diabetes"
df['Diabetes'] = df['Diabetes_binary']
features = [
    "HighBP", "Smoker", "Stroke", "PhysActivity",
    "Fruits", "Veggies", "HeartDiseaseorAttack",
    "Sex", "DiffWalk"
]
heatmap_features = st.multiselect(
    "Select what features you wish to see in the heatmap.", 
    features, 
    default=['HighBP', 'Smoker', 'PhysActivity'])

if heatmap_features:
    corr = df.select_dtypes("number").corr(numeric_only=True)
    corr_row = corr.loc[[target], heatmap_features]

    st.markdown("The red shows a strong indication for being correlated to having diabetes, and blue shows strong correlation for not having diabetes." \
    "The stronger the color, the stronger the correlation. The features response is assumed positive in this matrix.")
    fig = px.imshow(
        corr_row,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        zmin=-1, zmax=1,
    )
    fig.update_traces(
        textfont=dict(color='Black', size=18),
    )
    fig.update_layout(
        title_text = 'Correlation between Diabetes and selected Features',
        title_font=dict(size=18),
        coloraxis_colorbar=dict(
            title="Correlation",
            tickfont=dict(size=14)
        ),
        xaxis=dict(
            title=dict(
                text="Features",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=14),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(
                text="Target",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=14),
            categoryorder='total ascending'
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    for annotation in fig.layout.annotations:
        annotation.font.size = 14
        annotation.font.color = "black"
    st.plotly_chart(fig, use_container_width=True)
else: 
    st.warning("Please select at least one feature to display.")

st.divider()

# ---- PCA cluster Analysis ----
st.subheader("Interactive Cluster Analysis")

sample_frac = 0.05  # fraction of data you want to sample

# stratified sampling
df_sampled, _ = train_test_split(
    df,
    test_size=1 - sample_frac,
    stratify=df['Diabetes_binary'],
    random_state=42
)

features = df_sampled.drop(columns=['Diabetes_binary'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

col1, col2 = st.columns(2)
# ---- PCA 2D Analysis ----

pca = PCA(n_components=2)  # reduce to 2 dimensions for plotting
X_pca = pca.fit_transform(X_scaled)

# Put PCA result into a DataFrame
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['label'] = df_sampled['Diabetes_binary'].values

# Separate data by label
df_0 = df_pca[df_pca['label'] == 0]
df_1 = df_pca[df_pca['label'] == 1]

with col1:
    trace0 = go.Scatter(
        x=df_0['PC1'],
        y=df_0['PC2'],
        mode='markers',
        name='No Diabetes',
        marker=dict(size=5, color="#4682b4", symbol='circle'),
        text=df_0.index  # optional: hover text
    )

    trace1 = go.Scatter(
        x=df_1['PC1'],
        y=df_1['PC2'],
        mode='markers',
        name='Diabetes',
        marker=dict(size=5, color="#B22222", symbol='diamond'),
        text=df_1.index
    )

    fig = go.Figure(data=[trace0, trace1])

    fig.update_layout(
        title='2D PCA Scatter Plot',
        xaxis_title='PC1',
        yaxis_title='PC2',
        width=800,
        height=600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title_text='Absence/Presence Diabetes',
        xaxis=dict(
            title=dict(
                text="PC1",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(
                text="PC2",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12),
            categoryorder='total ascending'
        ),
    )

    st.plotly_chart(fig)

# ---- 3D PCA ----
pca = PCA(n_components=3)  # reduce to 2 dimensions for plotting
X_pca = pca.fit_transform(X_scaled)

# Put PCA result into a DataFrame
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2', 'PC3'])
df_pca['label'] = df_sampled['Diabetes_binary'].values

# Separate data by label
df_0 = df_pca[df_pca['label'] == 0]
df_1 = df_pca[df_pca['label'] == 1]

with col2:
    with st.container(border=True):
        st.markdown(
            """
            Principal Component Analysis (PCA) projects high-dimensional data onto orthogonal axes - 
            number of principal components (PC) - that explain the largest variance in the data.
            
            Both Diabetes (red) and No Diabetes (blue) points overlap heavily in the center. 
            There’s no distinct, well-separated cluster—instead, there’s a large mixed distribution. 
            The Diabetes points may be slightly shifted toward the right-hand side or more spread out, 
            but not clearly distinct.
            
            PC1 and PC2 do not strongly separate diabetic from non-diabetic individuals. 
            This means that the main sources of variance captured by PCA are not primarily 
            driven by diabetes status. Diabetes might influence other features, but that variance 
            is either subtle or exists along higher components.
            """
        )

st.divider()

st.subheader("Self-reported Physical and Mental Health")

# --- Data prep (same as your code) ---
df_plot = df[['Age','PhysHlth','MentHlth','Diabetes_binary']].copy()
df_plot['PhysHlth'] = -df_plot['PhysHlth']   # Invert values as higher = better
df_plot['MentHlth'] = -df_plot['MentHlth']
df_plot['Diabetes'] = np.where(df_plot['Diabetes_binary']==1, 'Diabetes', 'No diabetes')

age_map = {
    1: '18–24',  2: '25–29',  3: '30–34',  4: '35–39',
    5: '40–44',  6: '45–49',  7: '50–54',  8: '55–59',
    9: '60–64', 10: '65–69', 11: '70–74', 12: '75–79',
    13: '80+'
}
order = list(age_map.values())

df_plot['age_group'] = df_plot['Age'].map(age_map)
df_plot['age_group'] = pd.Categorical(df_plot['age_group'], categories=order, ordered=True)

# --- Compute mean values by group ---
mean_phys = df_plot.groupby(['age_group', 'Diabetes'])['PhysHlth'].mean().reset_index()
mean_ment = df_plot.groupby(['age_group', 'Diabetes'])['MentHlth'].mean().reset_index()

colors = {'Diabetes': '#d62728', 'No diabetes': '#1f77b4'}

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    # --- Left subplot: Physical Health ---
    for diabetes_status in ['No diabetes', 'Diabetes']:
        subset = mean_phys[mean_phys['Diabetes'] == diabetes_status]
        fig.add_trace(
            go.Scatter(
                x=subset['age_group'],
                y=subset['PhysHlth'],
                mode='lines+markers',
                name=diabetes_status,
                line=dict(color=colors[diabetes_status]),
                marker=dict(size=6)
            ),
        )
    # --- Layout styling ---
    fig.update_layout(
        title_text='Number of past days with physical health problems across age groups',
        title_font=dict(size=18),
        width=950,
        height=550,
        plot_bgcolor="white",
        paper_bgcolor="white",
        template="plotly_white",
        legend_title_text='Diabetes',
        font=dict(color='black', size=14),
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(
            title=dict(
                text="Age Group",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12)
        ),
        yaxis=dict(
            title=dict(
                text="Past days",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12)
        ),
    )

    # --- Show figure (for Streamlit) ---
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    # --- Right subplot: Mental Health ---
    for diabetes_status in ['No diabetes', 'Diabetes']:
        subset = mean_ment[mean_ment['Diabetes'] == diabetes_status]
        fig.add_trace(
            go.Scatter(
                x=subset['age_group'],
                y=subset['MentHlth'],
                mode='lines+markers',
                name=diabetes_status,
                line=dict(color=colors[diabetes_status]),
                marker=dict(size=6),
            ),
        )

    # --- Layout styling ---
    fig.update_layout(
        title_text='Number of past days with mental health problems across age groups',
        title_font=dict(size=18),
        width=1050,
        height=550,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title_text='Diabetes',
        font=dict(color='black', size=14),
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(
            title=dict(
                text="Age Group",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12)
        ),
        yaxis=dict(
            title=dict(
                text="Past days",
                font=dict(color="black", size=16)
            ),
            tickfont=dict(color="black", size=12)
        ),
    )

    # --- Show figure (for Streamlit) ---
    st.plotly_chart(fig, use_container_width=True)