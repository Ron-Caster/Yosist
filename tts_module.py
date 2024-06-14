# tts_module.py
import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    import sys
    text_to_speak = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    speak_text(text_to_speak)
