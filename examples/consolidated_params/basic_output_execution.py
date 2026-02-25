"""Basic output and execution example."""
from xoneaiagents import Agent

# Simple preset usage
agent = Agent(
    instructions="You are a helpful assistant.",
    output="verbose",  # Preset: verbose output
    execution="thorough",  # Preset: thorough execution
)

if __name__ == "__main__":
    response = agent.chat("What is 2+2?")
    print(response)
