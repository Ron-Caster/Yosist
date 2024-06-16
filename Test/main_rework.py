# main.py
import whisper_module
import groq_module
import tts_module
import intent_module
import apps

def main_loop():
    while True:
        # Record and transcribe audio
        transcribed_text = whisper_module.record_and_transcribe()
        print(f"Transcribed Text: {transcribed_text}")

        # Get users's intent
        file_name = intent_module.ask_groq(transcribed_text) #implement correct function
        print(f"File Name: {file_name}")

        # Choose which to run
        if (file_name == "apps.py"):
            apps.user_prompt(transcribed_text)
            break #(to while??) I want loop to continue

        else:
            # Get assistant's response
            assistant_response = groq_module.ask_groq(transcribed_text)
            print(f"Assistant Response: {assistant_response}")

        # Speak the assistant's response
        tts_module.speak_text(assistant_response)

if __name__ == "__main__":
    main_loop()
