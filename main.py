import json
import re
import os
import datetime
import subprocess

import speech_recognition as sr
import pyttsx3
from groq import Groq

# ================= CONFIG =================
API_KEY = "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"
MODEL = "llama-3.1-8b-instant"
MEMORY_FILE = "memory.json"

client = Groq(api_key=API_KEY)

# ================= VOICE SETUP =================
voice_mode = False

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Sun raha hoon...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="hi-IN")
        print("You (voice):", text)
        return text
    except:
        return ""

# ================= MEMORY =================
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

# ================= MEMORY EXTRACTION =================
def extract_memory(user):
    text = user.lower().strip()

    if "?" in text:
        return

    # Name
    m = re.match(r"(mera|my)\s+(naam|name)\s+(.+)\s+hai$", text)
    if m:
        memory["profile"]["name"] = m.group(3).title()
        save_memory(memory)
        return

    # City
    if "me rehta" in text or "i live in" in text:
        words = text.split()
        memory["profile"]["city"] = words[-1].title()
        save_memory(memory)
        return

    # Likes
    if "mujhe pasand" in text or "i like" in text:
        memory["profile"]["likes"] = user
        save_memory(memory)
        return

# ================= PC COMMANDS =================
def handle_pc_commands(user):
    text = user.lower()

    if "open chrome" in text or "chrome kholo" in text:
        os.startfile("chrome")
        return "Chrome open kar diya"

    if "open notepad" in text or "notepad kholo" in text:
        subprocess.Popen(["notepad.exe"])
        return "Notepad open ho gaya"

    if "open calculator" in text or "calculator kholo" in text:
        subprocess.Popen(["calc.exe"])
        return "Calculator open ho gaya"

    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Abhi time hai {now}"

    if "date" in text:
        today = datetime.date.today().strftime("%d %B %Y")
        return f"Aaj ki date hai {today}"

    if "shutdown" in text:
        return "⚠️ Confirm karne ke liye likho: confirm shutdown"

    if "confirm shutdown" in text:
        os.system("shutdown /s /t 5")
        return "PC shutdown ho raha hai"

    return None

# ================= DIRECT QUESTIONS =================
def handle_direct_questions(user):
    text = user.lower()
    profile = memory.get("profile", {})

    if "mera name kya hai" in text or "my name" in text:
        return profile.get("name", "Aapne abhi apna naam nahi bataya")

    if "mai kaha rehta" in text:
        return profile.get("city", "Aapne abhi city nahi batayi")

    if "mujhe kya pasand" in text:
        return profile.get("likes", "Aapne abhi pasand nahi batayi")

    return None

# ================= SYSTEM PROMPT =================
def system_prompt():
    return f"""
You are a calm, intelligent personal AI.
Rules:
- Never invent information.
- Use memory only if it exists.
- Reply in user's language.
- Short and clear answers only.

Memory:
{memory}
"""

# ================= MAIN LOOP =================
print("🤖 JARVIS-STYLE AI READY (CHAT + VOICE + MEMORY)")
print("👉 'voice mode on' / 'voice mode off'")
print("👉 exit likho band karne ke liye\n")

while True:
    if voice_mode:
        user = listen()
        if not user:
            continue
    else:
        user = input("You: ").strip()

    if user.lower() == "exit":
        print("AI: Bye 👋")
        break

    if user.lower() == "voice mode on":
        voice_mode = True
        print("AI: 🎤 Voice mode ON")
        speak("Voice mode on")
        continue

    if user.lower() == "voice mode off":
        voice_mode = False
        print("AI: ⌨️ Chat mode ON")
        continue

    pc = handle_pc_commands(user)
    if pc:
        print("AI:", pc)
        if voice_mode:
            speak(pc)
        continue

    direct = handle_direct_questions(user)
    if direct:
        print("AI:", direct)
        if voice_mode:
            speak(direct)
        continue

    extract_memory(user)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user}
        ],
        temperature=0.3
    )

    reply = response.choices[0].message.content
    print("AI:", reply)

    if voice_mode:
        speak(reply)
