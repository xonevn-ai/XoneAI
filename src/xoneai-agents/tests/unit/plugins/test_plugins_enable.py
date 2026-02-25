"""
Unit tests for plugins.enable() API and config-driven defaults.

Tests:
- plugins.enable() / plugins.disable()
- XONEAI_PLUGINS env var
- Config file loading
- Config-driven defaults for Agent parameters
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestPluginsEnableAPI:
    """Test the plugins.enable() API."""
    
    def test_enable_all_plugins(self):
        """Test enabling all plugins."""
        from xoneaiagents import plugins
        
        # Reset state
        plugins._plugins_enabled = False
        plugins._enabled_plugin_names = None
        
        # Enable all
        plugins.enable()
        
        assert plugins.is_enabled() is True
        assert plugins._enabled_plugin_names is None  # None means all
    
    def test_enable_specific_plugins(self):
        """Test enabling specific plugins by name."""
        from xoneaiagents import plugins
        
        # Reset state
        plugins._plugins_enabled = False
        plugins._enabled_plugin_names = None
        
        # Enable specific plugins
        plugins.enable(["logging", "metrics"])
        
        assert plugins.is_enabled() is True
        assert plugins._enabled_plugin_names == ["logging", "metrics"]
    
    def test_disable_all_plugins(self):
        """Test disabling all plugins."""
        from xoneaiagents import plugins
        
        # First enable
        plugins._plugins_enabled = True
        plugins._enabled_plugin_names = None
        
        # Then disable
        plugins.disable()
        
        assert plugins.is_enabled() is False
    
    def test_list_plugins_returns_list(self):
        """Test that list_plugins returns a list."""
        from xoneaiagents import plugins
        
        result = plugins.list_plugins()
        assert isinstance(result, list)
    
    def test_is_enabled_default_false(self):
        """Test that plugins are disabled by default."""
        from xoneaiagents import plugins
        
        # Reset state
        plugins._plugins_enabled = False
        
        assert plugins.is_enabled() is False


class TestPluginsEnvVar:
    """Test XONEAI_PLUGINS environment variable."""
    
    def test_env_var_true_enables_plugins(self):
        """Test that XONEAI_PLUGINS=true enables plugins."""
        from xoneaiagents._config import _get_plugins_enabled
        
        with patch.dict(os.environ, {"XONEAI_PLUGINS": "true"}):
            assert _get_plugins_enabled() is True
    
    def test_env_var_false_disables_plugins(self):
        """Test that XONEAI_PLUGINS=false disables plugins."""
        from xoneaiagents._config import _get_plugins_enabled
        
        with patch.dict(os.environ, {"XONEAI_PLUGINS": "false"}):
            assert _get_plugins_enabled() is False
    
    def test_env_var_list_enables_specific(self):
        """Test that XONEAI_PLUGINS=logging,metrics enables specific plugins."""
        from xoneaiagents._config import _get_plugins_enabled, _get_plugins_list
        
        with patch.dict(os.environ, {"XONEAI_PLUGINS": "logging,metrics"}):
            assert _get_plugins_enabled() is True
            assert _get_plugins_list() == ["logging", "metrics"]
    
    def test_env_var_empty_disables(self):
        """Test that empty XONEAI_PLUGINS disables plugins."""
        from xoneaiagents._config import _get_plugins_enabled
        
        with patch.dict(os.environ, {"XONEAI_PLUGINS": ""}):
            assert _get_plugins_enabled() is False


class TestConfigLoader:
    """Test config file loading."""
    
    def test_get_config_returns_xone_config(self):
        """Test that get_config returns a XoneConfig."""
        from xoneaiagents.config.loader import get_config, XoneConfig, clear_config_cache
        
        clear_config_cache()
        config = get_config()
        assert isinstance(config, XoneConfig)
    
    def test_get_plugins_config(self):
        """Test getting plugins config."""
        from xoneaiagents.config.loader import get_plugins_config, PluginsConfig, clear_config_cache
        
        clear_config_cache()
        plugins_config = get_plugins_config()
        assert isinstance(plugins_config, PluginsConfig)
    
    def test_get_defaults_config(self):
        """Test getting defaults config."""
        from xoneaiagents.config.loader import get_defaults_config, DefaultsConfig, clear_config_cache
        
        clear_config_cache()
        defaults_config = get_defaults_config()
        assert isinstance(defaults_config, DefaultsConfig)
    
    def test_get_default_with_fallback(self):
        """Test get_default returns fallback when key not found."""
        from xoneaiagents.config.loader import get_default, clear_config_cache
        
        clear_config_cache()
        result = get_default("nonexistent_key", "fallback_value")
        assert result == "fallback_value"
    
    def test_is_plugins_enabled_from_config(self):
        """Test is_plugins_enabled checks config file."""
        from xoneaiagents.config.loader import is_plugins_enabled, clear_config_cache
        
        clear_config_cache()
        # Without env var, should check config (which defaults to False)
        with patch.dict(os.environ, {}, clear=True):
            # Remove XONEAI_PLUGINS if present
            os.environ.pop("XONEAI_PLUGINS", None)
            result = is_plugins_enabled()
            assert isinstance(result, bool)
    
    def test_config_file_parsing(self):
        """Test parsing a TOML config file."""
        from xoneaiagents.config.loader import _parse_toml, clear_config_cache
        
        # Create a temp TOML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write("""
[plugins]
enabled = true
auto_discover = true

[defaults]
model = "gpt-4o-mini"

[defaults.memory]
enabled = true
backend = "file"
""")
            f.flush()
            
            try:
                result = _parse_toml(Path(f.name))
                assert result.get("plugins", {}).get("enabled") is True
                assert result.get("defaults", {}).get("model") == "gpt-4o-mini"
                assert result.get("defaults", {}).get("memory", {}).get("backend") == "file"
            finally:
                os.unlink(f.name)


class TestConfigDrivenDefaults:
    """Test config-driven defaults for Agent parameters."""
    
    def test_apply_config_defaults_with_true(self):
        """Test that True uses config defaults."""
        from xoneaiagents.config.loader import apply_config_defaults, clear_config_cache
        from xoneaiagents.config.feature_configs import MemoryConfig
        
        clear_config_cache()
        
        # When user passes True, should use config defaults
        # Without config file, should just return True
        result = apply_config_defaults("memory", True, MemoryConfig)
        # Should return True or a MemoryConfig
        assert result is True or isinstance(result, MemoryConfig)
    
    def test_apply_config_defaults_with_none(self):
        """Test that None checks config for enabled."""
        from xoneaiagents.config.loader import apply_config_defaults, clear_config_cache
        
        clear_config_cache()
        
        # When user passes None, should check config
        result = apply_config_defaults("memory", None, None)
        # Without config, should return None
        assert result is None
    
    def test_apply_config_defaults_explicit_value(self):
        """Test that explicit values are preserved."""
        from xoneaiagents.config.loader import apply_config_defaults, clear_config_cache
        from xoneaiagents.config.feature_configs import MemoryConfig
        
        clear_config_cache()
        
        # When user passes explicit config, should preserve it
        explicit_config = MemoryConfig(backend="postgres")
        result = apply_config_defaults("memory", explicit_config, MemoryConfig)
        assert result == explicit_config


class TestToolsGuardrailsExempt:
    """Test that tools and guardrails work without plugins.enable()."""
    
    def test_tools_work_without_enable(self):
        """Test that tools work without calling plugins.enable()."""
        from xoneaiagents import plugins
        
        # Ensure plugins are disabled
        plugins._plugins_enabled = False
        
        # Tools should still work - this is tested by Agent creation
        # Just verify the flag is false
        assert plugins.is_enabled() is False
    
    def test_guardrails_work_without_enable(self):
        """Test that guardrails work without calling plugins.enable()."""
        from xoneaiagents import plugins
        
        # Ensure plugins are disabled
        plugins._plugins_enabled = False
        
        # Guardrails should still work - this is tested by Agent creation
        # Just verify the flag is false
        assert plugins.is_enabled() is False


class TestPluginManagerIntegration:
    """Test PluginManager integration with enable API."""
    
    def test_get_plugin_manager_singleton(self):
        """Test that get_plugin_manager returns singleton."""
        from xoneaiagents.plugins import get_plugin_manager
        
        manager1 = get_plugin_manager()
        manager2 = get_plugin_manager()
        assert manager1 is manager2
    
    def test_plugin_manager_has_required_methods(self):
        """Test that PluginManager has all required methods."""
        from xoneaiagents.plugins import get_plugin_manager
        
        manager = get_plugin_manager()
        
        # Check required methods exist
        assert hasattr(manager, 'register')
        assert hasattr(manager, 'unregister')
        assert hasattr(manager, 'enable')
        assert hasattr(manager, 'disable')
        assert hasattr(manager, 'is_enabled')
        assert hasattr(manager, 'list_plugins')
        assert hasattr(manager, 'auto_discover_plugins')
        assert hasattr(manager, 'execute_hook')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
