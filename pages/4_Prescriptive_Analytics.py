import streamlit as st
import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("# Patient prescription 🎯")

# Load model
pre_trained_model_path = "./assets/best_model_so_far.pkl"
model = joblib.load(pre_trained_model_path)

X = pd.read_csv("data/input_data.csv")  # THIS must match the features (columns) the model expects

# ---- IMPORTANT: make sure X is preprocessed exactly like during training ----
# If your model is a sklearn Pipeline that does preprocessing internally, you can pass raw X.
# If the model expects numeric preprocessed arrays, apply same preprocessing here (encoder/scaler).

# ---- build a SHAP explainer (robust with fallbacks) ----
try:
    # Preferred: generic Explainer with model + background
    explainer = shap.Explainer(model, X)       # will pick a good backend if possible
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
# show shapes for debugging
try:
    st.write("shap values shape:", shap_expl.values.shape)
    st.write("base_values shape:", shap_expl.base_values.shape)
except Exception:
    st.write("Could not show shapes; continuing to plotting.")

col1, col2 = st.columns(2)
# ---- Global summary plot (beeswarm) ----
with col1:
    fig = plt.figure(figsize=(8, 4))
    # using new API plotting helper: beeswarm is a matplotlib plot
    shap.plots.beeswarm(shap_expl[:, :, 1])   # or shap.plots.bar(shap_expl) for aggregated importance
    plt.tight_layout()
    st.pyplot(fig)

with col2: 
    # ---- Local explanation for instance 0: waterfall ----
    i = 0  # pick an instance index; change as needed or loop
    fig = plt.figure(figsize=(8, 4))
    shap.plots.waterfall(shap_expl[i, :, 1])   # waterfall works well for one instance
    plt.tight_layout()
    st.pyplot(fig)