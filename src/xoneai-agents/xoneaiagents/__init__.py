"""
Xone AI Agents - A package for hierarchical AI agent task execution

This module uses lazy loading to minimize import time and memory usage.
Heavy dependencies like litellm are only loaded when actually needed.
"""

# =============================================================================
# NAMING CONVENTION GUIDE (Simplified patterns for consistency)
# =============================================================================
# | Pattern       | When to Use             | Examples                        |
# |---------------|-------------------------|----------------------------------|
# | add_X         | Register something      | add_hook, add_tool, add_profile |
# | get_X         | Retrieve something      | get_tool, get_profile           |
# | remove_X      | Unregister something    | remove_hook, remove_tool        |
# | has_X         | Check existence         | has_hook, has_tool              |
# | list_X        | List all items          | list_tools, list_profiles       |
# | enable_X      | Turn on feature         | enable_telemetry                |
# | disable_X     | Turn off feature        | disable_telemetry               |
# | XConfig       | Configuration class     | MemoryConfig, HooksConfig       |
# | @decorator    | Decorator               | @tool, @add_hook                |
# |---------------|-------------------------|----------------------------------|
# | set_default_X | Internal/advanced only  | (don't simplify - internal)     |
# | create_X      | Factory function        | (already well-named)            |
# =============================================================================

# =============================================================================
# NAMESPACE PACKAGE GUARD
# =============================================================================
# Detect if we're loaded as a namespace package (which indicates stale artifacts
# in site-packages). This happens when there's a xoneaiagents/ directory in
# site-packages without an __init__.py file.
#
# Root cause: Partial uninstall or version mismatch leaves directories that
# Python's PathFinder treats as namespace packages, shadowing the real package.
# =============================================================================
if __file__ is None:
    import warnings as _ns_warnings
    _ns_warnings.warn(
        "xoneaiagents is loaded as a namespace package, which indicates "
        "stale artifacts in site-packages. This will cause import errors. "
        "Fix: Remove the stale directory with:\n"
        "  rm -rf $(python -c \"import site; print(site.getsitepackages()[0])\")/xoneaiagents/\n"
        "Then reinstall: pip install xoneaiagents",
        ImportWarning,
        stacklevel=1
    )
    del _ns_warnings

# Apply warning patch BEFORE any imports to intercept warnings at the source
from . import _warning_patch  # noqa: F401

# Import centralized logging configuration FIRST
from . import _logging

# Configure root logger after logging is initialized
_logging.configure_root_logger()

# Import configuration (lightweight, no heavy deps)
from . import _config

# Lightweight imports that don't trigger heavy dependency chains
from .tools.tools import Tools
from .tools.base import BaseTool, ToolResult, ToolValidationError, validate_tool
from .tools.decorator import tool, FunctionTool
from .tools.registry import get_registry, register_tool, get_tool, ToolRegistry
# db and obs are lazy-loaded via __getattr__ for performance

# Sub-packages for organized imports (pa.config, pa.tools, etc.)
# These enable: import xoneaiagents as pa; pa.config.MemoryConfig
from . import config
from . import tools
# Note: db, obs, knowledge and mcp are lazy-loaded via __getattr__ due to heavy deps

# Embedding API - LAZY LOADED via __getattr__ for performance
# Supports: embedding, embeddings, aembedding, aembeddings, EmbeddingResult, get_dimensions

# Workflows - LAZY LOADED (moved to __getattr__)
# Workflow, Task, WorkflowContext, StepResult, Route, Parallel, Loop, Repeat, etc.

# Guardrails - LAZY LOADED (imports main.py which imports rich)
# GuardrailResult and LLMGuardrail moved to __getattr__

# Handoff - LAZY LOADED (moved to __getattr__)
# Handoff, handoff, handoff_filters, etc.

# Flow display - LAZY LOADED (moved to __getattr__)
# FlowDisplay and track_workflow are now lazy loaded

# Main display utilities - LAZY LOADED to avoid importing rich at startup
# These are only needed when output=verbose, not for silent mode
# Moved to __getattr__ for lazy loading

# ============================================================================
# LAZY LOADING CONFIGURATION
# ============================================================================
# Using centralized _lazy.py utility for DRY, thread-safe lazy loading.
# All heavy dependencies are loaded on-demand to minimize import time.
# ============================================================================

from ._lazy import lazy_import, create_lazy_getattr_with_fallback

# Thread-safe cache for lazy-loaded values
_lazy_cache = {}

# Backward compatibility: _get_lazy_cache function for tests
import threading
_lazy_cache_local = threading.local()

def _get_lazy_cache():
    """Get thread-local lazy cache dict. Thread-safe for concurrent access.
    
    Note: This is kept for backward compatibility with tests.
    The main lazy loading now uses the centralized _lazy.py utility.
    """
    if not hasattr(_lazy_cache_local, 'cache'):
        _lazy_cache_local.cache = {}
    return _lazy_cache_local.cache

# ============================================================================
# LAZY IMPORT MAPPING
# ============================================================================
# Maps attribute names to (module_path, attr_name) tuples.
# This is the single source of truth for all lazy imports.
# ============================================================================

_LAZY_IMPORTS = {
    # Main display utilities (imports rich)
    'TaskOutput': ('xoneaiagents.main', 'TaskOutput'),
    'ReflectionOutput': ('xoneaiagents.main', 'ReflectionOutput'),
    'display_interaction': ('xoneaiagents.main', 'display_interaction'),
    'display_self_reflection': ('xoneaiagents.main', 'display_self_reflection'),
    'display_instruction': ('xoneaiagents.main', 'display_instruction'),
    'display_tool_call': ('xoneaiagents.main', 'display_tool_call'),
    'display_error': ('xoneaiagents.main', 'display_error'),
    'display_generating': ('xoneaiagents.main', 'display_generating'),
    'clean_triple_backticks': ('xoneaiagents.main', 'clean_triple_backticks'),
    'error_logs': ('xoneaiagents.main', 'error_logs'),
    'register_display_callback': ('xoneaiagents.main', 'register_display_callback'),
    'sync_display_callbacks': ('xoneaiagents.main', 'sync_display_callbacks'),
    'async_display_callbacks': ('xoneaiagents.main', 'async_display_callbacks'),
    
    # AgentFlow (primary) / Workflow (alias)
    'AgentFlow': ('xoneaiagents.workflows', 'AgentFlow'),
    'Workflow': ('xoneaiagents.workflows', 'Workflow'),  # Silent alias
    'Pipeline': ('xoneaiagents.workflows', 'Pipeline'),  # Silent alias
    'WorkflowContext': ('xoneaiagents.workflows', 'WorkflowContext'),
    'StepResult': ('xoneaiagents.workflows', 'StepResult'),
    'Route': ('xoneaiagents.workflows', 'Route'),
    'Parallel': ('xoneaiagents.workflows', 'Parallel'),
    'Loop': ('xoneaiagents.workflows', 'Loop'),
    'Repeat': ('xoneaiagents.workflows', 'Repeat'),
    'If': ('xoneaiagents.workflows', 'If'),
    'route': ('xoneaiagents.workflows', 'route'),
    'parallel': ('xoneaiagents.workflows', 'parallel'),
    'loop': ('xoneaiagents.workflows', 'loop'),
    'repeat': ('xoneaiagents.workflows', 'repeat'),
    'when': ('xoneaiagents.workflows', 'when'),
    
    # Conditions (Protocol-driven condition evaluation)
    'ConditionProtocol': ('xoneaiagents.conditions.protocols', 'ConditionProtocol'),
    'RoutingConditionProtocol': ('xoneaiagents.conditions.protocols', 'RoutingConditionProtocol'),
    'ExpressionCondition': ('xoneaiagents.conditions.evaluator', 'ExpressionCondition'),
    'DictCondition': ('xoneaiagents.conditions.evaluator', 'DictCondition'),
    'evaluate_condition': ('xoneaiagents.conditions.evaluator', 'evaluate_condition'),
    
    # Handoff
    'Handoff': ('xoneaiagents.agent.handoff', 'Handoff'),
    'handoff': ('xoneaiagents.agent.handoff', 'handoff'),
    'handoff_filters': ('xoneaiagents.agent.handoff', 'handoff_filters'),
    'RECOMMENDED_PROMPT_PREFIX': ('xoneaiagents.agent.handoff', 'RECOMMENDED_PROMPT_PREFIX'),
    'prompt_with_handoff_instructions': ('xoneaiagents.agent.handoff', 'prompt_with_handoff_instructions'),
    'HandoffConfig': ('xoneaiagents.agent.handoff', 'HandoffConfig'),
    'HandoffResult': ('xoneaiagents.agent.handoff', 'HandoffResult'),
    'HandoffInputData': ('xoneaiagents.agent.handoff', 'HandoffInputData'),
    'ContextPolicy': ('xoneaiagents.agent.handoff', 'ContextPolicy'),
    'HandoffError': ('xoneaiagents.agent.handoff', 'HandoffError'),
    'HandoffCycleError': ('xoneaiagents.agent.handoff', 'HandoffCycleError'),
    'HandoffDepthError': ('xoneaiagents.agent.handoff', 'HandoffDepthError'),
    'HandoffTimeoutError': ('xoneaiagents.agent.handoff', 'HandoffTimeoutError'),
    
    # Embedding API
    'embedding': ('xoneaiagents.embedding.embed', 'embedding'),
    'embeddings': ('xoneaiagents.embedding.embed', 'embedding'),
    'aembedding': ('xoneaiagents.embedding.embed', 'aembedding'),
    'aembeddings': ('xoneaiagents.embedding.embed', 'aembedding'),
    'embed': ('xoneaiagents.embedding.embed', 'embed'),
    'aembed': ('xoneaiagents.embedding.embed', 'aembed'),
    'EmbeddingResult': ('xoneaiagents.embedding.result', 'EmbeddingResult'),
    'get_dimensions': ('xoneaiagents.embedding.dimensions', 'get_dimensions'),
    
    # Guardrails
    'GuardrailResult': ('xoneaiagents.guardrails', 'GuardrailResult'),
    'LLMGuardrail': ('xoneaiagents.guardrails', 'LLMGuardrail'),
    
    # Approval (agent-centric approval backends)
    'AutoApproveBackend': ('xoneaiagents.approval.backends', 'AutoApproveBackend'),
    'ConsoleBackend': ('xoneaiagents.approval.backends', 'ConsoleBackend'),
    
    # Flow display
    'FlowDisplay': ('xoneaiagents.flow_display', 'FlowDisplay'),
    'track_workflow': ('xoneaiagents.flow_display', 'track_workflow'),
    
    # Agent classes
    'Agent': ('xoneaiagents.agent.agent', 'Agent'),
    'ImageAgent': ('xoneaiagents.agent.image_agent', 'ImageAgent'),
    'VideoAgent': ('xoneaiagents.agent.video_agent', 'VideoAgent'),
    'VideoConfig': ('xoneaiagents.agent.video_agent', 'VideoConfig'),
    'AudioAgent': ('xoneaiagents.agent.audio_agent', 'AudioAgent'),
    'AudioConfig': ('xoneaiagents.agent.audio_agent', 'AudioConfig'),
    'OCRAgent': ('xoneaiagents.agent.ocr_agent', 'OCRAgent'),
    'OCRConfig': ('xoneaiagents.agent.ocr_agent', 'OCRConfig'),
    'ContextAgent': ('xoneaiagents.agent.context_agent', 'ContextAgent'),
    'create_context_agent': ('xoneaiagents.agent.context_agent', 'create_context_agent'),
    'DeepResearchAgent': ('xoneaiagents.agent.deep_research_agent', 'DeepResearchAgent'),
    'DeepResearchResponse': ('xoneaiagents.agent.deep_research_agent', 'DeepResearchResponse'),
    'ReasoningStep': ('xoneaiagents.agent.deep_research_agent', 'ReasoningStep'),
    'WebSearchCall': ('xoneaiagents.agent.deep_research_agent', 'WebSearchCall'),
    'CodeExecutionStep': ('xoneaiagents.agent.deep_research_agent', 'CodeExecutionStep'),
    'MCPCall': ('xoneaiagents.agent.deep_research_agent', 'MCPCall'),
    'FileSearchCall': ('xoneaiagents.agent.deep_research_agent', 'FileSearchCall'),
    'Provider': ('xoneaiagents.agent.deep_research_agent', 'Provider'),
    'QueryRewriterAgent': ('xoneaiagents.agent.query_rewriter_agent', 'QueryRewriterAgent'),
    'RewriteStrategy': ('xoneaiagents.agent.query_rewriter_agent', 'RewriteStrategy'),
    'RewriteResult': ('xoneaiagents.agent.query_rewriter_agent', 'RewriteResult'),
    'PromptExpanderAgent': ('xoneaiagents.agent.prompt_expander_agent', 'PromptExpanderAgent'),
    'ExpandStrategy': ('xoneaiagents.agent.prompt_expander_agent', 'ExpandStrategy'),
    'ExpandResult': ('xoneaiagents.agent.prompt_expander_agent', 'ExpandResult'),
    'VisionAgent': ('xoneaiagents.agent.vision_agent', 'VisionAgent'),
    'VisionConfig': ('xoneaiagents.agent.vision_agent', 'VisionConfig'),
    'EmbeddingAgent': ('xoneaiagents.agent.embedding_agent', 'EmbeddingAgent'),
    'EmbeddingConfig': ('xoneaiagents.agent.embedding_agent', 'EmbeddingConfig'),
    'RealtimeAgent': ('xoneaiagents.agent.realtime_agent', 'RealtimeAgent'),
    'RealtimeConfig': ('xoneaiagents.agent.realtime_agent', 'RealtimeConfig'),
    'CodeAgent': ('xoneaiagents.agent.code_agent', 'CodeAgent'),
    'CodeConfig': ('xoneaiagents.agent.code_agent', 'CodeConfig'),
    
    # AgentTeam (primary) / AgentManager (alias)
    'AgentTeam': ('xoneaiagents.agents.agents', 'AgentTeam'),
    'AgentManager': ('xoneaiagents.agents.agents', 'AgentManager'),  # Silent alias
    # Note: 'Agents' is handled by _custom_handler for deprecation warning
    'Task': ('xoneaiagents.task.task', 'Task'),
    'AutoAgents': ('xoneaiagents.agents.autoagents', 'AutoAgents'),
    'AutoRagAgent': ('xoneaiagents.agents.auto_rag_agent', 'AutoRagAgent'),
    'AutoRagConfig': ('xoneaiagents.agents.auto_rag_agent', 'AutoRagConfig'),
    'RagRetrievalPolicy': ('xoneaiagents.agents.auto_rag_agent', 'RetrievalPolicy'),
    
    # Session
    'Session': ('xoneaiagents.session', 'Session'),
    
    # AgentOS (primary) / AgentApp (alias) - protocol and config
    'AgentOSProtocol': ('xoneaiagents.app.protocols', 'AgentOSProtocol'),
    'AgentOSConfig': ('xoneaiagents.app', 'AgentOSConfig'),
    'AgentAppProtocol': ('xoneaiagents.app.protocols', 'AgentAppProtocol'),  # Silent alias
    'AgentAppConfig': ('xoneaiagents.app.config', 'AgentAppConfig'),  # Silent alias
    
    # MCP (optional)
    'MCP': ('xoneaiagents.mcp.mcp', 'MCP'),
    
    # Knowledge
    'Knowledge': ('xoneaiagents.knowledge.knowledge', 'Knowledge'),
    'Chunking': ('xoneaiagents.knowledge.chunking', 'Chunking'),
    
    # FastContext
    'FastContext': ('xoneaiagents.context.fast', 'FastContext'),
    'FastContextResult': ('xoneaiagents.context.fast', 'FastContextResult'),
    'FileMatch': ('xoneaiagents.context.fast', 'FileMatch'),
    'LineRange': ('xoneaiagents.context.fast', 'LineRange'),
    
    # RAG
    'RetrievalConfig': ('xoneaiagents.rag.retrieval_config', 'RetrievalConfig'),
    'RetrievalPolicy': ('xoneaiagents.rag.retrieval_config', 'RetrievalPolicy'),
    'CitationsMode': ('xoneaiagents.rag.retrieval_config', 'CitationsMode'),
    'ContextPack': ('xoneaiagents.rag.models', 'ContextPack'),
    'RAGResult': ('xoneaiagents.rag', 'RAGResult'),
    'Citation': ('xoneaiagents.rag', 'Citation'),
    'RAG': ('xoneaiagents.rag', 'RAG'),
    'RAGConfig': ('xoneaiagents.rag', 'RAGConfig'),
    'RAGCitation': ('xoneaiagents.rag', 'Citation'),
    
    # Skills
    'SkillManager': ('xoneaiagents.skills', 'SkillManager'),
    'SkillProperties': ('xoneaiagents.skills', 'SkillProperties'),
    'SkillMetadata': ('xoneaiagents.skills', 'SkillMetadata'),
    'SkillLoader': ('xoneaiagents.skills', 'SkillLoader'),
    
    # Memory
    'Memory': ('xoneaiagents.memory.memory', 'Memory'),
    
    # Planning
    'Plan': ('xoneaiagents.planning', 'Plan'),
    'PlanStep': ('xoneaiagents.planning', 'PlanStep'),
    'TodoList': ('xoneaiagents.planning', 'TodoList'),
    'TodoItem': ('xoneaiagents.planning', 'TodoItem'),
    'PlanStorage': ('xoneaiagents.planning', 'PlanStorage'),
    'PlanningAgent': ('xoneaiagents.planning', 'PlanningAgent'),
    'ApprovalCallback': ('xoneaiagents.planning', 'ApprovalCallback'),
    'READ_ONLY_TOOLS': ('xoneaiagents.planning', 'READ_ONLY_TOOLS'),
    'RESTRICTED_TOOLS': ('xoneaiagents.planning', 'RESTRICTED_TOOLS'),
    
    # Trace (protocol-driven, for custom sinks) - AGENTS.md naming: XProtocol
    'ContextTraceSinkProtocol': ('xoneaiagents.trace', 'ContextTraceSinkProtocol'),
    'ContextTraceSink': ('xoneaiagents.trace', 'ContextTraceSink'),  # Backward compat alias
    'TraceSinkProtocol': ('xoneaiagents.trace', 'TraceSinkProtocol'),
    'TraceSink': ('xoneaiagents.trace', 'TraceSink'),  # Backward compat alias
    'ContextTraceEmitter': ('xoneaiagents.trace', 'ContextTraceEmitter'),
    'ContextEvent': ('xoneaiagents.trace', 'ContextEvent'),
    'ContextEventType': ('xoneaiagents.trace', 'ContextEventType'),
    'trace_context': ('xoneaiagents.trace', 'trace_context'),
    'ContextListSink': ('xoneaiagents.trace', 'ContextListSink'),
    'ContextNoOpSink': ('xoneaiagents.trace', 'ContextNoOpSink'),
    
    # Telemetry
    'get_telemetry': ('xoneaiagents.telemetry', 'get_telemetry'),
    'enable_telemetry': ('xoneaiagents.telemetry', 'enable_telemetry'),
    'disable_telemetry': ('xoneaiagents.telemetry', 'disable_telemetry'),
    'enable_performance_mode': ('xoneaiagents.telemetry', 'enable_performance_mode'),
    'disable_performance_mode': ('xoneaiagents.telemetry', 'disable_performance_mode'),
    'cleanup_telemetry_resources': ('xoneaiagents.telemetry', 'cleanup_telemetry_resources'),
    'MinimalTelemetry': ('xoneaiagents.telemetry', 'MinimalTelemetry'),
    'TelemetryCollector': ('xoneaiagents.telemetry', 'TelemetryCollector'),
    
    # UI (optional)
    'AGUI': ('xoneaiagents.ui.agui', 'AGUI'),
    'A2A': ('xoneaiagents.ui.a2a', 'A2A'),
    
    # Feature configs
    'MemoryConfig': ('xoneaiagents.config.feature_configs', 'MemoryConfig'),
    'KnowledgeConfig': ('xoneaiagents.config.feature_configs', 'KnowledgeConfig'),
    'PlanningConfig': ('xoneaiagents.config.feature_configs', 'PlanningConfig'),
    'ReflectionConfig': ('xoneaiagents.config.feature_configs', 'ReflectionConfig'),
    'GuardrailConfig': ('xoneaiagents.config.feature_configs', 'GuardrailConfig'),
    'WebConfig': ('xoneaiagents.config.feature_configs', 'WebConfig'),
    'OutputConfig': ('xoneaiagents.config.feature_configs', 'OutputConfig'),
    'ExecutionConfig': ('xoneaiagents.config.feature_configs', 'ExecutionConfig'),
    'TemplateConfig': ('xoneaiagents.config.feature_configs', 'TemplateConfig'),
    'CachingConfig': ('xoneaiagents.config.feature_configs', 'CachingConfig'),
    'HooksConfig': ('xoneaiagents.config.feature_configs', 'HooksConfig'),
    'SkillsConfig': ('xoneaiagents.config.feature_configs', 'SkillsConfig'),
    'AutonomyConfig': ('xoneaiagents.agent.autonomy', 'AutonomyConfig'),
    'EscalationStage': ('xoneaiagents.escalation.types', 'EscalationStage'),
    'EscalationPipeline': ('xoneaiagents.escalation.pipeline', 'EscalationPipeline'),
    'ObservabilityHooks': ('xoneaiagents.escalation.observability', 'ObservabilityHooks'),
    'ObservabilityEventType': ('xoneaiagents.escalation.observability', 'EventType'),
    'DoomLoopDetector': ('xoneaiagents.escalation.doom_loop', 'DoomLoopDetector'),
    'MemoryBackend': ('xoneaiagents.config.feature_configs', 'MemoryBackend'),
    'ChunkingStrategy': ('xoneaiagents.config.feature_configs', 'ChunkingStrategy'),
    'GuardrailAction': ('xoneaiagents.config.feature_configs', 'GuardrailAction'),
    'WebSearchProvider': ('xoneaiagents.config.feature_configs', 'WebSearchProvider'),
    'OutputPreset': ('xoneaiagents.config.feature_configs', 'OutputPreset'),
    'ExecutionPreset': ('xoneaiagents.config.feature_configs', 'ExecutionPreset'),
    'AutonomyLevel': ('xoneaiagents.config.feature_configs', 'AutonomyLevel'),
    'MultiAgentHooksConfig': ('xoneaiagents.config.feature_configs', 'MultiAgentHooksConfig'),
    'MultiAgentOutputConfig': ('xoneaiagents.config.feature_configs', 'MultiAgentOutputConfig'),
    'MultiAgentExecutionConfig': ('xoneaiagents.config.feature_configs', 'MultiAgentExecutionConfig'),
    'MultiAgentPlanningConfig': ('xoneaiagents.config.feature_configs', 'MultiAgentPlanningConfig'),
    'MultiAgentMemoryConfig': ('xoneaiagents.config.feature_configs', 'MultiAgentMemoryConfig'),
    
    # Parameter resolver
    'resolve': ('xoneaiagents.config.param_resolver', 'resolve'),
    'ArrayMode': ('xoneaiagents.config.param_resolver', 'ArrayMode'),
    'resolve_memory': ('xoneaiagents.config.param_resolver', 'resolve_memory'),
    'resolve_knowledge': ('xoneaiagents.config.param_resolver', 'resolve_knowledge'),
    'resolve_output': ('xoneaiagents.config.param_resolver', 'resolve_output'),
    'resolve_execution': ('xoneaiagents.config.param_resolver', 'resolve_execution'),
    'resolve_web': ('xoneaiagents.config.param_resolver', 'resolve_web'),
    'resolve_planning': ('xoneaiagents.config.param_resolver', 'resolve_planning'),
    'resolve_reflection': ('xoneaiagents.config.param_resolver', 'resolve_reflection'),
    'resolve_context': ('xoneaiagents.config.param_resolver', 'resolve_context'),
    'resolve_autonomy': ('xoneaiagents.config.param_resolver', 'resolve_autonomy'),
    'resolve_caching': ('xoneaiagents.config.param_resolver', 'resolve_caching'),
    'resolve_hooks': ('xoneaiagents.config.param_resolver', 'resolve_hooks'),
    'resolve_skills': ('xoneaiagents.config.param_resolver', 'resolve_skills'),
    'resolve_routing': ('xoneaiagents.config.param_resolver', 'resolve_routing'),
    'resolve_guardrails': ('xoneaiagents.config.param_resolver', 'resolve_guardrails'),
    'resolve_guardrail_policies': ('xoneaiagents.config.param_resolver', 'resolve_guardrail_policies'),
    
    # Presets
    'MEMORY_PRESETS': ('xoneaiagents.config.presets', 'MEMORY_PRESETS'),
    'MEMORY_URL_SCHEMES': ('xoneaiagents.config.presets', 'MEMORY_URL_SCHEMES'),
    'OUTPUT_PRESETS': ('xoneaiagents.config.presets', 'OUTPUT_PRESETS'),
    'EXECUTION_PRESETS': ('xoneaiagents.config.presets', 'EXECUTION_PRESETS'),
    'WEB_PRESETS': ('xoneaiagents.config.presets', 'WEB_PRESETS'),
    'PLANNING_PRESETS': ('xoneaiagents.config.presets', 'PLANNING_PRESETS'),
    'REFLECTION_PRESETS': ('xoneaiagents.config.presets', 'REFLECTION_PRESETS'),
    'CONTEXT_PRESETS': ('xoneaiagents.config.presets', 'CONTEXT_PRESETS'),
    'AUTONOMY_PRESETS': ('xoneaiagents.config.presets', 'AUTONOMY_PRESETS'),
    'CACHING_PRESETS': ('xoneaiagents.config.presets', 'CACHING_PRESETS'),
    'MULTI_AGENT_OUTPUT_PRESETS': ('xoneaiagents.config.presets', 'MULTI_AGENT_OUTPUT_PRESETS'),
    'MULTI_AGENT_EXECUTION_PRESETS': ('xoneaiagents.config.presets', 'MULTI_AGENT_EXECUTION_PRESETS'),
    'GUARDRAIL_PRESETS': ('xoneaiagents.config.presets', 'GUARDRAIL_PRESETS'),
    'KNOWLEDGE_PRESETS': ('xoneaiagents.config.presets', 'KNOWLEDGE_PRESETS'),
    
    # Parse utilities
    'detect_url_scheme': ('xoneaiagents.config.parse_utils', 'detect_url_scheme'),
    'is_path_like': ('xoneaiagents.config.parse_utils', 'is_path_like'),
    'suggest_similar': ('xoneaiagents.config.parse_utils', 'suggest_similar'),
    'is_policy_string': ('xoneaiagents.config.parse_utils', 'is_policy_string'),
    'parse_policy_string': ('xoneaiagents.config.parse_utils', 'parse_policy_string'),
    
    # Context management
    'ContextConfig': ('xoneaiagents.context.models', 'ContextConfig'),
    'OptimizerStrategy': ('xoneaiagents.context.models', 'OptimizerStrategy'),
    'ManagerConfig': ('xoneaiagents.context.manager', 'ManagerConfig'),
    'ContextManager': ('xoneaiagents.context.manager', 'ContextManager'),
    
    # db and obs modules
    'db': ('xoneaiagents.db', 'db'),
    'obs': ('xoneaiagents.obs', 'obs'),
    
    # Gateway protocols and config (implementations in xoneai wrapper)
    'GatewayProtocol': ('xoneaiagents.gateway.protocols', 'GatewayProtocol'),
    'GatewaySessionProtocol': ('xoneaiagents.gateway.protocols', 'GatewaySessionProtocol'),
    'GatewayClientProtocol': ('xoneaiagents.gateway.protocols', 'GatewayClientProtocol'),
    'GatewayEvent': ('xoneaiagents.gateway.protocols', 'GatewayEvent'),
    'GatewayMessage': ('xoneaiagents.gateway.protocols', 'GatewayMessage'),
    'EventType': ('xoneaiagents.gateway.protocols', 'EventType'),
    'GatewayConfig': ('xoneaiagents.gateway.config', 'GatewayConfig'),
    'SessionConfig': ('xoneaiagents.gateway.config', 'SessionConfig'),
    
    # Bot protocols and config (implementations in xoneai wrapper)
    'BotProtocol': ('xoneaiagents.bots.protocols', 'BotProtocol'),
    'BotMessage': ('xoneaiagents.bots.protocols', 'BotMessage'),
    'BotUser': ('xoneaiagents.bots.protocols', 'BotUser'),
    'BotChannel': ('xoneaiagents.bots.protocols', 'BotChannel'),
    'MessageType': ('xoneaiagents.bots.protocols', 'MessageType'),
    'BotConfig': ('xoneaiagents.bots.config', 'BotConfig'),
    'BotOSProtocol': ('xoneaiagents.bots.protocols', 'BotOSProtocol'),
    'BotOSConfig': ('xoneaiagents.bots.config', 'BotOSConfig'),
    
    # Sandbox protocols and config (implementations in xoneai wrapper)
    'SandboxProtocol': ('xoneaiagents.sandbox.protocols', 'SandboxProtocol'),
    'SandboxResult': ('xoneaiagents.sandbox.protocols', 'SandboxResult'),
    'SandboxStatus': ('xoneaiagents.sandbox.protocols', 'SandboxStatus'),
    'ResourceLimits': ('xoneaiagents.sandbox.protocols', 'ResourceLimits'),
    'SandboxConfig': ('xoneaiagents.sandbox.config', 'SandboxConfig'),
    'SecurityPolicy': ('xoneaiagents.sandbox.config', 'SecurityPolicy'),
    
    # Model failover
    'AuthProfile': ('xoneaiagents.llm.failover', 'AuthProfile'),
    'ProviderStatus': ('xoneaiagents.llm.failover', 'ProviderStatus'),
    'FailoverConfig': ('xoneaiagents.llm.failover', 'FailoverConfig'),
    'FailoverManager': ('xoneaiagents.llm.failover', 'FailoverManager'),
    
    # Plugins - Core classes
    'PluginManager': ('xoneaiagents.plugins', 'PluginManager'),
    'Plugin': ('xoneaiagents.plugins', 'Plugin'),
    'PluginInfo': ('xoneaiagents.plugins', 'PluginInfo'),
    'PluginHook': ('xoneaiagents.plugins', 'PluginHook'),
    'FunctionPlugin': ('xoneaiagents.plugins', 'FunctionPlugin'),
    'get_plugin_manager': ('xoneaiagents.plugins', 'get_plugin_manager'),
    
    # Plugins - Protocols
    'PluginProtocol': ('xoneaiagents.plugins', 'PluginProtocol'),
    'ToolPluginProtocol': ('xoneaiagents.plugins', 'ToolPluginProtocol'),
    'HookPluginProtocol': ('xoneaiagents.plugins', 'HookPluginProtocol'),
    'AgentPluginProtocol': ('xoneaiagents.plugins', 'AgentPluginProtocol'),
    'LLMPluginProtocol': ('xoneaiagents.plugins', 'LLMPluginProtocol'),
    
    # Plugins - Single-file plugin support
    'PluginMetadata': ('xoneaiagents.plugins', 'PluginMetadata'),
    'PluginParseError': ('xoneaiagents.plugins', 'PluginParseError'),
    'parse_plugin_header': ('xoneaiagents.plugins', 'parse_plugin_header'),
    'parse_plugin_header_from_file': ('xoneaiagents.plugins', 'parse_plugin_header_from_file'),
    'discover_plugins': ('xoneaiagents.plugins', 'discover_plugins'),
    'load_plugin': ('xoneaiagents.plugins', 'load_plugin'),
    'discover_and_load_plugins': ('xoneaiagents.plugins', 'discover_and_load_plugins'),
    'get_default_plugin_dirs': ('xoneaiagents.plugins', 'get_default_plugin_dirs'),
    'get_plugin_template': ('xoneaiagents.plugins', 'get_plugin_template'),
    'ensure_plugin_dir': ('xoneaiagents.plugins', 'ensure_plugin_dir'),
    
    # Config loader - for config-driven defaults
    'get_config': ('xoneaiagents.config.loader', 'get_config'),
    'get_default': ('xoneaiagents.config.loader', 'get_default'),
    'get_plugins_config': ('xoneaiagents.config.loader', 'get_plugins_config'),
    'get_defaults_config': ('xoneaiagents.config.loader', 'get_defaults_config'),
    'apply_config_defaults': ('xoneaiagents.config.loader', 'apply_config_defaults'),
    'validate_config': ('xoneaiagents.config.loader', 'validate_config'),
    'get_config_path': ('xoneaiagents.config.loader', 'get_config_path'),
    'ConfigValidationError': ('xoneaiagents.config.loader', 'ConfigValidationError'),
    'XoneConfig': ('xoneaiagents.config.loader', 'XoneConfig'),
    'PluginsConfig': ('xoneaiagents.config.loader', 'PluginsConfig'),
    'DefaultsConfig': ('xoneaiagents.config.loader', 'DefaultsConfig'),
}


def _custom_handler(name, cache):
    """Handle special cases that need custom logic."""
    import warnings
    
    # Agents is a silent alias for AgentManager
    if name == "Agents":
        value = lazy_import('xoneaiagents.agents.agents', 'AgentManager', cache)
        cache['AgentManager'] = value
        cache['Agents'] = value
        return value
    
    # Task removed in v4.0.0 - use Task instead
    if name == "Task":
        raise ImportError(
            "Task has been removed in v4.0.0. Use Task instead.\n"
            "Migration: Replace 'from xoneaiagents import Task' with 'from xoneaiagents import Task'\n"
            "Task supports all Task features including action, handler, loop_over, etc."
        )
    
    # Module imports (return the module itself)
    if name == 'memory':
        import importlib
        return importlib.import_module('.memory', 'xoneaiagents')
    if name == 'workflows':
        import importlib
        return importlib.import_module('.workflows', 'xoneaiagents')
    
    raise AttributeError(f"Not handled by custom_handler: {name}")


# ============================================================================
# SUBPACKAGE FUNCTION OVERRIDES
# ============================================================================
# Some subpackage names conflict with function names we want to export.
# Override them here to return the function instead of the module.
# ============================================================================

# Override 'embedding' to return the function, not the subpackage
from .embedding.embed import embedding as _embedding_func
embedding = _embedding_func

# Also provide embeddings alias
embeddings = _embedding_func


# Create the __getattr__ function using centralized utility
__getattr__ = create_lazy_getattr_with_fallback(
    mapping=_LAZY_IMPORTS,
    module_name=__name__,
    cache=_lazy_cache,
    fallback_modules=['tools', 'memory', 'config', 'workflows'],
    custom_handler=_custom_handler
)


# Initialize telemetry only if explicitly enabled via config
def _init_telemetry():
    """Initialize telemetry if enabled via environment variable."""
    if not _config.TELEMETRY_ENABLED:
        return
    
    try:
        from .telemetry import get_telemetry
        from .telemetry.integration import auto_instrument_all
        
        _telemetry = get_telemetry()
        if _telemetry and _telemetry.enabled:
            use_performance_mode = _config.PERFORMANCE_MODE and not (
                _config.FULL_TELEMETRY or _config.AUTO_INSTRUMENT
            )
            auto_instrument_all(_telemetry, performance_mode=use_performance_mode)
            
            # Track package import for basic usage analytics
            try:
                _telemetry.track_feature_usage("package_import")
            except Exception:
                pass
    except Exception:
        # Silently fail if there are any issues - never break user applications
        pass


# Only initialize telemetry if explicitly enabled
_init_telemetry()


def warmup(include_litellm: bool = False, include_openai: bool = True) -> dict:
    """
    Pre-import heavy dependencies to reduce first-call latency.
    
    NOTE: For default OpenAI usage (llm="gpt-4o-mini"), warmup is NOT needed.
    The default path uses the native OpenAI SDK which is fast (~100ms import).
    
    Warmup is only beneficial when using LiteLLM backend, which is triggered by:
    - Using "/" in model name (e.g., llm="openai/gpt-4o-mini")
    - Passing a dict config (e.g., llm={"model": "gpt-4o-mini"})
    - Using base_url parameter
    
    Args:
        include_litellm: Pre-import LiteLLM (~2-3s). Only needed for multi-provider support.
        include_openai: Pre-import OpenAI SDK (~100ms). Default path, usually fast.
    
    Returns:
        dict: Timing information for each component warmed up
    
    Example:
        # For LiteLLM multi-provider usage:
        from xoneaiagents import warmup
        warmup(include_litellm=True)  # Pre-load LiteLLM
        
        agent = Agent(llm="anthropic/claude-3-sonnet")  # Now faster
        
        # For default OpenAI usage, no warmup needed:
        agent = Agent(llm="gpt-4o-mini")  # Already fast!
    """
    import time
    timings = {}
    
    if include_openai:
        start = time.perf_counter()
        try:
            import openai
            timings['openai'] = (time.perf_counter() - start) * 1000
        except ImportError:
            timings['openai'] = -1  # Not available
    
    if include_litellm:
        start = time.perf_counter()
        try:
            import litellm
            # Also configure litellm to avoid first-call overhead
            litellm.telemetry = False
            litellm.set_verbose = False
            litellm.drop_params = True
            litellm.modify_params = True
            timings['litellm'] = (time.perf_counter() - start) * 1000
        except ImportError:
            timings['litellm'] = -1  # Not available
    
    return timings


# ============================================================================
# PUBLIC API: __all__ (controls IDE autocomplete and `from X import *`)
# ============================================================================
# DESIGN: Keep __all__ minimal for clean IDE experience.
# All 186+ symbols are still accessible via __getattr__ for backwards compat.
# Organized imports available via sub-packages: config, tools, memory, workflows
# ============================================================================

__all__ = [
    # Core classes - the essentials
    'Agent',
    'AgentTeam',  # Primary class for multi-agent coordination (v1.0+)
    'AgentManager',  # Silent alias for AgentTeam
    'Agents',  # Deprecated alias for AgentTeam (emits warning)
    'Task',
    
    # AgentFlow (deterministic pipelines)
    'AgentFlow',  # Primary class for workflows (v1.0+)
    'Workflow',  # Silent alias for AgentFlow
    'Pipeline',  # Silent alias for AgentFlow
    
    # AgentOS (production deployment protocols)
    'AgentOSProtocol',  # Primary protocol for deployment (v1.0+)
    'AgentOSConfig',  # Primary config for deployment (v1.0+)
    'AgentAppProtocol',  # Silent alias for AgentOSProtocol
    'AgentAppConfig',  # Silent alias for AgentOSConfig
    
    # Tool essentials
    'tool',
    'Tools',
    
    # Approval (agent-centric approval backends)
    'AutoApproveBackend',
    
    # Embedding API - simplified imports
    # Usage: from xoneaiagents import embedding, EmbeddingResult
    'embedding',
    'embeddings',  # Plural alias (OpenAI style)
    'aembedding',
    'aembeddings',  # Plural alias for async
    'EmbeddingResult',
    'get_dimensions',
    
    # Autonomy
    'AutonomyConfig',
    'AutonomyLevel',
    
    # Sub-packages for organized imports
    # Usage: import xoneaiagents as pa; pa.config.MemoryConfig
    'config',
    'tools',
    'memory',
    'workflows',
]


def __dir__():
    """
    Return clean list for dir() - matches __all__ plus standard attributes.
    
    This keeps IDE autocomplete clean while preserving full backwards
    compatibility via __getattr__ for all 186+ legacy exports.
    """
    return list(__all__) + [
        # Standard module attributes
        '__name__', '__doc__', '__file__', '__path__', '__package__',
        '__loader__', '__spec__', '__cached__', '__builtins__',
    ]


# ============================================================================
# BACKWARDS COMPATIBILITY: Legacy __all__ items (for reference)
# ============================================================================
# All items below are still importable via __getattr__ but NOT in autocomplete:
# - ImageAgent, ContextAgent, create_context_agent, XoneAIAgents
# - BaseTool, ToolResult, ToolValidationError, validate_tool, FunctionTool
# - ToolRegistry, get_registry, register_tool, get_tool
# - TaskOutput, ReflectionOutput, AutoAgents, AutoRagAgent, AutoRagConfig
# - Session, Memory, db, obs, Knowledge, Chunking
# - GuardrailResult, LLMGuardrail, Handoff, handoff, handoff_filters
# - MemoryConfig, KnowledgeConfig, PlanningConfig, OutputConfig, etc.
# - Workflow, Task, Route, Parallel, Loop, Repeat, Pipeline, etc.
# - MCP, FlowDisplay, track_workflow, FastContext, etc.
# - Plan, PlanStep, TodoList, PlanningAgent, ApprovalCallback, etc.
# - RAG, RAGConfig, RAGResult, AGUI, A2A, etc.
# - All telemetry, display, and utility functions
# ============================================================================
