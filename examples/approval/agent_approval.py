"""
Agent Approval Example
======================
Uses an AI agent as an automated reviewer to approve/deny tool calls.

Requires:
    pip install xoneaiagents
    export OPENAI_API_KEY=sk-...
"""

from xoneaiagents import Agent
from xoneaiagents.approval import AgentApproval
from xoneaiagents.tools.shell_tools import execute_command

reviewer = AgentApproval(
    instructions="Only approve read-only commands like 'ls' or 'cat'. Deny destructive commands.",
)

agent = Agent(
    name="DevOps",
    instructions="You are a DevOps assistant. Use shell tools when asked.",
    tools=[execute_command],
    approval=reviewer,
)

agent.start("List files in the current directory")
