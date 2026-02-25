from xoneaiagents import Agent, MCP

agent = Agent(
    instructions="""You are a helpful assistant that can check stock prices and perform other tasks.
    Use the available tools when relevant to answer user questions.""",
    llm="gpt-4o-mini",
    tools = MCP("/Users/xonevn/miniconda3/envs/mcp/bin/python /Users/xonevn/stockprice/app.py")
)

# NOTE: Python Path replace with yours: /Users/xonevn/miniconda3/envs/mcp/bin/python
# NOTE: app.py file path, replace it with yours: /Users/xonevn/stockprice/app.py

agent.start("What is the stock price of Tesla?")