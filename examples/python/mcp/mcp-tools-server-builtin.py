"""MCP Server with Built-in XoneAI Tools

Expose XoneAI's built-in tools as an MCP server.

Usage:
    # Set required API keys first
    export TAVILY_API_KEY=your_key
    
    python mcp-tools-server-builtin.py
"""

from xoneaiagents.mcp import launch_tools_mcp_server


if __name__ == "__main__":
    # Expose built-in XoneAI tools as MCP server
    # This allows external MCP clients to use these tools
    
    launch_tools_mcp_server(
        tool_names=[
            "tavily_search",      # Web search via Tavily
            "duckduckgo_search",  # Web search via DuckDuckGo
            # Add more built-in tools as needed
        ],
        name="xoneai-builtin-tools",
        transport="stdio"  # Use "sse" for web clients
    )
