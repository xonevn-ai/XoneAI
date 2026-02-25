from xoneaiagents import Agent, MCP

whatsapp_agent = Agent(
    instructions="Whatsapp Agent",
    llm="ollama/llama3.2",
    tools=MCP("python /Users/xonevn/whatsapp-mcp/whatsapp-mcp-server/main.py")
)

whatsapp_agent.start("Send Hello to Daniel Do. Use send_message tool, recipient and message are the required parameters.")