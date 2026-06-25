from mcp.server.fastmcp import FastMCP
from services.session_store import SessionStore
from tools.register import register_tools
from prompts.register import register_prompts

def create_server() -> FastMCP:
    mcp = FastMCP("Anonymizer MCP")
    store = SessionStore()

    register_tools(mcp, store)
    register_prompts(mcp)

    return mcp