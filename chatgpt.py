import openai
import os
from conversation import Conversation

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use environment variable method

def get_chat_completion(messages=list, model="gpt-4o-mini") -> str:
    try:
        # Calling the ChatCompletion API
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        # Returning the extracted response
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

# Example usage
conversation = Conversation()
user_prompt = "one plus one is how much?"
print("\nuser: ", user_prompt)
conversation.add_message(user_prompt, "user")
response = get_chat_completion(conversation.messages)
print("\nassistant: ", response)
conversation.add_message(response, "assistant")

user_prompt = "my wife says one plus one is three, is she right?"
print("\nuser: ", user_prompt)
conversation.add_message(user_prompt, "user")
response = get_chat_completion(conversation.messages)
print("\nassistant: ", response)
conversation.add_message(response, "assistant")