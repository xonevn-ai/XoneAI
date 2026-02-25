# xoneai/inc/__init__.py
# Lazy loading - XoneAIModel is only imported when accessed
# This avoids the ~3500ms langchain_openai import at CLI startup

def __getattr__(name):
    """Lazy load XoneAIModel only when accessed."""
    if name == "XoneAIModel":
        from .models import XoneAIModel
        return XoneAIModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["XoneAIModel"]