import streamlit as st
import requests
import json

# ---------- CONFIG ----------
DEEPINFRA_API_KEY = "x4XsrhwYBLAsndhnPxopMJJBuLKAnBmt"
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

# ---------- AI GENERATION FUNCTION ----------
def generate_humanized_text(input_text):
    url = f"https://api.deepinfra.com/v1/inference/{MODEL_NAME}"
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": f"Rewrite this text to sound more natural, fluent, and human while keeping its meaning:\n\n{input_text}",
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 400
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        # Debugging output (in case something goes wrong)
        if "results" in result and len(result["results"]) > 0:
            return result["results"][0]["generated_text"].strip()
        elif "output" in result:
            return result["output"].strip()
        else:
            return f"❌ Error from API: {result}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Text Humanizer", page_icon="🧠", layout="centered")
st.title("🧠 AI Text Humanizer")
st.write("Paste your text below to get a smoother, more natural version.")

# Input text box
input_text = st.text_area("✍️ Enter your text:", height=200, placeholder="Paste your text here...")

# Button to run the model
if st.button("✨ Humanize Text"):
    if input_text.strip():
        with st.spinner("Rewriting your text..."):
            output = generate_humanized_text(input_text)
        st.subheader("✅ Humanized Output:")
        st.text_area("🔹 Edited Text:", output, height=200)
    else:
        st.warning("Please enter some text first.")

st.caption("Powered by DeepInfra • Clean text output • No JSON clutter ⚙️")
