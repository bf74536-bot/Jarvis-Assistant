"""
JARVIS - a simple voice assistant
-----------------------------------
How it works (the loop):
  1. Listen to your microphone
  2. Convert your speech to text
  3. Send that text to Claude (the "brain") to get a smart reply
  4. Speak the reply back out loud
  5. Repeat

SETUP (do this once):
  1. Install Python 3.9+ from python.org if you don't have it.
  2. Open a terminal in this folder and run:
        pip install SpeechRecognition pyttsx3 anthropic pyaudio
     (If pyaudio fails to install on Mac, run: brew install portaudio  then try again)
     (If pyaudio fails on Windows, run: pip install pipwin  then  pipwin install pyaudio)
  3. Get an API key from https://console.anthropic.com/ and either:
       - set it as an environment variable called ANTHROPIC_API_KEY, OR
       - paste it directly into API_KEY below (only for local testing, don't share this file with the key in it!)
  4. Run:  python jarvis.py
  5. Wait for "Listening..." then talk. Say "goodbye" to exit.
"""

import os
import speech_recognition as sr
import pyttsx3
from anthropic import Anthropic

# ------------------- SETTINGS -------------------
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")  # or paste your key here as a string
WAKE_EXIT_WORDS = ["goodbye", "exit", "quit", "stop listening"]
ASSISTANT_NAME = "Jarvis"
# --------------------------------------------------

# Set up the "mouth" (text-to-speech engine)
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # speaking speed

def speak(text: str):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

# Set up the "ears" (speech recognition)
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen() -> str:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        return ""  # couldn't understand
    except sr.RequestError:
        speak("I'm having trouble reaching the speech recognition service.")
        return ""

# Set up the "brain" (Claude)
client = Anthropic(api_key=API_KEY) if API_KEY else Anthropic()  # falls back to env var automatically

conversation_history = []

def ask_brain(user_text: str) -> str:
    conversation_history.append({"role": "user", "content": user_text})
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=(
            f"You are {ASSISTANT_NAME}, a helpful, witty voice assistant in the style of "
            "Tony Stark's AI. Keep replies SHORT (1-3 sentences) since they'll be spoken aloud."
        ),
        messages=conversation_history,
    )
    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

def main():
    speak(f"{ASSISTANT_NAME} online. How can I help?")
    while True:
        user_text = listen()
        if not user_text:
            continue  # didn't catch anything, just listen again

        if any(word in user_text.lower() for word in WAKE_EXIT_WORDS):
            speak("Goodbye!")
            break

        reply = ask_brain(user_text)
        speak(reply)

if __name__ == "__main__":
    main()
