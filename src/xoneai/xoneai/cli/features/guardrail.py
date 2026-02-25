"""
Guardrail Handler for CLI.

Provides output validation using LLM guardrails.
Usage: xoneai "prompt" --guardrail "Ensure output is valid JSON"
"""

from typing import Any, Dict, Tuple
from .base import FlagHandler

# Lazy import to avoid performance impact
XONEAI_AVAILABLE = False
LLMGuardrail = None

def _check_xoneai():
    """Check if xoneaiagents is available."""
    global XONEAI_AVAILABLE, LLMGuardrail
    try:
        from xoneaiagents import LLMGuardrail as _LLMGuardrail
        LLMGuardrail = _LLMGuardrail
        XONEAI_AVAILABLE = True
    except ImportError:
        XONEAI_AVAILABLE = False
    return XONEAI_AVAILABLE


class GuardrailHandler(FlagHandler):
    """
    Handler for --guardrail flag.
    
    Validates agent output using LLM-based guardrails.
    
    Example:
        xoneai "Write code" --guardrail "Ensure code is secure"
    """
    
    @property
    def feature_name(self) -> str:
        return "guardrail"
    
    @property
    def flag_name(self) -> str:
        return "guardrail"
    
    @property
    def flag_help(self) -> str:
        return "Validate output with LLM guardrail (provide description string)"
    
    def check_dependencies(self) -> Tuple[bool, str]:
        """Check if xoneaiagents is available."""
        if _check_xoneai():
            return True, ""
        return False, "xoneaiagents not installed. Install with: pip install xoneaiagents"
    
    def apply_to_agent_config(self, config: Dict[str, Any], flag_value: Any) -> Dict[str, Any]:
        """
        Apply guardrail configuration to agent config.
        
        Args:
            config: Agent configuration dictionary
            flag_value: Guardrail description string
            
        Returns:
            Modified configuration with guardrail settings
        """
        if flag_value:
            config["guardrail_description"] = flag_value
            # Store for later use in post_process_result
            self._guardrail_description = flag_value
        return config
    
    def create_guardrail(self, description: str, llm: Any = None):
        """
        Create an LLMGuardrail instance.
        
        Args:
            description: Natural language description of validation criteria
            llm: Optional LLM instance for validation (defaults to gpt-4o-mini)
            
        Returns:
            LLMGuardrail instance or None if unavailable
        """
        if not _check_xoneai():
            self.print_status(
                "Guardrail requires xoneaiagents. Install with: pip install xoneaiagents",
                "error"
            )
            return None
        
        # Provide default LLM if none specified
        if llm is None:
            import os
            # Try to get from environment or use default
            llm = os.environ.get('OPENAI_MODEL_NAME', 'gpt-4o-mini')
        
        return LLMGuardrail(description=description, llm=llm)
    
    def validate_output(self, output: str, description: str, llm: Any = None) -> Tuple[bool, str]:
        """
        Validate output against guardrail criteria.
        
        Args:
            output: The output to validate
            description: Validation criteria description
            llm: Optional LLM for validation
            
        Returns:
            Tuple of (is_valid, message)
        """
        guardrail = self.create_guardrail(description, llm)
        if not guardrail:
            return True, "Guardrail unavailable, skipping validation"
        
        try:
            # Create a mock TaskOutput for the guardrail
            from xoneaiagents import TaskOutput
            task_output = TaskOutput(
                description="CLI output",
                summary="CLI output",
                raw=output,
                agent="CLI",
                output_format="RAW"
            )
            
            success, result = guardrail(task_output)
            if success:
                return True, "Guardrail validation passed"
            else:
                return False, f"Guardrail validation failed: {result}"
        except Exception as e:
            self.log(f"Guardrail error: {e}", "warning")
            return True, f"Guardrail error (skipped): {e}"
    
    def post_process_result(self, result: Any, flag_value: Any) -> Any:
        """
        Post-process result with guardrail validation.
        
        Args:
            result: Agent output
            flag_value: Guardrail description
            
        Returns:
            Original result (validation is logged)
        """
        if not flag_value:
            return result
        
        is_valid, message = self.validate_output(str(result), flag_value)
        
        if is_valid:
            self.print_status(f"✅ {message}", "success")
        else:
            self.print_status(f"⚠️ {message}", "warning")
        
        return result
    
    def execute(self, output: str = None, guardrail_description: str = None, **kwargs) -> Tuple[bool, str]:
        """
        Execute guardrail validation.
        
        Args:
            output: Output to validate
            guardrail_description: Validation criteria
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not output or not guardrail_description:
            return True, "No output or description provided"
        
        return self.validate_output(output, guardrail_description)
