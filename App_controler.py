import os
import subprocess
import webbrowser

def open_app(user_text: str):
    text = user_text.lower()

    if "open chrome" in text or "chrome kholo" in text:
        try:
            os.startfile("chrome")
        except:
            webbrowser.open("https://www.google.com")
        return "Chrome open kar diya 🌐"

    if "open youtube" in text or "youtube kholo" in text:
        webbrowser.open("https://www.youtube.com")
        return "YouTube open kar diya ▶️"

    if "open google" in text or "google kholo" in text:
        webbrowser.open("https://www.google.com")
        return "Google open ho gaya 🔍"

    if "open notepad" in text or "notepad kholo" in text:
        subprocess.Popen(["notepad.exe"])
        return "Notepad open ho gaya ✍️"

    if "open calculator" in text or "calculator kholo" in text:
        subprocess.Popen(["calc.exe"])
        return "Calculator open ho gaya 🧮"

    return None