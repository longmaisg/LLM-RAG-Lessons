from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
import asyncio
import chatgpt
from chatgpt import Conversation

# This code snippet defines a simple workflow using the LlamaIndex library.

class MyWorkflow(Workflow):
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        # do something here
        return StopEvent(result="Hello, world!")


async def main():
    w = MyWorkflow(timeout=10, verbose=False)
    result = await w.run()
    print(result)


if __name__ == "__main__":
    # set up ChatGPT
    chatgpt.setup_chatgpt()


    # start a new conversation
    conversation = Conversation()

    asyncio.run(main())