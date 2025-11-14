import speech_recognition as sr
import pyttsx3
from datetime import datetime
import google.generativeai as genai

# ---- GEMINI ----
GEMINI_API_KEY = "AIzaSyBQoSL4LSylbHupDpGrDpg1bk8uiv8VihU"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def ai_chat(prompt):
    response = model.generate_content(prompt)
    return response.text

engine = pyttsx3.init()

def speak(text):
    engine.say(text or "Text is not Given")
    # engine.runAndWait()

def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"The current time is {current_time}."

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except:
            return None


print("Hello! I’m your AI voice assistant.")
speak("Hello! I’m your AI voice assistant.")

while True:
    command = listen()

    if command:
        
        cmd = command.lower()

        if "hello ai" in cmd:
            engine.say("Hello Bewin Immanuel!")

        elif "time" in cmd:
            t = get_time()
            engine.say(t)
            print(t)

        elif "goodbye" in cmd or "exit" in cmd:
            speak("Goodbye! Have a great day!")
            break

        else:
            reply = ai_chat(command)
            engine.say(reply)
            print("AI:", reply)

    else:
        engine.say("I didn't hear anything, please repeat.")
