import openai
import os
from conversation import Conversation

class Conversation:
    messages = []
    system_prompt_get_keywords = "A user want to find best fitted video to learn french. From the prompt, extract up to 5 keywords to search youtube meaningfully."
    system_prompt_rank_videos = "Given some videos with title + description + videoid, rank the best video based on the user prompt. Return only 1 videoid"

    def __init__(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_message(self, message, role="user"):
        if role not in ["user", "assistant"]:
            raise ValueError("Role must be either 'user' or 'assistant'")
        self.messages.append({"role": role, "content": message})

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
    
def setup_chatgpt():
    # Set up OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use environment variable method

# Example usage
if __name__ == "__main__":

    setup_chatgpt()

    # Example conversation
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