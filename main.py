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

        # Get user's intent
        file_name = intent_module.run_conversation(transcribed_text)
        print(f"File Name: {file_name}")

        # Choose which to run
        if file_name == "apps.py":
            apps.run_conversation(transcribed_text)
            continue
        else:
            # Get assistant's response
            assistant_response = groq_module.ask_groq(transcribed_text)
            print(f"Assistant Response: {assistant_response}")

        # Check if a specific language is mentioned
        if "language" in transcribed_text.lower():
            language = transcribed_text.split("language")[-1].strip()
            if language.lower() == "english":
                # Perform actions for English language
                print("Performing actions for English language")
            else:
                # Perform actions for the specified language
                print(f"Performing actions for {language} language")
        else:
            # Default to English language
            print("Performing actions for English language")

        # Speak the assistant's response
        tts_module.speak_text(assistant_response)

if __name__ == "__main__":
    main_loop()