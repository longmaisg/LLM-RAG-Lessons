import openai
import os

# Make sure the API key is set either via environment variable or directly
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use environment variable method

system_content = "you are a helpful assistant"
# messages = [{"role": "system", "content": system_content}]
messages = []

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
    
def generate_message(prompt=str, role="user") -> list:
    global messages
    # Creating a message as required by the API
    if (role == "user"):
        messages.append({"role": "user", "content": prompt})
    elif (role == "assistant"):
        messages.append({"role": "assistant", "content": prompt})
    else:
        print("Invalid role specified. Use 'user' or 'assistant'.")

# Example usage
user_prompt = "one plus one is how much?"
print("\nuser: ", user_prompt)
generate_message(user_prompt, "user")
response = get_chat_completion(messages)
print("\nassistant: ", response)
generate_message(response, "assistant")

user_prompt = "my wife says one plus one is three, is she right?"
print("\nuser: ", user_prompt)
generate_message(user_prompt, "user")
response = get_chat_completion(messages)
print("\nassistant: ", response)
generate_message(response, "assistant")