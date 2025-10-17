import altair as alt
import pandas as pd
import io
import requests
import json
from PIL import Image
import base64
from huggingface_hub import InferenceClient

def make_donut(input_response, input_text, input_color, size=180):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    source = pd.DataFrame({
        "Topic": ['', input_text],
        "Value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "Value": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=0).encode(
        theta="Value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=size, height=size)

    text = plot.mark_text(align='center', color="#29b5e8", font="Calibri", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="Value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=size, height=size)
    return plot_bg + plot + text


def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def compress_image(base64_str, max_size=(512, 512)):
    img = Image.open(io.BytesIO(base64.b64decode(base64_str.split(",")[1])))
    img.thumbnail(max_size)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def llama_vision(image):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2-vision",
        "prompt": f"""
        You are an Analyzer and Summarizer of my explainability SHAP data:
        
        Analyze the given image of SHAP feature importances and analyze the SHAP values for the features in 
        the context of Type-2 diabetes risk assessment. 
        
        Give a short summary of the values and give an interpretation of the values for specific patient with 
        clinical background.
        
        Please keep in mind that the explainations or summaries are intended for clinicans, so keep a sufficient
        medical scientific background to the summary.  
        """,
        "images": compress_image(image),
        "stream": False
    }

    payload["options"] = {"num_predict": 150}  # ~ short paragraph

    response = requests.post(url, json=payload)
    return json.loads(response.text)["response"]

def llama_data(data, pred):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",  # text-only model is fine here
        "prompt": f"""
        You are a clinical decision support assistant specialized in endocrinology and metabolic disorders.

        You are given SHAP feature importance values for a predictive model estimating a patient's **risk of Type 2 Diabetes**. 
        Each feature’s SHAP value represents how much it increases or decreases the model’s predicted risk. 
        Positive SHAP values indicate stronger contribution *toward higher diabetes risk*, while negative values indicate *protective effects*.

        Here are the feature SHAP values for this patient:
        {data}

        Here is the predicted risk of Type-2 diabetes for the specific patient in %:
        {pred}

        Please provide a short, clinician-oriented interpretation by doing the following:
        1. Summarize the **top 3–5 most influential features**, noting whether each increases or decreases diabetes risk.  
        2. Explain these findings in **clinical terms**, relating them to pathophysiology or risk factors (e.g., obesity, hypertension, physical inactivity, diet, metabolic syndrome).  
        3. Conclude with a **concise 3–5 sentence summary** that contextualizes the risk profile and potential next clinical considerations (e.g., lifestyle modification, screening follow-up, further lab testing).

        The output should be clear, evidence-informed, and phrased for **healthcare professionals** (not patients).  
        Avoid generic statements — tie your reasoning directly to the SHAP feature effects above.
        """,
        "stream": False,
        #  "options": {"num_predict": 200, "temperature": 0.2}
    }

    response = requests.post(url, json=payload)
    return json.loads(response.text)["response"]

def huggingface_model(image):
    client = InferenceClient(model="liuhaotian/llava-v1.6-vicuna-7b")

    #  st.write(client.model)

    response = client.text_generation(
        prompt="""
        Analyze this image and describe the SHAP values for the features in 
        the context of Type-2 diabetes risk assessment. Please keep in mind that the explainations or summaries
        are intended for clinicans, so keep a medical scientific background to the summary. Don't make the summary too technical 
        and do not include the word SHAP - just make it intuitive for the clinician. 
        """,
        images=[image]
    )

    return json.loads(response.text)["response"] 