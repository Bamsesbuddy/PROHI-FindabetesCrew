import streamlit as st
import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import expit
import numpy as np
from pages.helper import make_donut

st.set_page_config(layout="wide")

st.sidebar.markdown("# Explainability of a specific instance")
st.sidebar.image("./assets/LogoFindabetes.png")

st.markdown("# Patient prescription 🎯")

# Load model
pre_trained_model_path = "./jupyter-notebooks/hgb_classifier.pkl"
model = joblib.load(pre_trained_model_path)

X = pd.read_csv("data/input_data.csv")  # THIS must match the features (columns) the model expects

# ---- IMPORTANT: make sure X is preprocessed exactly like during training ----
# If your model is a sklearn Pipeline that does preprocessing internally, you can pass raw X.
# If the model expects numeric preprocessed arrays, apply same preprocessing here (encoder/scaler).

# ---- build a SHAP explainer (robust with fallbacks) ----
try:
    # Preferred: generic Explainer with model + background
    explainer = shap.Explainer(model, feature_names=X.columns)
except Exception as e:
    st.write("shap.Explainer() failed:", e)
    # Try TreeExplainer (fast for tree models)
    try:
        explainer = shap.TreeExplainer(model)
    except Exception as e2:
        st.write("TreeExplainer failed:", e2)
        # Fallback to KernelExplainer (slow), needs a predict function and a small background sample
        predict_fn = model.predict_proba if hasattr(model, "predict_proba") else model.predict
        background = X.sample(n=min(100, len(X)), random_state=0)
        explainer = shap.KernelExplainer(predict_fn, background)

# ---- compute SHAP values (new API) ----
shap_expl = explainer(X)   # returns shap.Explanation
prob = model.predict_proba(X)
base_logit = explainer.expected_value
shap_sum_logit = base_logit + shap_expl.values.sum()
shap_prob = expit(shap_sum_logit)

st.header('Patient-Level Insights')

col1, col2 = st.columns(2)
# ---- Global summary plot (beeswarm) ----
with col1:

    fig = plt.figure(figsize=(8, 4))
    shap.plots.bar(shap_expl) 
    plt.tight_layout()
    st.pyplot(fig)

with col2: 
    fig = plt.figure(figsize=(8, 4))
    shap.plots.waterfall(shap_expl[0])
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("🧠 Counterfactual What-If Explorer")
st.write("Adjust the top 5 most important features and observe how the model’s prediction changes.")

shap_importance = np.abs(shap_expl.values).mean(axis=0)
top_features = pd.Series(shap_importance, index=X.columns).sort_values(ascending=False).head(5)
top_features_list = top_features.index.tolist()

col1, col2 = st.columns(2)
with col1:
    for i, feature in enumerate(top_features_list):
        if feature in ['High BP', 'Smoker','Stroke','Heart Disease or Attack','Physical Activity','Fruits','Veggies','Heavy Alcohol Consumption', 'Difficulties Walking']:
            default_value = 'Yes' if int(X[feature]) > 0.5 else 'No'
            value = st.select_slider(label=f'{feature} - Yes or No: ', options=['Yes', 'No'], value=default_value)
            X[feature] = 1 if value == 'Yes' else 0
        elif feature in ['BMI', 'General Health', 'Mental Health']:
            X[feature] = st.number_input(label=f'Select {feature}: ', value=X[feature])
        elif feature in ['Age']:
            X[feature] = st.slider(label=f'Select {feature}: ', min_value=0, max_value=100, value=int(X[feature]))

pred_prob = model.predict_proba(X)[0, 1]
donut_class_one = make_donut(int(pred_prob * 100), 'Outbound Migration', 'red')

with col2:
    st.altair_chart(donut_class_one)

### Link to giudelines (recommendations outside of scope)

### GenAI model 