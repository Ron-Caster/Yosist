# whisper_module.py
import pyaudio
import wave
import whisper
import keyboard  # pip install keyboard
import pyautogui  # pip install pyautogui

# Constants for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

# Load the Whisper model once
whisper_model = whisper.load_model("base.en")  # Use tiny.en for smallest English Model, base.en, small.en are the other ones.

# Function to handle transcription
def transcribe_audio(filename):
    result = whisper_model.transcribe(filename)
    return result["text"]

# Function to record audio
def record_audio():
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording... Press Caps Lock to stop and transcribe.")

    frames = []
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed('capslock'):
            break

    print("Finished recording.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return WAVE_OUTPUT_FILENAME

def record_and_transcribe():
    audio_filename = record_audio()
    return transcribe_audio(audio_filename)

if __name__ == "__main__":
    print(record_and_transcribe())
