import requests
import uuid
 
# 1. Discover the agent by fetching its Agent Card
AGENT_BASE_URL = "http://localhost:8000"
agent_card_url = f"{AGENT_BASE_URL}/.well-known/agent.json"
response = requests.get(agent_card_url)
if response.status_code != 200:
    raise RuntimeError(f"Failed to get agent card: {response.status_code}")
agent_card = response.json()
print("Discovered Agent:", agent_card["name"], "-", agent_card.get("description", ""))
 
# 2. Prepare a task request for the agent
task_id = str(uuid.uuid4())  # generate a random unique task ID
user_text = "What is the meaning of life?"
task_payload = {
    "id": task_id,
    "message": {
        "role": "user",
        "parts": [
            {"text": user_text}
        ]
    }
}
print(f"Sending task {task_id} to agent with message: '{user_text}'")
 
# 3. Send the task to the agent's tasks/send endpoint
tasks_send_url = f"{AGENT_BASE_URL}/tasks/send"
result = requests.post(tasks_send_url, json=task_payload)
if result.status_code != 200:
    raise RuntimeError(f"Task request failed: {result.status_code}, {result.text}")
task_response = result.json()
 
# 4. Process the agent's response
# The response should contain the task ID, status, and the messages (including the agent's reply).
if task_response.get("status", {}).get("state") == "completed":
    # The last message in the list should be the agent's answer (since our agent included history in messages).
    messages = task_response.get("messages", [])
    if messages:
        agent_message = messages[-1]  # last message (from agent)
        agent_reply_text = ""
        # Extract text from the agent's message parts
        for part in agent_message.get("parts", []):
            if "text" in part:
                agent_reply_text += part["text"]
        print("Agent's reply:", agent_reply_text)
    else:
        print("No messages in response!")
else:
    print("Task did not complete. Status:", task_response.get("status"))