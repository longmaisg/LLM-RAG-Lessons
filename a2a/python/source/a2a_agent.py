import asyncio
import sys
import os
# Add the *parent directory* of `common` to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from common.client import A2AClient, A2ACardResolver
from common.types import TaskSendParams, Message, TextPart
import uuid
 
async def query_agent(agent_url, user_text):
    # Fetch agent card automatically
    card_resolver = A2ACardResolver(agent_url)
    agent_card = card_resolver.get_agent_card()
    print("Discovered Agent:", agent_card.name)

    # Create A2A client with the agent's card
    client = A2AClient(agent_card=agent_card)

    # Prepare Task parameters (using A2A type classes)
    payload = TaskSendParams(
        id=str(uuid.uuid4()),
        message=Message(role="user", parts=[TextPart(text=user_text)])
    )

    # Send the task and wait for completion
    # client.url = f"{agent_url}/tasks/send"
    result_task = await client.send_task(payload)  # send_task is an async method

    # Extract agent's reply from result_task
    if result_task.status.state.value == "completed":
        # The A2A Task object can be inspected for messages and artifacts
        for msg in result_task.messages:
            if msg.role == "agent":
                # Print text parts of agent's message
                print("Agent's reply:", " ".join(part.text for part in msg.parts if hasattr(part, "text")))


if __name__ == "__main__":
    # Example usage
    agent_url = "http://localhost:8000"  # URL of the A2A agent
    user_text = "What is the meaning of life?"
    asyncio.run(query_agent(agent_url, user_text))