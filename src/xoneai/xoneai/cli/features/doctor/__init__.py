"""
Doctor CLI module for XoneAI.

Provides comprehensive health checks, diagnostics, and validation for the XoneAI ecosystem.

Commands:
    xoneai doctor              - Run fast default checks
    xoneai doctor env          - Environment and API key validation
    xoneai doctor config       - Configuration file validation
    xoneai doctor tools        - Tool availability checks
    xoneai doctor db           - Database connectivity checks
    xoneai doctor mcp          - MCP server validation
    xoneai doctor obs          - Observability provider checks
    xoneai doctor skills       - Agent skills validation
    xoneai doctor memory       - Memory/session storage checks
    xoneai doctor permissions  - Filesystem permission checks
    xoneai doctor network      - Network connectivity checks
    xoneai doctor performance  - Import time analysis
    xoneai doctor ci           - CI-optimized checks
    xoneai doctor selftest     - Minimal agent dry-run
"""

__version__ = "1.0.0"

__all__ = [
    "DoctorHandler",
    "DoctorEngine",
    "CheckResult",
    "CheckStatus",
    "DoctorReport",
    "CheckRegistry",
    "TextFormatter",
    "JsonFormatter",
]


def __getattr__(name: str):
    """Lazy load doctor components to minimize import overhead."""
    if name == "DoctorHandler":
        from .handler import DoctorHandler
        return DoctorHandler
    elif name == "DoctorEngine":
        from .engine import DoctorEngine
        return DoctorEngine
    elif name == "CheckResult":
        from .models import CheckResult
        return CheckResult
    elif name == "CheckStatus":
        from .models import CheckStatus
        return CheckStatus
    elif name == "DoctorReport":
        from .models import DoctorReport
        return DoctorReport
    elif name == "CheckRegistry":
        from .registry import CheckRegistry
        return CheckRegistry
    elif name == "TextFormatter":
        from .formatters import TextFormatter
        return TextFormatter
    elif name == "JsonFormatter":
        from .formatters import JsonFormatter
        return JsonFormatter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
