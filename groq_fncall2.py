#appends chat in each call for history

import os
import json
from groq import Groq

# Set up the Groq API client
client = Groq()
MODEL = 'llama3-70b-8192'

# Define the function to open an application
def open_app(app_name):
    app_map = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        # Add more apps as needed
    }
    
    if app_name in app_map:
        executable_name = app_map[app_name]
        try:
            os.startfile(executable_name)
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