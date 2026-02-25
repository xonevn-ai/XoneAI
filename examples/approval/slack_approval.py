"""
Slack Approval Example
======================
Routes tool approvals to a Slack channel.

Requires:
    pip install xoneaiagents xoneai[bot]
    export SLACK_BOT_TOKEN=xoxb-...
    export SLACK_CHANNEL=C0123456789
    export OPENAI_API_KEY=sk-...
"""

from xoneaiagents import Agent
from xoneaiagents.tools.shell_tools import execute_command
from xoneai.bots import SlackApproval

agent = Agent(
    name="DevOps",
    instructions="You are a DevOps assistant. Use shell tools when asked.",
    tools=[execute_command],
    approval=SlackApproval(),
)

agent.start("List files in the current directory")
