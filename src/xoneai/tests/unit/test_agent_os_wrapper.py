"""
TDD tests for AgentOS exports from xoneai wrapper.

Tests verify:
1. AgentOS is importable from xoneai
2. AgentApp is silent alias for AgentOS (backward compat)
3. Both are in __all__
4. No deprecation warnings for AgentApp alias
"""


class TestAgentOSWrapperExports:
    """Test AgentOS exports from xoneai wrapper."""
    
    def test_agent_os_importable_from_wrapper(self):
        """AgentOS should be importable from xoneai."""
        from xoneai import AgentOS
        assert AgentOS is not None
    
    def test_agent_app_is_alias_for_agent_os(self):
        """AgentApp should be silent alias for AgentOS."""
        from xoneai import AgentOS, AgentApp
        assert AgentApp is AgentOS
    
    def test_agent_os_in_all(self):
        """AgentOS should be in __all__."""
        import xoneai
        assert 'AgentOS' in xoneai.__all__
    
    def test_agent_app_in_all(self):
        """AgentApp should be in __all__ (silent alias)."""
        import xoneai
        assert 'AgentApp' in xoneai.__all__


class TestAgentAppNoDeprecationWarning:
    """Test that AgentApp alias is silent (no deprecation warnings)."""
    
    def test_agent_app_no_warning(self):
        """Importing AgentApp should not emit deprecation warning."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneai import AgentApp
            _ = AgentApp
            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0, f"Got deprecation warnings: {deprecation_warnings}"
