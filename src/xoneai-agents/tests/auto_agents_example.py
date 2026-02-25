from xoneaiagents import AutoAgents
from xoneaiagents.tools import duckduckgo

agents = AutoAgentTeam(
    instructions="Search for information about AI Agents",
    tools=[duckduckgo],
    process="sequential",
    verbose=True
)

agents.start()