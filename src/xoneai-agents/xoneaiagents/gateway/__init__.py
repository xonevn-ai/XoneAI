"""
Gateway module for XoneAI Agents.

Provides protocols and base classes for building gateway/control plane
implementations that coordinate multi-agent deployments.

This module contains only protocols and lightweight utilities.
Heavy implementations live in the xoneai wrapper package.
"""

from .protocols import (
    GatewayProtocol,
    GatewaySessionProtocol,
    GatewayClientProtocol,
    GatewayEvent,
    GatewayMessage,
    EventType,
)
from .config import GatewayConfig, SessionConfig, ChannelRouteConfig, MultiChannelGatewayConfig

__all__ = [
    "GatewayProtocol",
    "GatewaySessionProtocol",
    "GatewayClientProtocol",
    "GatewayEvent",
    "GatewayMessage",
    "EventType",
    "GatewayConfig",
    "SessionConfig",
    "ChannelRouteConfig",
    "MultiChannelGatewayConfig",
]
