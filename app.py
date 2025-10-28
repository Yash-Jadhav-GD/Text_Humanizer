import streamlit as st
import requests
import json
import re

# ---------- CONFIG ----------
DEEPINFRA_API_KEY = "x4XsrhwYBLAsndhnPxopMJJBuLKAnBmt"
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

# ---------- CLEANING FUNCTION ----------
def extract_text(response_json):
    """Extract clean text only, removing JSON and trailing metadata."""
    if isinstance(response_json, dict):
        try:
            return response_json["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            pass
    return "❌ Could not extract text. Check API response."

# ---------- AI GENERATION FUNCTION ----------
def generate_humanized_text(input_text):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPINFRA_API_KEY}"}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a professional editor. Rewrite text to sound fluent, natural, and human without changing meaning."},
            {"role": "user", "content": input_text},
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if response.status_code == 200 and "choices" in result:
            return extract_text(result)
        else:
            return f"❌ Error from API: {result.get('error', {}).get('message', 'Unknown error')}"
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
