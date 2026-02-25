"""
Hooks Module for XoneAI Agents.

Provides a powerful hook system for intercepting and modifying agent behavior
at various lifecycle points. Unlike callbacks (which are for UI events),
hooks can intercept, modify, or block tool execution.

Features:
- Event-based hook system (BeforeTool, AfterTool, BeforeAgent, etc.)
- Shell command hooks for external integrations
- Python function hooks for in-process customization
- Matcher patterns for selective hook execution
- Sequential and parallel hook execution
- Decision outcomes (allow, deny, block, ask)

Zero Performance Impact:
- All imports are lazy loaded via centralized _lazy.py utility
- Hooks only execute when registered
- No overhead when hooks are disabled

Usage:
    from xoneaiagents.hooks import HookRegistry, HookEvent
    
    # Register a Python function hook
    registry = HookRegistry()
    
    @registry.on(HookEvent.BEFORE_TOOL)
    def my_hook(event_data):
        if event_data.tool_name == "dangerous_tool":
            return HookResult(decision="deny", reason="Tool blocked by policy")
        return HookResult(decision="allow")
    
    # Register a shell command hook
    registry.register_command_hook(
        event=HookEvent.BEFORE_TOOL,
        command="python /path/to/validator.py",
        matcher="write_*"  # Only match tools starting with write_
    )
    
    # Use with Agent
    agent = Agent(
        name="MyAgent",
        hooks=registry
    )
"""

from .._lazy import create_lazy_getattr_with_groups

__all__ = [
    # Core types
    "HookEvent",
    "HookDecision",
    "HookResult",
    "HookInput",
    "HookOutput",
    # Hook definitions
    "HookDefinition",
    "CommandHook",
    "FunctionHook",
    # Registry and runner
    "HookRegistry",
    "HookRunner",
    # Event-specific inputs
    "BeforeToolInput",
    "AfterToolInput",
    "BeforeAgentInput",
    "AfterAgentInput",
    "BeforeLLMInput",
    "AfterLLMInput",
    "SessionStartInput",
    "SessionEndInput",
    "OnErrorInput",
    "OnRetryInput",
    # Message lifecycle event inputs
    "MessageReceivedInput",
    "MessageSendingInput",
    "MessageSentInput",
    # Middleware types
    "InvocationContext",
    "ModelRequest",
    "ModelResponse",
    "ToolRequest",
    "ToolResponse",
    # Middleware decorators
    "before_model",
    "after_model",
    "wrap_model_call",
    "before_tool",
    "after_tool",
    "wrap_tool_call",
    # Middleware utilities
    "MiddlewareChain",
    "AsyncMiddlewareChain",
    "MiddlewareManager",
    # Verification hooks (protocols)
    "VerificationHook",
    "VerificationResult",
    # Simplified API (beginner-friendly)
    "add_hook",
    "remove_hook",
    "has_hook",
    "get_default_registry",
]

# Grouped lazy imports for DRY and efficient loading
# When one attribute from a group is accessed, all are loaded together
_LAZY_GROUPS = {
    'types_core': {
        'HookEvent': ('xoneaiagents.hooks.types', 'HookEvent'),
        'HookDecision': ('xoneaiagents.hooks.types', 'HookDecision'),
        'HookResult': ('xoneaiagents.hooks.types', 'HookResult'),
        'HookInput': ('xoneaiagents.hooks.types', 'HookInput'),
        'HookOutput': ('xoneaiagents.hooks.types', 'HookOutput'),
    },
    'types_definitions': {
        'HookDefinition': ('xoneaiagents.hooks.types', 'HookDefinition'),
        'CommandHook': ('xoneaiagents.hooks.types', 'CommandHook'),
        'FunctionHook': ('xoneaiagents.hooks.types', 'FunctionHook'),
    },
    'registry': {
        'HookRegistry': ('xoneaiagents.hooks.registry', 'HookRegistry'),
    },
    'runner': {
        'HookRunner': ('xoneaiagents.hooks.runner', 'HookRunner'),
    },
    'events': {
        'BeforeToolInput': ('xoneaiagents.hooks.events', 'BeforeToolInput'),
        'AfterToolInput': ('xoneaiagents.hooks.events', 'AfterToolInput'),
        'BeforeAgentInput': ('xoneaiagents.hooks.events', 'BeforeAgentInput'),
        'AfterAgentInput': ('xoneaiagents.hooks.events', 'AfterAgentInput'),
        'BeforeLLMInput': ('xoneaiagents.hooks.events', 'BeforeLLMInput'),
        'AfterLLMInput': ('xoneaiagents.hooks.events', 'AfterLLMInput'),
        'SessionStartInput': ('xoneaiagents.hooks.events', 'SessionStartInput'),
        'SessionEndInput': ('xoneaiagents.hooks.events', 'SessionEndInput'),
        'OnErrorInput': ('xoneaiagents.hooks.events', 'OnErrorInput'),
        'OnRetryInput': ('xoneaiagents.hooks.events', 'OnRetryInput'),
        'MessageReceivedInput': ('xoneaiagents.hooks.events', 'MessageReceivedInput'),
        'MessageSendingInput': ('xoneaiagents.hooks.events', 'MessageSendingInput'),
        'MessageSentInput': ('xoneaiagents.hooks.events', 'MessageSentInput'),
    },
    'middleware_types': {
        'InvocationContext': ('xoneaiagents.hooks.middleware', 'InvocationContext'),
        'ModelRequest': ('xoneaiagents.hooks.middleware', 'ModelRequest'),
        'ModelResponse': ('xoneaiagents.hooks.middleware', 'ModelResponse'),
        'ToolRequest': ('xoneaiagents.hooks.middleware', 'ToolRequest'),
        'ToolResponse': ('xoneaiagents.hooks.middleware', 'ToolResponse'),
    },
    'middleware_decorators': {
        'before_model': ('xoneaiagents.hooks.middleware', 'before_model'),
        'after_model': ('xoneaiagents.hooks.middleware', 'after_model'),
        'wrap_model_call': ('xoneaiagents.hooks.middleware', 'wrap_model_call'),
        'before_tool': ('xoneaiagents.hooks.middleware', 'before_tool'),
        'after_tool': ('xoneaiagents.hooks.middleware', 'after_tool'),
        'wrap_tool_call': ('xoneaiagents.hooks.middleware', 'wrap_tool_call'),
    },
    'middleware_utilities': {
        'MiddlewareChain': ('xoneaiagents.hooks.middleware', 'MiddlewareChain'),
        'AsyncMiddlewareChain': ('xoneaiagents.hooks.middleware', 'AsyncMiddlewareChain'),
        'MiddlewareManager': ('xoneaiagents.hooks.middleware', 'MiddlewareManager'),
    },
    'verification': {
        'VerificationHook': ('xoneaiagents.hooks.verification', 'VerificationHook'),
        'VerificationResult': ('xoneaiagents.hooks.verification', 'VerificationResult'),
    },
    # Simplified API (beginner-friendly aliases)
    'simplified_api': {
        'add_hook': ('xoneaiagents.hooks.registry', 'add_hook'),
        'remove_hook': ('xoneaiagents.hooks.registry', 'remove_hook'),
        'has_hook': ('xoneaiagents.hooks.registry', 'has_hook'),
        'get_default_registry': ('xoneaiagents.hooks.registry', 'get_default_registry'),
    },
}

# Create the __getattr__ function using centralized utility
__getattr__ = create_lazy_getattr_with_groups(_LAZY_GROUPS, __name__)
