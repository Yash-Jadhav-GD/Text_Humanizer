import streamlit as st
import json
import re
from g4f import ChatCompletion, Provider

# ---------- CLEANING FUNCTION ----------
def extract_text(response):
    """Extract clean text only, removing JSON and trailing metadata."""
    text = str(response)

    # Try JSON extraction
    try:
        data = json.loads(text)
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if content:
            return content.strip()
    except Exception:
        pass

    # Fallback regex extraction
    match = re.search(r"'content':\s*'([^']+)'", text)
    if match:
        text = match.group(1)

    # Remove trailing metadata
    text = re.split(r",\s*'finish_reason'|,\s*'logprobs'|,\s*'usage'|\}\}|\}\]", text)[0]

    # Trim at last sentence punctuation
    if any(p in text for p in [".", "!", "?"]):
        last_punct = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
        text = text[: last_punct + 1]

    # Clean up escape chars
    text = text.replace("\\n", " ").replace("\\", "").strip()
    return text


# ---------- AI GENERATION FUNCTION ----------
providers_and_models = [
    (Provider.DeepInfra, "deepseek-ai/DeepSeek-V3"),
    (Provider.DeepInfra, "meta-llama/Llama-3.3-70B-Instruct"),
    (Provider.DeepInfra, "mistralai/Mistral-Small-3.2-24B-Instruct-2506"),
    (Provider.DeepInfra, "microsoft/phi-4"),
    (Provider.DeepInfra, "Qwen/Qwen3-235B-A22B-Instruct-2507"),
]

def generate_humanized_text(input_text):
    prompt = f"""
    Rewrite the following text to sound more natural, fluent, and human.
    Maintain the meaning, but make it smoother and conversational.

    Text:
    {input_text}
    """

    for provider, model in providers_and_models:
        try:
            response = ChatCompletion.create(
                model=model,
                provider=provider,
                messages=[{"role": "user", "content": prompt}],
            )
            clean_output = extract_text(response)
            if clean_output:
                st.subheader("⏳Humanising your text", divider=True)
                #st.success("⏳Humanising your text")
                #st.success(f"✅ Response from: {provider.__name__} | Model: {model}")
                return clean_output
        except Exception as e:
            st.warning(f"⚠️ {provider.__name__} ({model}) failed: {e}")
            continue

    return "❌ All providers failed. Please try again later."


# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Text Humanizer", page_icon="🧠", layout="centered")
st.title("🧠 AI Text Humanizer")
st.write("Paste your text below to get a smoother, more human-like version.")

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

st.caption("Powered by GPT4Free • Clean text output • No JSON clutter ⚙️")
