import json
import re
import os
import datetime
import subprocess
from groq import Groq

API_KEY = "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"
MODEL = "llama-3.1-8b-instant"
MEMORY_FILE = "memory.json"

client = Groq(api_key=API_KEY)

def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"profile": {}}

def save_memory(mem):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2, ensure_ascii=False)

memory = load_memory()

def handle_pc_commands(user):
    text = user.lower()

    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Abhi time hai {now}"

    if "date" in text:
        today = datetime.date.today().strftime("%d %B %Y")
        return f"Aaj ki date hai {today}"

    return None

def system_prompt():
    return f"""
You are a smart personal AI.
Reply short and correct.
Memory:
{memory}
"""

def get_ai_reply(user):
    pc = handle_pc_commands(user)
    if pc:
        return pc

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content