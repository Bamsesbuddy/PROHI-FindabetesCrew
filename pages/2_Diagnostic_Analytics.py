import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objs as go

st.markdown("# Diagnostic Analytics")

st.sidebar.markdown("# Diagnostic Analytics")
st.sidebar.image("./assets/LogoFindabetes.png")

# The code for storing the processed dataset data.csv
@st.cache_data
def load_data():
    return pd.read_csv("data/data.csv")
df = load_data()


# ---- Heatmap Correlation -----
st.subheader("Interactive correlation heatmap")
# Target and available features
target = "Diabetes_binary"
features = [
    "HighBP", "Smoker", "Stroke", "PhysActivity",
    "Fruits", "Veggies", "HvyAlcoholConsump", "HeartDiseaseorAttack",
    "Sex", "DiffWalk"
]
heatmap_features = st.multiselect(
    "Select what features you wish to see in the heatmap.", 
    features, 
    default=None)

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
        title="Correlation between Diabetes and other features"
    )
    st.plotly_chart(fig, use_container_width=True)
else: 
    st.warning("Please select at least one feature to display.")


# ---- PCA cluster Analysis ----

st.subheader("Interactive Cluster Analysis")

sample_frac = 0.2  # fraction of data you want to sample

# stratified sampling
df_sampled, _ = train_test_split(
    df,
    test_size=1 - sample_frac,
    stratify=df['Diabetes_binary'],
    random_state=42
)

from sklearn.preprocessing import StandardScaler

features = df_sampled.drop(columns=['Diabetes_binary'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

from sklearn.decomposition import PCA

pca = PCA(n_components=2)  # reduce to 2 dimensions for plotting
X_pca = pca.fit_transform(X_scaled)

# Put PCA result into a DataFrame
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['label'] = df_sampled['Diabetes_binary'].values

# Separate data by label
df_0 = df_pca[df_pca['label'] == 0]
df_1 = df_pca[df_pca['label'] == 1]

trace0 = go.Scatter(
    x=df_0['PC1'],
    y=df_0['PC2'],
    mode='markers',
    name='Label 0',
    marker=dict(size=10, color='blue', symbol='circle'),
    text=df_0.index  # optional: hover text
)

trace1 = go.Scatter(
    x=df_1['PC1'],
    y=df_1['PC2'],
    mode='markers',
    name='Label 1',
    marker=dict(size=10, color='red', symbol='diamond'),
    text=df_1.index
)

fig = go.Figure(data=[trace0, trace1])

fig.update_layout(
    title='PCA Scatter Plot with Graph Objects',
    xaxis_title='PC1',
    yaxis_title='PC2',
    width=800,
    height=600,
    legend_title_text='Binary Label'
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


trace0 = go.Scatter3d(
    x=df_0['PC1'],
    y=df_0['PC2'],
    z=df_0['PC3'],
    mode='markers',
    name='Label 0',
    marker=dict(size=5),
    text=df_0.index,  # optional hover info
    hovertemplate='Index: %{text}<br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>PC3: %{z:.2f}<extra></extra>'
)

trace1 = go.Scatter3d(
    x=df_1['PC1'],
    y=df_1['PC2'],
    z=df_1['PC3'],
    mode='markers',
    name='Label 1',
    marker=dict(size=5),
    text=df_1.index,
    hovertemplate='Index: %{text}<br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>PC3: %{z:.2f}<extra></extra>'
)

fig = go.Figure(data=[trace0, trace1])

fig.update_layout(
    title='3D PCA Scatter Plot',
    scene=dict(
        xaxis_title='PC1',
        yaxis_title='PC2',
        zaxis_title='PC3'
    ),
    width=900,
    height=700,
    legend_title_text='Binary Label'
)

st.plotly_chart(fig)