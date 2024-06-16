
# Your Assistant - Yosist

This project implements an AI Voice Assistant to open Windows Applications and Utilizes Generative AI to Answer Queries (As of now)

## IMPORTANT 
1) Get Groq API Key from [Groq Website](https://console.groq.com/keys)
2) Add Groq API Key to Environmental Variables: GROQ_API_KEY=YOUR_API_KEY_HERE
 
   ![image](https://github.com/Ron-Caster/Yosist/assets/56224323/7c56d271-a4c7-4a85-9d34-5056b2690433)


## INSTALLATION
```sh
git clone https://github.com/Ron-Caster/Yosist.git
```
Install the required packages using pip:
```sh
pip install pyaudio wave pyttsx3 whisper groq
```

### Running the Voice Assistant

Run the `main.py` script to start the voice assistant:
```sh
python main.py
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
