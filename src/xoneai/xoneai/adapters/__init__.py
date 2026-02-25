"""
XoneAI Adapters - Implementations for core protocols.

This module provides concrete implementations of:
- Reader adapters (AutoReader, LlamaIndexReaderAdapter, MarkItDownReaderAdapter)
- Vector store adapters (ChromaAdapter, PineconeAdapter, etc.)
- Retriever implementations
- Reranker implementations
"""

# Lazy loading to avoid heavy imports at package load time
_LAZY_IMPORTS = {
    # Readers
    "AutoReader": ("xoneai.adapters.readers", "AutoReader"),
    "MarkItDownReader": ("xoneai.adapters.readers", "MarkItDownReader"),
    "TextReader": ("xoneai.adapters.readers", "TextReader"),
    "DirectoryReader": ("xoneai.adapters.readers", "DirectoryReader"),
    "register_default_readers": ("xoneai.adapters.readers", "register_default_readers"),
    
    # Vector stores
    "ChromaVectorStore": ("xoneai.adapters.vector_stores", "ChromaVectorStore"),
    "register_default_vector_stores": ("xoneai.adapters.vector_stores", "register_default_vector_stores"),
    
    # Retrievers
    "BasicRetriever": ("xoneai.adapters.retrievers", "BasicRetriever"),
    "FusionRetriever": ("xoneai.adapters.retrievers", "FusionRetriever"),
    "register_default_retrievers": ("xoneai.adapters.retrievers", "register_default_retrievers"),
    
    # Rerankers
    "LLMReranker": ("xoneai.adapters.rerankers", "LLMReranker"),
    "register_default_rerankers": ("xoneai.adapters.rerankers", "register_default_rerankers"),
}


def __getattr__(name: str):
    """Lazy load adapters."""
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys())


__all__ = list(_LAZY_IMPORTS.keys())
