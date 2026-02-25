"""
AG-UI Protocol Integration for XoneAI Agents

This module provides AG-UI (Agent-User Interface) protocol support,
enabling XoneAI Agents to be exposed via a standardized streaming API
compatible with CopilotKit and other AG-UI frontends.

Usage:
    from xoneaiagents import Agent
    from xoneaiagents.ui.agui import AGUI
    from fastapi import FastAPI

    agent = Agent(name="Assistant", role="Helper", goal="Help users")
    agui = AGUI(agent=agent)

    app = FastAPI()
    app.include_router(agui.get_router())
"""

from xoneaiagents.ui.agui.agui import AGUI

__all__ = ["AGUI"]
