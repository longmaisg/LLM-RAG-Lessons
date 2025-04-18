from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Your existing FastAPI application
app = FastAPI()

# Define your endpoints as you normally would

async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

# Add the MCP server to your FastAPI app
mcp = FastApiMCP(
    app,  
    name="My API MCP",  # Name for your MCP server
    description="MCP server for my API",  # Description
    base_url="http://localhost:8000"  # Where your API is running
)

# Mount the MCP server to your FastAPI app
mcp.mount()

# Add new endpoints after MCP server creation
@app.get("/hello/", operation_id="hello")
async def new_endpoint():
    return {"message": "Hello, world!"}


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)