class Conversation:
    messages = []
    system_prompt = "You are a helpful assistant. You answer will be short and no more than 20 words."

    def __init__(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def add_message(self, message, role="user"):
        if role not in ["user", "assistant"]:
            raise ValueError("Role must be either 'user' or 'assistant'")
        self.messages.append({"role": role, "content": message})