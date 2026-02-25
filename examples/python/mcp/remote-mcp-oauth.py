"""
Remote MCP Server with OAuth Authentication Example

This example shows how to connect to a remote MCP server
that requires OAuth 2.1 authentication.

Prerequisites:
1. Configure the remote server in ~/.xone/config.yaml
2. Run: xoneai mcp auth <server-name>
"""

from xoneaiagents import Agent, MCP
from xoneaiagents.mcp import MCPAuthStorage

# Check if authenticated
storage = MCPAuthStorage()
entry = storage.get("my-remote-server")

if not entry or not entry.get("tokens"):
    print("Not authenticated. Run: xoneai mcp auth my-remote-server")
    exit(1)

# Create agent with remote MCP server
agent = Agent(
    name="Remote Assistant",
    instructions="You help with tasks using the remote MCP server.",
    llm="gpt-4o-mini",
    tools=MCP("https://mcp.example.com/mcp")
)

# Start the agent
agent.start("What tools are available?")
