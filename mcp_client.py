from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import openai
import os
import json

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()

            # Get a prompt
            prompt = await session.get_prompt(
                "prompt", arguments={"name": "value"}
            )
            print(prompt)

            # List available tools
            tools = await session.list_tools()
            print(tools.tools[0])

            functions = []
            for tool in tools.tools:
                function = {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": tool.inputSchema.get("type"),
                        "properties": tool.inputSchema.get("properties"),
                        "required": tool.inputSchema.get("required"),
                    },
                }
                functions.append(function)

            # Use ChatGPT to get the best tool
            openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use environment variable method
            messages = [{"role": "user", "content": "choose the best tool from user's question. Return the tool name only."}]
            messages.append({"role": "user", "content": "1 plus 3 is how much?"})
            try:
                # Calling the ChatCompletion API
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    functions=functions,
                    function_call="auto",
                    temperature=0,
                )
                # Returning the extracted response
                name = response.choices[0].message.function_call.name
                arguments = response.choices[0].message.function_call.arguments
                print(f"response: name: {name} -- arguments: {arguments}")

                # Call a tool
                result = await session.call_tool(name=name, arguments=json.loads(arguments))
                print(result)
            except Exception as e:
                print(str(e))


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())