"""
XoneAI CLI Package

This package provides the command-line interface for XoneAI.

Structure:
- main.py: Main CLI entry point (XoneAI class)
- features/: Feature handlers for CLI flags and commands
"""

__all__ = ["XoneAI"]


def __getattr__(name):
    """Lazy load XoneAI to avoid slow imports."""
    if name == "XoneAI":
        from .main import XoneAI
        return XoneAI
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def main():
    """CLI entry point function."""
    from .main import XoneAI
    xone_ai = XoneAI()
    xone_ai.main()
