"""
XoneAI RAG - Retrieval Augmented Generation Module.

This module provides a thin orchestration layer over Knowledge for RAG workflows.
Knowledge handles indexing/retrieval; RAG adds answer generation with citations.

Usage:
    from xoneaiagents.rag import RAG, RAGConfig, RAGResult, Citation
    
    # With existing Knowledge
    rag = RAG(knowledge=my_knowledge)
    result = rag.query("What is the main finding?")
    print(result.answer)
    for citation in result.citations:
        print(f"  [{citation.id}] {citation.source}")

All imports are lazy to avoid performance impact when RAG is not used.
"""

from typing import TYPE_CHECKING

# Lazy loading to avoid import overhead
_LAZY_IMPORTS = {
    # Models
    "Citation": ("xoneaiagents.rag.models", "Citation"),
    "ContextPack": ("xoneaiagents.rag.models", "ContextPack"),
    "RAGResult": ("xoneaiagents.rag.models", "RAGResult"),
    "RAGConfig": ("xoneaiagents.rag.models", "RAGConfig"),
    # Unified retrieval config (Agent-first)
    "RetrievalConfig": ("xoneaiagents.rag.retrieval_config", "RetrievalConfig"),
    "RetrievalPolicy": ("xoneaiagents.rag.retrieval_config", "RetrievalPolicy"),
    "CitationsMode": ("xoneaiagents.rag.retrieval_config", "CitationsMode"),
    "create_retrieval_config": ("xoneaiagents.rag.retrieval_config", "create_retrieval_config"),
    # Token Budget (Phase 1)
    "TokenBudget": ("xoneaiagents.rag.budget", "TokenBudget"),
    "get_model_context_window": ("xoneaiagents.rag.budget", "get_model_context_window"),
    "BudgetEnforcerProtocol": ("xoneaiagents.rag.budget", "BudgetEnforcerProtocol"),
    "DefaultBudgetEnforcer": ("xoneaiagents.rag.budget", "DefaultBudgetEnforcer"),
    "estimate_tokens": ("xoneaiagents.rag.budget", "estimate_tokens"),
    # Strategy Selection (Phase 3) - RetrievalStrategy now from strategy module
    "RetrievalStrategy": ("xoneaiagents.rag.strategy", "RetrievalStrategy"),
    "select_strategy": ("xoneaiagents.rag.strategy", "select_strategy"),
    "get_strategy_description": ("xoneaiagents.rag.strategy", "get_strategy_description"),
    "STRATEGY_THRESHOLDS": ("xoneaiagents.rag.strategy", "STRATEGY_THRESHOLDS"),
    # SmartRetriever (Phase 4)
    "SmartRetriever": ("xoneaiagents.rag.retriever", "SmartRetriever"),
    "RetrievalResult": ("xoneaiagents.rag.retriever", "RetrievalResult"),
    "SimpleReranker": ("xoneaiagents.rag.retriever", "SimpleReranker"),
    "RetrieverProtocol": ("xoneaiagents.rag.retriever", "RetrieverProtocol"),
    "RerankerProtocol": ("xoneaiagents.rag.retriever", "RerankerProtocol"),
    # Compressor (Phase 5)
    "ContextCompressor": ("xoneaiagents.rag.compressor", "ContextCompressor"),
    "CompressionResult": ("xoneaiagents.rag.compressor", "CompressionResult"),
    "CompressorProtocol": ("xoneaiagents.rag.compressor", "CompressorProtocol"),
    # Summarizer (Phase 6)
    "HierarchicalSummarizer": ("xoneaiagents.rag.summarizer", "HierarchicalSummarizer"),
    "SummaryNode": ("xoneaiagents.rag.summarizer", "SummaryNode"),
    "HierarchyResult": ("xoneaiagents.rag.summarizer", "HierarchyResult"),
    # Protocols
    "ContextBuilderProtocol": ("xoneaiagents.rag.protocols", "ContextBuilderProtocol"),
    "CitationFormatterProtocol": ("xoneaiagents.rag.protocols", "CitationFormatterProtocol"),
    # Pipeline (internal - use Agent for primary access)
    "RAG": ("xoneaiagents.rag.pipeline", "RAG"),
    # Context utilities
    "build_context": ("xoneaiagents.rag.context", "build_context"),
    "truncate_context": ("xoneaiagents.rag.context", "truncate_context"),
    "deduplicate_chunks": ("xoneaiagents.rag.context", "deduplicate_chunks"),
}

_cache = {}


def __getattr__(name: str):
    """Lazy load RAG components."""
    if name in _cache:
        return _cache[name]
    
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        value = getattr(module, attr_name)
        _cache[name] = value
        return value
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys())


__all__ = list(_LAZY_IMPORTS.keys())

if TYPE_CHECKING:
    from .models import Citation, ContextPack, RAGResult, RAGConfig
    from .protocols import ContextBuilderProtocol, CitationFormatterProtocol
    from .pipeline import RAG
    from .context import build_context, truncate_context, deduplicate_chunks
