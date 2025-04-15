from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

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

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())