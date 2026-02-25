from xoneaiagents import Agent, Tools
from xoneaiagents.tools import duckduckgo

agent = Agent(instructions="You are a Research Agent", tools=[duckduckgo])
agent.start("Research about AI 2024")