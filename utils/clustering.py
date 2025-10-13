import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

# ----- tSNE and UMAP Cluster Analysis
def tsne_clustering_2D(df_sampled):
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    X_tsne = tsne.fit_transform(df_sampled)

    # Put PCA result into a DataFrame
    df_tsne = pd.DataFrame(X_tsne, columns=['tSNE1', 'tSNE2'])
    df_tsne['label'] = df_sampled['Diabetes_binary'].values

    # Separate data by label
    df_0 = df_tsne[df_tsne['label'] == 0]
    df_1 = df_tsne[df_tsne['label'] == 1]

    trace0 = go.Scatter(
        x=df_0['tSNE1'],
        y=df_0['tSNE2'],
        mode='markers',
        name='Label 0',
        marker=dict(size=10, color='blue', symbol='circle'),
        text=df_0.index  # optional: hover text
    )

    trace1 = go.Scatter(
        x=df_1['tSNE1'],
        y=df_1['tSNE2'],
        mode='markers',
        name='Label 1',
        marker=dict(size=10, color='red', symbol='diamond'),
        text=df_1.index
    )

    fig = go.Figure(data=[trace0, trace1])

    fig.update_layout(
        title='tSNE Scatter Plot',
        xaxis_title='tSNE1',
        yaxis_title='tSNE2',
        width=800,
        height=600,
        legend_title_text='Binary Label'
    )

    st.plotly_chart(fig)


def umap_clustering_2D(df_sampled):
    # UMAP
    reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
    X_umap = reducer.fit_transform(df_sampled)

    # Put PCA result into a DataFrame
    df_umap = pd.DataFrame(X_umap, columns=['umap1', 'umap2'])
    df_umap['label'] = df_sampled['Diabetes_binary'].values

    # Separate data by label
    df_0 = df_umap[df_umap['label'] == 0]
    df_1 = df_umap[df_umap['label'] == 1]

    trace0 = go.Scatter(
        x=df_0['umap1'],
        y=df_0['umap2'],
        mode='markers',
        name='Label 0',
        marker=dict(size=10, symbol='circle'),
        text=df_0.index  # optional: hover text
    )

    trace1 = go.Scatter(
        x=df_1['umap1'],
        y=df_1['umap2'],
        mode='markers',
        name='Label 1',
        marker=dict(size=10, symbol='diamond'),
        text=df_1.index
    )

    fig = go.Figure(data=[trace0, trace1])

    fig.update_layout(
        title='UMAP Scatter Plot',
        xaxis_title='UMAP1',
        yaxis_title='UMAP2',
        width=800,
        height=600,
        legend_title_text='Binary Label'
    )

    st.plotly_chart(fig)

def tsne_clustering_3D(df_sampled):
    reducer = umap.UMAP(n_components=3, n_neighbors=15, min_dist=0.1, random_state=42)
    X_umap = reducer.fit_transform(df_sampled)

    # Put PCA result into a DataFrame
    df_umap = pd.DataFrame(X_umap, columns=['umap1', 'umap2', 'umap3'])
    df_umap['label'] = df_sampled['Diabetes_binary'].values

    # Separate data by label
    df_0 = df_umap[df_umap['label'] == 0]
    df_1 = df_umap[df_umap['label'] == 1]

    trace0 = go.Scatter3d(
        x=df_0['umap1'],
        y=df_0['umap2'],
        z=df_0['umap3'],
        mode='markers',
        name='Label 0',
        marker=dict(size=10, symbol='circle'),
        text=df_0.index  # optional: hover text
    )

    trace1 = go.Scatter3d(
        x=df_1['umap1'],
        y=df_1['umap2'],
        z=df_1['umap3'],
        mode='markers',
        name='Label 1',
        marker=dict(size=10, symbol='diamond'),
        text=df_1.index
    )

    fig = go.Figure(data=[trace0, trace1])

    fig.update_layout(
        title='UMAP Scatter Plot',
        scene=dict(
            xaxis_title='UMAP1',
            yaxis_title='UMAP2',
            zaxis_title='UMAP3'
        ),
        width=800,
        height=600,
        legend_title_text='Binary Label'
    )

    st.plotly_chart(fig)