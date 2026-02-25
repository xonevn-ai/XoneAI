from xoneaiagents import Agent, MCP

whatsapp_agent = Agent(
    instructions="Whatsapp Agent",
    llm="groq/llama-3.2-90b-vision-preview",
    tools=MCP("python /Users/xonevn/whatsapp-mcp/whatsapp-mcp-server/main.py")
)

whatsapp_agent.start("Send Hello to Daniel Do")