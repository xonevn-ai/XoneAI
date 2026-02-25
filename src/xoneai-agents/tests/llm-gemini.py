from xoneaiagents import Agent
from xoneaiagents.tools import internet_search

agent = Agent(
    instructions="You are a helpful assistant",
    tools=[internet_search],
    llm="gemini/gemini-1.5-flash-8b"
)

agent.start("What is Xone AI?")