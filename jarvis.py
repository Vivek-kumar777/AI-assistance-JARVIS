import pyaudio
import webbrowser
import pygame
import speech_recognition as sr
import pyttsx3
import time
import re
from openai import OpenAI

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Replace with your actual key securely
)

# Initialize speech recognizer and TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_jarvis(question):
    completion = client.chat.completions.create(
        model="openrouter/sonoma-sky-alpha",
        messages=[
            {"role": "system", "content": "You are Jarvis, a helpful and witty AI assistant created by jarvis. Introduce yourself only when the user asks who you are or greets you."},
            {"role": "system", "content": "Answer all user questions with some interactive emoji's."},
            {"role": "user", "content": question}
        ],
        extra_headers={
            "HTTP-Referer": "https://code-with-jarvis.netlify.app",
            "X-Title": "code-with-jarvis"
        }
    )
    return completion.choices[0].message.content

# Main loop
if __name__ == "__main__":
    speak("initialising jarvis")
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for wake word...")
            audio = r.listen(source)

            try:
                word = r.recognize_google(audio, language="en-IN")
                if "jarvis" == word.lower():
                    print("jarvis activated..")
                    speak("yes sir.")

                    while True:
                        try:
                            with sr.Microphone() as source:
                                r.adjust_for_ambient_noise(source)
                                print("Listening for command...")
                                audio = r.listen(source)
                                command = r.recognize_google(audio, language="en-IN")
                            print("You said:", command)
                            speak(f"You said..{command}")

                            # Handle basic commands
                            if "open youtube" in command.lower():
                                webbrowser.open("https://www.youtube.com/?feature=ytca")
                            elif "open facebook" in command.lower():
                                webbrowser.open("https://www.facebook.com/")
                            elif "chat gpt" in command.lower():
                                webbrowser.open("https://chatgpt.com/overview")
                            elif "stop" in command.lower():
                                print("Thanks sir")
                                speak("Thanks sir")
                                break
                            else:
                                # Send question to Jarvis
                                response = ask_jarvis(command)
                                print("Jarvis:", response)
                                speak(response)

                        except Exception as e:
                            print("Couldn't understand:", e)
                            speak("Couldn't understand")
                            time.sleep(0.01)

            except sr.UnknownValueError:
                print("Sorry, could not understand.")
                speak("Sorry, I could not understand.")
            except sr.RequestError:
                print("Speech service is unavailable.")
                speak("Speech service is unavailable.")

        time.sleep(0.5)
