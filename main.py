# main.py
import whisper_module
import groq_module
import tts_module

def main_loop():
    while True:
        # Record and transcribe audio
        transcribed_text = whisper_module.record_and_transcribe()
        print(f"Transcribed Text: {transcribed_text}")

        # Get assistant's response
        assistant_response = groq_module.ask_groq(transcribed_text)
        print(f"Assistant Response: {assistant_response}")

        # Speak the assistant's response
        tts_module.speak_text(assistant_response)

if __name__ == "__main__":
    main_loop()
