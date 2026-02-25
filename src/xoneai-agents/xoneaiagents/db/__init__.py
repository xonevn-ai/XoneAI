"""
Database adapter interface for XoneAI Agents.

This module provides the protocol and types for database persistence.
Implementations are provided by the wrapper layer (xoneai.db).

Usage (simplest - recommended):
    from xoneaiagents import Agent, db
    
    agent = Agent(
        name="Assistant",
        db=db(database_url="postgresql://localhost/mydb"),  # db(...) shortcut
        session_id="my-session"  # optional: defaults to per-hour ID
    )
    agent.chat("Hello!")  # auto-persists messages, runs, traces, tool calls

Alternative (explicit backend):
    db=db.XoneDB(database_url="...")  # Auto-detect backend
    db=db.PostgresDB(host="localhost")   # PostgreSQL
    db=db.SQLiteDB(path="data.db")       # SQLite
    db=db.RedisDB(host="localhost")      # Redis (state only)
"""

from .protocol import (
    DbAdapter,
    AsyncDbAdapter,
    DbMessage,
    DbToolCall,
    DbRun,
    DbSpan,
    DbTrace,
)


class _LazyDbModule:
    """
    Lazy proxy for database backends.
    
    Allows `from xoneaiagents import db` without importing heavy deps.
    Actual backend classes are loaded only when accessed.
    """
    
    _BACKENDS = {
        "XoneDB": "xoneai.db.adapter",
        "PostgresDB": "xoneai.db.adapter",
        "SQLiteDB": "xoneai.db.adapter",
        "RedisDB": "xoneai.db.adapter",
    }
    
    def __getattr__(self, name: str):
        if name in self._BACKENDS:
            try:
                import importlib
                module = importlib.import_module(self._BACKENDS[name])
                return getattr(module, name)
            except ImportError as e:
                raise ImportError(
                    f"Database backend '{name}' requires the xoneai package. "
                    f"Install with: pip install xoneai\n"
                    f"Original error: {e}"
                ) from e
        raise AttributeError(f"module 'db' has no attribute {name!r}")
    
    def __repr__(self):
        return "<module 'xoneaiagents.db' (lazy database backends)>"
    
    def __call__(self, **kwargs):
        """Shortcut: db(...) is equivalent to db.XoneDB(...)"""
        return self.XoneDB(**kwargs)


# Singleton lazy module instance
db = _LazyDbModule()


__all__ = [
    "DbAdapter",
    "AsyncDbAdapter",
    "DbMessage",
    "DbToolCall",
    "DbRun",
    "DbSpan",
    "DbTrace",
    "db",
]
