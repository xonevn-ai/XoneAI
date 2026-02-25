"""
Sandbox Protocols for XoneAI Agents.

Provides protocols and base classes for building sandbox implementations
that enable safe code execution in isolated environments.

This module contains only protocols and lightweight utilities.
Heavy implementations (Docker, etc.) live in the xoneai wrapper package.
"""

from .protocols import (
    SandboxProtocol,
    SandboxResult,
    SandboxStatus,
    ResourceLimits,
)
from .config import SandboxConfig, SecurityPolicy

__all__ = [
    "SandboxProtocol",
    "SandboxResult",
    "SandboxStatus",
    "ResourceLimits",
    "SandboxConfig",
    "SecurityPolicy",
]
