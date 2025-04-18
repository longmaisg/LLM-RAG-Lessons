from mcp.server.fastmcp import FastMCP  # The MCP server library

# Create an mcp server
mcp = FastMCP("mcp_server")

# Add a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """ Add two numbers together. """
    return a + b

# Add a data resource
@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """ Greet the user by name. """
    return f"Hello, {name}!"

# Add a prompt
@mcp.prompt()
def prompt(name: str) -> str:
    """ Prompt the user for their name. """
    return f"What is your name, {name}?"

if __name__ == "__main__":
    mcp.run(transport="stdio")

