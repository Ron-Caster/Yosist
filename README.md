
# Voice Assistant

## IMPORTANT 
1) Get Groq API Key from [Groq Website](https://console.groq.com/keys)
2) Add Groq API Key to Environmental Variables: GROQ_API_KEY=YOUR_API_KEY_HERE
 
   ![image](https://github.com/Ron-Caster/Yosist/assets/56224323/7c56d271-a4c7-4a85-9d34-5056b2690433)


This project implements a voice assistant that uses speech-to-text (STT) for recognizing spoken queries, a large language model (LLM) for generating responses, and text-to-speech (TTS) for vocalizing the responses. The components are modularized into three separate scripts focusing on audio recording and transcription, querying a language model, and text-to-speech synthesis.

## Overview

- **Audio Recording and Transcription**: Records audio from the microphone and transcribes it using Whisper.
- **Querying Groq Model**: Sends the transcribed text to the Groq model to get a response.
- **Text-to-Speech**: Converts the text response from the model into speech using pyttsx3.

## Modules

1. `whisper_module.py`: Handles audio recording and transcription using Whisper.
2. `groq_module.py`: Manages querying the Groq model and chat history.
3. `tts_module.py`: Converts text responses into speech using pyttsx3.
4. `main.py`: Coordinates the other modules to create a seamless voice assistant experience.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages:
  - pyaudio
  - wave
  - pyttsx3
  - whisper
  - groq

Install the required packages using pip:
```sh
pip install pyaudio wave pyttsx3 whisper groq
```

### Running the Voice Assistant

Run the `main.py` script to start the voice assistant:
```sh
python main.py
```

## Usage

### Testing Individual Modules

You can test each module separately if needed.

- **Whisper Module**:
  ```sh
  python whisper_module.py
  ```
  
- **Groq Module**:
  ```sh
  python groq_module.py "What is the capital of France?"
  ```
  
- **TTS Module**:
  ```sh
  python tts_module.py "Hello, how can I assist you today?"
  ```

## Project Structure

```
main.py
├── whisper_module.py
├── groq_module.py
├── tts_module.py
├── intent_module.py
├── apps.py
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
