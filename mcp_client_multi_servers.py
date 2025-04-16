from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import openai
import os
import json

async def run():
    async with MultiServerMCPClient(
        {
            "mcp_server": {
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio",
            },
            "mcp_server2": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        tools = client.get_tools()  # -> cannot know which server the tool is from

        functions = []
        for tool in tools:
            function = {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": tool.args_schema.get("type"),
                    "properties": tool.args_schema.get("properties"),
                    "required": tool.args_schema.get("required"),
                },
            }
            functions.append(function)

        # Use ChatGPT to get the best tool
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Or use environment variable method
        messages = [{"role": "user", "content": "choose the best tool from user's question. Return the tool name only."}]
        messages.append({"role": "user", "content": "1 times 3 is how much?"})
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
            result = await client.sessions.get("mcp_server").call_tool(name=name, arguments=json.loads(arguments))
            print(f"result: {result}")
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())