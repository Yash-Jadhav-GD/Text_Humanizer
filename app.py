import streamlit as st
import json
import re
from g4f import ChatCompletion, Provider

# ---------- CLEANING FUNCTION ----------
def extract_text(response):
    """Extract clean text only, removing JSON and trailing metadata."""
    text = str(response)

    try:
        data = json.loads(text)
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if content:
            return content.strip()
    except Exception:
        pass

    match = re.search(r"'content':\s*'([^']+)'", text)
    if match:
        text = match.group(1)

    text = re.split(r",\s*'finish_reason'|,\s*'logprobs'|,\s*'usage'|\}\}|\}\]", text)[0]
    if any(p in text for p in [".", "!", "?"]):
        last_punct = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
        text = text[: last_punct + 1]

    text = text.replace("\\n", " ").replace("\\", "").strip()
    return text


# ---------- PROVIDERS ----------
# ✅ These work without login or API key
providers = [
    Provider.H2o,           # Stable free model
    Provider.Perplexity,    # Lightweight model
    Provider.Bing,          # Reliable fallback
]

# ---------- AI GENERATION ----------
def generate_humanized_text(input_text):
    prompt = f"""
    Rewrite the following text to sound more natural, fluent, and human.
    Keep the meaning the same but make it conversational.

    Text:
    {input_text}
    """

    for provider in providers:
        try:
            response = ChatCompletion.create(
                model="gpt-4o-mini",
                provider=provider,
                messages=[{"role": "user", "content": prompt}],
            )
            clean_output = extract_text(response)

            # Ignore blank or login messages
            if clean_output and "login" not in clean_output.lower() and len(clean_output.split()) > 3:
                st.info(f"✅ Response from: {provider.__name__}")
                return clean_output
            else:
                st.warning(f"⚠️ {provider.__name__} returned invalid output.")
        except Exception as e:
            st.warning(f"⚠️ {provider.__name__} failed: {e}")
            continue

    return "❌ All free providers failed. Please try again later."


# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Text Humanizer (Free)", page_icon="🧠", layout="centered")
st.title("🧠 Free AI Text Humanizer")
st.write("Paste text below to get a smoother, more natural version — no API key needed!")

input_text = st.text_area("✍️ Enter your text:", height=200, placeholder="Paste your text here...")

if st.button("✨ Humanize Text"):
    if input_text.strip():
        with st.spinner("Rewriting your text..."):
            output = generate_humanized_text(input_text)
        st.subheader("✅ Humanized Output:")
        st.text_area("🔹 Edited Text:", output, height=200)
    else:
        st.warning("Please enter some text first.")

st.caption("Powered by GPT4Free • No API key • Fully free ⚙️")
