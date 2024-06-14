# groq_module.py
import groq

# Initialize Groq client once
groq_client = groq.Groq()

# System prompt for the assistant
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant. I am talking to you with STT and listening your response with TTS. Respond with relevant answers for my queries. Give short answers unless I require explanations or ask for long answers. Don't repeat unless I ask for it. If you receive nothing as an input then I am thinking only, in that case respond nothing or if you can't do that respond with three dots (...) only so that the TTS won't disturb me"
}

# Initialize the chat history
chat_history = [system_prompt]

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

if __name__ == "__main__":
    import sys
    user_query = sys.argv[1] if len(sys.argv) > 1 else "Hello"
    print(ask_groq(user_query))
