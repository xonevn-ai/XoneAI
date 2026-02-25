from xoneaiagents import Agent, MCP

stock_agent = Agent(
    instructions="""You are a Stock Price Assistant.""",
    llm="ollama/llama3.2",
    tools=MCP("/Users/xonevn/miniconda3/envs/mcp/bin/python /Users/xonevn/stockprice/app.py")
)

stock_agent.start("What is the Stock Price of Apple?")