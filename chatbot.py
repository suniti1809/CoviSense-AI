import os
import requests
import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()

def local_bot(user_input, context):
    text = user_input.lower()

    if "cases" in text:
        return f"📊 Total cases are {context['cases']}."
    elif "growth" in text:
        return f"📈 Growth rate is {context['growth']}%."
    elif "trend" in text:
        return f"📉 Trend is {context['trend']}."
    elif "risk" in text:
        return f"⚠ Risk level is {context['risk']}."
    elif "peak" in text:
        return f"🔥 Peak: {context['peak']}."
    elif "hello" in text or "hi" in text:
        return "👋 Hello! Ask about cases, growth, trend, risk."
    else:
        return "🤖 Ask about cases, growth, prediction, or risk."


def ask_gpt(user_input, context):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return local_bot(user_input, context)

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = f"""
    Epidemic Data:
    Cases: {context['cases']}
    Growth: {context['growth']}%
    Peak: {context['peak']}
    Trend: {context['trend']}
    Risk: {context['risk']}
    """

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            return local_bot(user_input, context)

        return res.json()["choices"][0]["message"]["content"]

    except:
        return local_bot(user_input, context)


def typewriter(text):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(output)
        time.sleep(0.01)