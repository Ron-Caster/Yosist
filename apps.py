import os
import json
import subprocess
from groq import Groq

# Set up the Groq API client
client = Groq()
MODEL = 'llama3-70b-8192'

# Define the function to open an application
def open_app(app_name):
    app_map = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",  # Full path to OBS Studio executable
        "geforce experience": r"C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience\NVIDIA GeForce Experience.exe",
        "vs code": r"C:\Users\Hari Prezadu\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "vlc": "vlc.exe",
        "windows media player": "wmplayer.exe",
        "notepad": "notepad.exe",
        "localsend": r"C:\Program Files\LocalSend\localsend_app.exe",
        "proton vpn": r"C:\Program Files\Proton\VPN\v3.2.11\ProtonVPN.exe",
        "excel": "EXCEL.EXE",
        "outlook": "OUTLOOK.EXE",
        "word": "WINWORD.EXE",
        "powerpoint": "POWERPNT.EXE",
        "onenote": "ONENOTE.EXE",
        "access": "MSACCESS.EXE",
        "publisher": "MSPUB.EXE",
        "telegram": r"C:\Program Files\WindowsApps\TelegramMessengerLLP.TelegramDesktop_5.0.1.0_x64__t4vj0pshhgkwm\Telegram.exe",
        "whatsapp": r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2423.7.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
        "obsidian": r"C:\Users\Hari Prezadu\AppData\Local\Programs\obsidian\Obsidian.exe",
        "spotify": "Spotify.exe"
        # Add more apps as needed
    }
    
    if app_name.lower() in app_map:
        executable_path = app_map[app_name.lower()]
        try:
            if app_name.lower() == "obs":
                subprocess.Popen([executable_path], cwd=os.path.dirname(executable_path))
            elif app_name.lower() == "geforce experience":
                subprocess.Popen([executable_path], cwd=os.path.dirname(executable_path))
            else:
                os.startfile(executable_path)
            return f"Opened {app_name} successfully!"
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    else:
        return f"Unsupported app: {app_name}"

# Define the conversation function
def run_conversation():
    conversation_history = []
    
    while True:
        user_prompt = input("Please enter your prompt: ")
        
        conversation_history.append({"role": "user", "content": user_prompt})
        
        messages = conversation_history.copy()
        
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "open_app",
                    "description": "Open an application",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {
                                "type": "string",
                                "description": "The name of the application to open",
                            }
                        },
                        "required": ["app_name"],
                    },
                },
            }
        ]
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096
        )

        # Print the response to debug
        print("Response:", response)

        # Check if the tool_calls attribute exists
        if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)  # Parse the arguments string as JSON
            app_name = arguments["app_name"]
            result = open_app(app_name)
            print(result)
            conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
        else:
            print("No tool call was made in the response.")
            conversation_history.append({"role": "assistant", "content": "No tool call was made in the response."})

if __name__ == "__main__":
    run_conversation()
