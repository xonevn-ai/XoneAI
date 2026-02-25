"""
TDD tests for AgentOS-related exports.

Tests verify:
1. AgentOSProtocol is importable from root
2. AgentOSConfig is importable from root  
3. AgentAppProtocol is silent alias for AgentOSProtocol
4. AgentAppConfig is silent alias for AgentOSConfig
5. All are in __all__ for IDE autocomplete
"""

class TestAgentOSProtocolExports:
    """Test AgentOSProtocol exports from xoneaiagents."""
    
    def test_agent_os_protocol_importable_from_root(self):
        """AgentOSProtocol should be importable from xoneaiagents root."""
        from xoneaiagents import AgentOSProtocol
        assert AgentOSProtocol is not None
    
    def test_agent_os_protocol_is_protocol(self):
        """AgentOSProtocol should be a typing.Protocol."""
        from xoneaiagents import AgentOSProtocol
        # Check it's decorated with @runtime_checkable (Protocol has _is_protocol attr)
        assert hasattr(AgentOSProtocol, '__protocol_attrs__') or hasattr(AgentOSProtocol, '_is_protocol')
    
    def test_agent_app_protocol_is_alias(self):
        """AgentAppProtocol should be silent alias for AgentOSProtocol."""
        from xoneaiagents import AgentOSProtocol, AgentAppProtocol
        assert AgentAppProtocol is AgentOSProtocol
    
    def test_agent_os_protocol_from_app_module(self):
        """AgentOSProtocol should be importable from app module."""
        from xoneaiagents.app import AgentOSProtocol
        assert AgentOSProtocol is not None


class TestAgentOSConfigExports:
    """Test AgentOSConfig exports from xoneaiagents."""
    
    def test_agent_os_config_importable_from_root(self):
        """AgentOSConfig should be importable from xoneaiagents root."""
        from xoneaiagents import AgentOSConfig
        assert AgentOSConfig is not None
    
    def test_agent_app_config_is_alias(self):
        """AgentAppConfig should be silent alias for AgentOSConfig."""
        from xoneaiagents import AgentOSConfig, AgentAppConfig
        assert AgentAppConfig is AgentOSConfig
    
    def test_agent_os_config_from_app_module(self):
        """AgentOSConfig should be importable from app module."""
        from xoneaiagents.app import AgentOSConfig
        assert AgentOSConfig is not None


class TestAgentOSInAll:
    """Test that AgentOS symbols are in __all__ for IDE autocomplete."""
    
    def test_agent_os_protocol_in_all(self):
        """AgentOSProtocol should be in __all__."""
        import xoneaiagents
        assert 'AgentOSProtocol' in xoneaiagents.__all__
    
    def test_agent_os_config_in_all(self):
        """AgentOSConfig should be in __all__."""
        import xoneaiagents
        assert 'AgentOSConfig' in xoneaiagents.__all__
    
    def test_agent_app_protocol_in_all(self):
        """AgentAppProtocol should be in __all__ (silent alias)."""
        import xoneaiagents
        assert 'AgentAppProtocol' in xoneaiagents.__all__
    
    def test_agent_app_config_in_all(self):
        """AgentAppConfig should be in __all__ (silent alias)."""
        import xoneaiagents
        assert 'AgentAppConfig' in xoneaiagents.__all__


class TestNoDeprecationWarnings:
    """Test that AgentOS aliases are silent (no deprecation warnings)."""
    
    def test_agent_app_protocol_no_warning(self):
        """Importing AgentAppProtocol should not emit deprecation warning."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneaiagents import AgentAppProtocol
            _ = AgentAppProtocol
            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0, f"Got deprecation warnings: {deprecation_warnings}"
    
    def test_agent_app_config_no_warning(self):
        """Importing AgentAppConfig should not emit deprecation warning."""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from xoneaiagents import AgentAppConfig
            _ = AgentAppConfig
            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0, f"Got deprecation warnings: {deprecation_warnings}"
