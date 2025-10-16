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
target = "Diabetes_binary"
features = [
    "HighBP", "Smoker", "Stroke", "PhysActivity",
    "Fruits", "Veggies", "HeartDiseaseorAttack",
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
    trace0 = go.Scatter3d(
        x=df_0['PC1'],
        y=df_0['PC2'],
        z=df_0['PC3'],
        mode='markers',
        name='No Diabetes',
        marker=dict(size=3, color="#4682b4", symbol='diamond'),
        text=df_0.index,  # optional hover info
        hovertemplate='Index: %{text}<br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>PC3: %{z:.2f}<extra></extra>'
    )

    trace1 = go.Scatter3d(
        x=df_1['PC1'],
        y=df_1['PC2'],
        z=df_1['PC3'],
        mode='markers',
        name='Diabetes',
        marker=dict(size=3, color="#B22222", symbol='diamond'),
        text=df_1.index,
        hovertemplate='Index: %{text}<br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>PC3: %{z:.2f}<extra></extra>'
    )

    fig = go.Figure(data=[trace0, trace1])

    fig.update_layout(
        title='3D PCA Scatter Plot',
        width=900,
        height=700,
        legend_title_text='Absence/Presence Diabetes',
        scene=dict(
            xaxis=dict(
                title=dict(text='PC1', font=dict(color='black', size=16)),
                tickfont=dict(color='black', size=12),
                showgrid=False,
            ),
            yaxis=dict(
                title=dict(text='PC2', font=dict(color='black', size=16)),
                tickfont=dict(color='black', size=12),
            ),
            zaxis=dict(
                title=dict(text='PC3', font=dict(color='black', size=16)),
                tickfont=dict(color='black', size=12),
            )
        )
    )

    st.plotly_chart(fig)

with st.container(border=True):
    st.markdown(
        """
        Principal Component Analysis (PCA) projects high-dimensional data onto orthogonal axes 
        (number of components) that explain the largest variance in the data.
        
        Both “Diabetes” (red) and “No Diabetes” (blue) points overlap heavily in the center. 
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

# --- Create 1x2 subplot figure ---
fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                    subplot_titles=("Physical health by age group", "Mental health by age group"))

colors = {'Diabetes': '#d62728', 'No diabetes': '#1f77b4'}

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
        row=1, col=1
    )

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
            showlegend=(diabetes_status == 'Diabetes')  # legend on right subplot only
        ),
        row=1, col=2
    )

# --- Layout styling ---
fig.update_layout(
    title_text='Physical & Mental Health by Age and Diabetes Status',
    title_x=0.5,
    width=950,
    height=450,
    plot_bgcolor='white',
    legend_title_text='Diabetes',
    font=dict(color='black', size=14)
)

# --- Axis formatting ---
# fig.update_xaxes(title_text='Age Group', tickfont=dict(color='black', size=12),
#                  titlefont=dict(color='black', size=14), row=1, col=1)
# fig.update_xaxes(title_text='Age Group', tickfont=dict(color='black', size=12),
#                  titlefont=dict(color='black', size=14), row=1, col=2)

# fig.update_yaxes(title_text='Average (higher = better)', tickfont=dict(color='black', size=12),
#                  titlefont=dict(color='black', size=14), row=1, col=1)
# fig.update_yaxes(tickfont=dict(color='black', size=12), row=1, col=2)

# --- Show figure (for Streamlit) ---
st.plotly_chart(fig, use_container_width=True)