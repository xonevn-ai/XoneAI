# pip install xoneaiagents
# export OPENAI_BASE_URL=http://localhost:11434/v1
# ollama pull deepseek-r1

from xoneaiagents import Agent

agent = Agent(instructions="You are helpful Assisant", llm="deepseek-r1")

agent.start("Why sky is Blue?")