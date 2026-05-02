import json, os, webbrowser, pyaudio, pyttsx3, requests
from vosk import KaldiRecognizer, Model

MODEL_PATH = "lab10/vosk-model-small-en-us-0.15"
API = "https://api.dictionaryapi.dev/api/v2/entries/en/"

model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()
mic = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

def speak(text):
    print(f"Bot: {text}")
    mic.stop_stream() 
    tts = pyttsx3.init()
    tts.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    tts.say(text)
    tts.runAndWait()
    
    mic.start_stream()

mic.start_stream()
speak("Yo, I'm online. Say find, meaning, link, save, or exit.")

current_word = ""
data = {}

while True:
    wave = mic.read(4000, exception_on_overflow=False)
    if not rec.AcceptWaveform(wave):
        continue

    cmd = json.loads(rec.Result()).get("text", "").strip()
    if not cmd:
        continue
    
    print(f"You: {cmd}")

    if cmd.startswith("find "):
        current_word = cmd[5:]
        try:
            res = requests.get(API + current_word)
            res.raise_for_status()
            data = res.json()[0]
            speak(f"Found {current_word}.")
        except Exception:
            speak("Oops, request failed or word doesn't exist.")
            current_word, data = "", {}

    elif cmd == "meaning" and data:
        try:
            speak(data["meanings"][0]["definitions"][0]["definition"])
        except (KeyError, IndexError):
            speak("No meaning found for this one.")

    elif cmd == "link" and current_word:
        webbrowser.open(f"https://dictionaryapi.dev/?search={current_word}")
        speak("Opening your browser.")

    elif cmd == "save" and current_word:
        with open("lab10/saved_words.txt", "a", encoding="utf-8") as f:
            f.write(current_word + "\n")
        speak("Saved it to your file.")

    elif cmd in ["exit", "quit", "stop"]:
        speak("Cya")
        break

    else:
        print("Say what? Unknown command or no word selected yet.")

mic.stop_stream()
mic.close()
audio.terminate()