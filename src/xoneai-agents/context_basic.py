from xoneaiagents import ContextAgent

agent = ContextAgent(llm="gpt-4o-mini", auto_analyze=False)

agent.start("https://github.com/xonevn-ai/XoneAI/ Need to add Authentication")