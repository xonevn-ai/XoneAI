"""
HTTP Approval Example
=====================
Opens a local web dashboard for tool approvals.

Requires:
    pip install xoneaiagents xoneai[bot]
    export OPENAI_API_KEY=sk-...
"""

from xoneaiagents import Agent
from xoneaiagents.tools.shell_tools import execute_command
from xoneai.bots import HTTPApproval

agent = Agent(
    name="DevOps",
    instructions="You are a DevOps assistant. Use shell tools when asked.",
    tools=[execute_command],
    approval=HTTPApproval(),
)

agent.start("List files in the current directory")
