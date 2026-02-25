"""
XoneAI Knowledge - Advanced knowledge management system with configurable features.

This module provides:
- Document readers (ReaderProtocol, ReaderRegistry)
- Vector stores (VectorStoreProtocol, VectorStoreRegistry)
- Retrieval strategies (RetrieverProtocol, RetrievalStrategy)
- Rerankers (RerankerProtocol, RerankerRegistry)
- Index types (IndexProtocol, IndexType)
- Query engines (QueryEngineProtocol, QueryMode)
"""

# Core Knowledge class (always available)
from xoneaiagents.knowledge.knowledge import Knowledge
from xoneaiagents.knowledge.chunking import Chunking

# Lazy loading for protocols and registries to avoid import overhead
_LAZY_IMPORTS = {
    # Models and Protocols (new)
    "SearchResultItem": ("xoneaiagents.knowledge.models", "SearchResultItem"),
    "SearchResult": ("xoneaiagents.knowledge.models", "SearchResult"),
    "AddResult": ("xoneaiagents.knowledge.models", "AddResult"),
    "normalize_search_item": ("xoneaiagents.knowledge.models", "normalize_search_item"),
    "normalize_search_result": ("xoneaiagents.knowledge.models", "normalize_search_result"),
    "normalize_to_dict": ("xoneaiagents.knowledge.models", "normalize_to_dict"),
    "KnowledgeStoreProtocol": ("xoneaiagents.knowledge.protocols", "KnowledgeStoreProtocol"),
    "KnowledgeBackendError": ("xoneaiagents.knowledge.protocols", "KnowledgeBackendError"),
    "ScopeRequiredError": ("xoneaiagents.knowledge.protocols", "ScopeRequiredError"),
    "BackendNotAvailableError": ("xoneaiagents.knowledge.protocols", "BackendNotAvailableError"),
    
    # Readers
    "Document": ("xoneaiagents.knowledge.readers", "Document"),
    "ReaderProtocol": ("xoneaiagents.knowledge.readers", "ReaderProtocol"),
    "ReaderRegistry": ("xoneaiagents.knowledge.readers", "ReaderRegistry"),
    "get_reader_registry": ("xoneaiagents.knowledge.readers", "get_reader_registry"),
    "detect_source_kind": ("xoneaiagents.knowledge.readers", "detect_source_kind"),
    
    # Vector stores
    "VectorRecord": ("xoneaiagents.knowledge.vector_store", "VectorRecord"),
    "VectorStoreProtocol": ("xoneaiagents.knowledge.vector_store", "VectorStoreProtocol"),
    "VectorStoreRegistry": ("xoneaiagents.knowledge.vector_store", "VectorStoreRegistry"),
    "get_vector_store_registry": ("xoneaiagents.knowledge.vector_store", "get_vector_store_registry"),
    "InMemoryVectorStore": ("xoneaiagents.knowledge.vector_store", "InMemoryVectorStore"),
    
    # Retrieval
    "RetrievalResult": ("xoneaiagents.knowledge.retrieval", "RetrievalResult"),
    "RetrievalStrategy": ("xoneaiagents.knowledge.retrieval", "RetrievalStrategy"),
    "RetrieverProtocol": ("xoneaiagents.knowledge.retrieval", "RetrieverProtocol"),
    "RetrieverRegistry": ("xoneaiagents.knowledge.retrieval", "RetrieverRegistry"),
    "get_retriever_registry": ("xoneaiagents.knowledge.retrieval", "get_retriever_registry"),
    "reciprocal_rank_fusion": ("xoneaiagents.knowledge.retrieval", "reciprocal_rank_fusion"),
    "merge_adjacent_chunks": ("xoneaiagents.knowledge.retrieval", "merge_adjacent_chunks"),
    
    # Rerankers
    "RerankResult": ("xoneaiagents.knowledge.rerankers", "RerankResult"),
    "RerankerProtocol": ("xoneaiagents.knowledge.rerankers", "RerankerProtocol"),
    "RerankerRegistry": ("xoneaiagents.knowledge.rerankers", "RerankerRegistry"),
    "get_reranker_registry": ("xoneaiagents.knowledge.rerankers", "get_reranker_registry"),
    "SimpleReranker": ("xoneaiagents.knowledge.rerankers", "SimpleReranker"),
    
    # Index
    "IndexType": ("xoneaiagents.knowledge.index", "IndexType"),
    "IndexStats": ("xoneaiagents.knowledge.index", "IndexStats"),
    "IndexProtocol": ("xoneaiagents.knowledge.index", "IndexProtocol"),
    "IndexRegistry": ("xoneaiagents.knowledge.index", "IndexRegistry"),
    "get_index_registry": ("xoneaiagents.knowledge.index", "get_index_registry"),
    "KeywordIndex": ("xoneaiagents.knowledge.index", "KeywordIndex"),
    
    # Query engine
    "QueryMode": ("xoneaiagents.knowledge.query_engine", "QueryMode"),
    "QueryResult": ("xoneaiagents.knowledge.query_engine", "QueryResult"),
    "QueryEngineProtocol": ("xoneaiagents.knowledge.query_engine", "QueryEngineProtocol"),
    "QueryEngineRegistry": ("xoneaiagents.knowledge.query_engine", "QueryEngineRegistry"),
    "get_query_engine_registry": ("xoneaiagents.knowledge.query_engine", "get_query_engine_registry"),
    "decompose_question": ("xoneaiagents.knowledge.query_engine", "decompose_question"),
    "SimpleQueryEngine": ("xoneaiagents.knowledge.query_engine", "SimpleQueryEngine"),
    "SubQuestionEngine": ("xoneaiagents.knowledge.query_engine", "SubQuestionEngine"),
}


def __getattr__(name: str):
    """Lazy load protocols and registries."""
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys()) + ["Knowledge", "Chunking"]


__all__ = [
    # Core
    "Knowledge",
    "Chunking",
    # Models and Protocols
    "SearchResultItem",
    "SearchResult",
    "AddResult",
    "normalize_search_item",
    "normalize_search_result",
    "normalize_to_dict",
    "KnowledgeStoreProtocol",
    "KnowledgeBackendError",
    "ScopeRequiredError",
    "BackendNotAvailableError",
    # Readers
    "Document",
    "ReaderProtocol",
    "ReaderRegistry",
    "get_reader_registry",
    "detect_source_kind",
    # Vector stores
    "VectorRecord",
    "VectorStoreProtocol",
    "VectorStoreRegistry",
    "get_vector_store_registry",
    "InMemoryVectorStore",
    # Retrieval
    "RetrievalResult",
    "RetrievalStrategy",
    "RetrieverProtocol",
    "RetrieverRegistry",
    "get_retriever_registry",
    "reciprocal_rank_fusion",
    "merge_adjacent_chunks",
    # Rerankers
    "RerankResult",
    "RerankerProtocol",
    "RerankerRegistry",
    "get_reranker_registry",
    "SimpleReranker",
    # Index
    "IndexType",
    "IndexStats",
    "IndexProtocol",
    "IndexRegistry",
    "get_index_registry",
    "KeywordIndex",
    # Query engine
    "QueryMode",
    "QueryResult",
    "QueryEngineProtocol",
    "QueryEngineRegistry",
    "get_query_engine_registry",
    "decompose_question",
    "SimpleQueryEngine",
    "SubQuestionEngine",
] 