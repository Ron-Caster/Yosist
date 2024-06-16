from groq import Groq
import os
import json

client = Groq()
MODEL = 'llama3-70b-8192'


# Example dummy function hard coded to return the score of an NBA game
def get_pyfile(file_name):
    """Select the correct python file as required"""
    if "open" in file_name.lower():
        return json.dumps({"purpose": "Open Apps", "py_file": 'apps.py'})
    else:
        return json.dumps({"file_name": file_name, "py_file": "groq_module.py"})

def run_conversation(user_prompt):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": "You are a function calling LLM that uses the data extracted from the get_pyfile function to answer questions around which python file to choose as per the query. If the query is about to open apps like chrome, firefox or something - give apps.py as output else give groq_module.py. Include only py_file in your response."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_pyfile",
                "description": "Select correct python file according to purpose of the query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the python file (e.g. 'apps.py', 'groq_module.py')",
                        }
                    },
                    "required": ["file_name"],
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

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_pyfile": get_pyfile,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                file_name=function_args.get("file_name")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content

def get_pyfile_name(user_prompt):
    response_content = run_conversation(user_prompt)
    response_json = json.loads(response_content)
    return response_json['py_file']
