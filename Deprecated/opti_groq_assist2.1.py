import whisper
import pyaudio
import wave
import pyttsx3
import groq
import os
import queue
import threading
import time
import signal

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialize the TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Load the Whisper model once
whisper_model = whisper.load_model("base.en")

# Initialize Groq client once
groq_client = groq.Groq()

# Queue for buffering audio chunks
audio_queue = queue.Queue()

# System prompt for the assistant
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant. I am talking to you with STT and listening your response with TTS. Respond with relevant answers for my queries. Give short answers unless I require explanations or ask for long answers. Don't repeat unless I ask for it. If you recieve nothing as an input then I am thinking only, in that case respond nothing or if you can't do that respond with three dots (...) only so that the tts won't disturb me"
}

# Initialize the chat history
chat_history = [system_prompt]

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    global running
    running = False
    print("Exiting gracefully...")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to record audio from the microphone and put chunks into the queue
def record_audio(record_seconds):
    audio = pyaudio.PyAudio()
    
    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording...")

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        audio_queue.put(data)  # Put each chunk into the queue

    print("Finished recording.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Indicate that recording is done
    audio_queue.put(None)

# Function to transcribe audio from the queue using Whisper
def transcribe_audio():
    frames = []

    while True:
        chunk = audio_queue.get()
        if chunk is None:  # End of recording
            break
        frames.append(chunk)

    # Save the recorded audio to a file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # Transcribe the audio
    result = whisper_model.transcribe(WAVE_OUTPUT_FILENAME)
    return result["text"]

# Function to get response from Groq model
def ask_groq(query):
    chat_history.append({"role": "user", "content": query})
    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=1024,
        temperature=1.2
    )
    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

def main_loop():
    global running
    while running:
        # Start recording in a separate thread
        record_thread = threading.Thread(target=record_audio, args=(RECORD_SECONDS,))
        record_thread.start()
        record_thread.join()  # Wait for recording to finish

        # Transcribe and get the assistant's response
        transcribed_text = transcribe_audio()
        print(f"Transcribed Text: {transcribed_text}")
        assistant_response = ask_groq(transcribed_text)
        print(f"Assistant Response: {assistant_response}")

        # Speak the assistant's response
        engine.say(assistant_response)
        engine.runAndWait()

        # Wait a moment before recording the next query
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
