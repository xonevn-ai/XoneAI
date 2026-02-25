"""
AutoAgents Example

AutoAgents automatically creates and manages AI agents based on high-level instructions.
It features dynamic agent count based on task complexity.

Documentation: https://docs.xone.ai/features/autoagents
CLI Reference: https://docs.xone.ai/nocode/auto

New Features:
- Dynamic agent count (1-4 based on task complexity)
- Workflow patterns: sequential, parallel, routing, orchestrator-workers, evaluator-optimizer
- Pattern recommendation based on task keywords
- Tool preservation from LLM suggestions
"""

from xoneaiagents import AutoAgents
from xoneaiagents.tools import duckduckgo

# Basic usage - AutoAgents analyzes complexity and creates optimal agents
agents = AutoAgentTeam(
    instructions="Search for information about AI Agents",
    tools=[duckduckgo],
    process="sequential",  # or "hierarchical"
    max_agents=3  # Maximum number of agents to create
)

result = agents.start()
print(result)

# =============================================================================
# CLI Usage Examples (for reference)
# =============================================================================
# 
# # Auto-generate agents (dynamic count based on complexity)
# xoneai --auto "Write a haiku about spring"
# xoneai --auto "Research AI trends, analyze data, write report"
#
# # Auto-generate workflow with specific pattern
# xoneai workflow auto "Research and write" --pattern sequential
# xoneai workflow auto "Research from multiple sources" --pattern parallel
# xoneai workflow auto "Comprehensive analysis" --pattern orchestrator-workers
# xoneai workflow auto "Refine content quality" --pattern evaluator-optimizer
#
# # With framework selection
# xoneai --framework crewai --auto "Create a movie script"
# xoneai --framework autogen --auto "Create a movie script"