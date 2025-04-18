
import sys
import os
# Add the *parent directory* of `common` to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))

# Add to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

"""This file serves as the main entry point for the application.

It initializes the A2A server, defines the agent's capabilities,
and starts the server to handle incoming requests.
"""

import click
from common.server import A2AServer, InMemoryTaskManager
from common.types import AgentCapabilities, AgentCard, AgentSkill, MissingAPIKeyError
from typing import Union, AsyncIterable, List
from common.types import (
    JSONRPCResponse,
    TaskIdParams,
    TaskQueryParams,
    GetTaskRequest,
    TaskNotFoundError,
    SendTaskRequest,
    CancelTaskRequest,
    TaskNotCancelableError,
    SetTaskPushNotificationRequest,
    GetTaskPushNotificationRequest,
    GetTaskResponse,
    CancelTaskResponse,
    SendTaskResponse,
    SetTaskPushNotificationResponse,
    GetTaskPushNotificationResponse,
    PushNotificationNotSupportedError,
    TaskSendParams,
    TaskStatus,
    TaskState,
    TaskResubscriptionRequest,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    Artifact,
    PushNotificationConfig,
    TaskStatusUpdateEvent,
    JSONRPCError,
    TaskPushNotificationConfig,
    InternalError,
)
import logging
import os
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewTask(InMemoryTaskManager):
    """A simple task manager that handles incoming tasks."""

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """Handle a new task request."""
        # Here you would implement the logic to process the task
        # For this example, we just log the task and return a dummy response
        logger.info(f"Received task: {request}")
        return SendTaskResponse(id=request.id, status="completed")

    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> Union[AsyncIterable[SendTaskStreamingResponse], JSONRPCResponse]:
        """Handle subscription to task updates."""
        pass


@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=8000)
def main(host, port):
    """Entry point for the A2A sample."""
    try:
        capabilities = AgentCapabilities(streaming=False)
        skill = AgentSkill(
            id="image_generator",
            name="Image Generator",
            description=(
                "Generate stunning, high-quality images on demand and leverage"
                " powerful editing capabilities to modify, enhance, or completely"
                " transform visuals."
            ),
            tags=["generate image", "edit image"],
            examples=["Generate a photorealistic image of raspberry lemonade"],
        )

        agent_card = AgentCard(
            name="EchoAgent",
            description="An agent that echoes back the user's message.",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            capabilities=capabilities,
            skills=[skill],
        )

        server = A2AServer(
            agent_card=agent_card,
            task_manager=NewTask,
            host=host,
            port=port,
        )

        # add the task handler to the server
        server.app.add_route(
            "/tasks/send", handle_task, methods=["POST"]
        )

        logger.info(f"Starting server on {host}:{port}")
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)

# Handle incoming task requests at the A2A endpoint.
async def handle_task(request: Request):
    """Endpoint for A2A clients to send a new task (with an initial user message)."""
    task_request = await request.get_json()  # parse incoming JSON request
    # Extract the task ID and the user's message text from the request.
    task_id = task_request.get("id")
    user_message = ""
    try:
        # According to A2A spec, the user message is in task_request["message"]["parts"][0]["text"]
        user_message = task_request["message"]["parts"][0]["text"]
    except Exception as e:
        return JSONResponse(content={"error": "Invalid request format"}, status_code=400)
 
    # For this simple agent, the "processing" is just echoing the message back.
    agent_reply_text = f"Hello! You said: '{user_message}'"
 
    # Formulate the response in A2A Task format.
    # We'll return a Task object with the final state = 'completed' and the agent's message.
    response_task = {
        "id": task_id,
        "status": {"state": "completed"},
        "messages": [
            task_request.get("message", {}),             # include the original user message in history
            {
                "role": "agent",                        # the agent's reply
                "parts": [{"text": agent_reply_text}]   # agent's message content as a TextPart
            }
        ]
        # We could also include an "artifacts" field if the agent returned files or other data.
    }
    return JSONResponse(response_task)


if __name__ == "__main__":
  main()
