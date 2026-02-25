"""
Tests for namespace package guard in xoneaiagents.

These tests verify that xoneaiagents properly detects when it's loaded
as a namespace package (which indicates stale artifacts in site-packages)
and provides helpful error messages.
"""

import pytest


class TestNamespaceGuard:
    """Tests for namespace package detection."""
    
    def test_xoneaiagents_has_file_attribute(self):
        """Verify xoneaiagents.__file__ is not None (not a namespace package)."""
        import xoneaiagents
        assert xoneaiagents.__file__ is not None, (
            "xoneaiagents.__file__ is None - this indicates it's loaded as a "
            "namespace package. Remove stale xoneaiagents directory from site-packages."
        )
    
    def test_xoneaiagents_has_init_py(self):
        """Verify xoneaiagents has a proper __init__.py."""
        import xoneaiagents
        import os
        
        # __file__ should point to __init__.py
        if xoneaiagents.__file__:
            assert xoneaiagents.__file__.endswith("__init__.py"), (
                f"Expected __init__.py, got {xoneaiagents.__file__}"
            )
            assert os.path.exists(xoneaiagents.__file__), (
                f"__init__.py does not exist at {xoneaiagents.__file__}"
            )
    
    def test_agent_import_succeeds(self):
        """Verify Agent can be imported from xoneaiagents."""
        from xoneaiagents import Agent
        assert Agent is not None
        assert hasattr(Agent, '__init__')
    
    def test_lazy_loading_works(self):
        """Verify lazy loading via __getattr__ works correctly."""
        import xoneaiagents
        
        # These should be lazy-loaded via __getattr__
        Agent = xoneaiagents.Agent
        assert Agent is not None
        
        # Verify it's cached
        Agent2 = xoneaiagents.Agent
        assert Agent is Agent2
    
    def test_package_spec_has_origin(self):
        """Verify the package spec has an origin (not a namespace package)."""
        import xoneaiagents
        
        spec = xoneaiagents.__spec__
        assert spec is not None, "Package has no __spec__"
        
        # Namespace packages have origin=None
        # Regular packages have origin pointing to __init__.py
        assert spec.origin is not None, (
            "Package spec.origin is None - this indicates a namespace package. "
            "Remove stale xoneaiagents directory from site-packages."
        )
    
    def test_submodule_search_locations_correct(self):
        """Verify submodule_search_locations points to source, not site-packages stale dir."""
        import xoneaiagents
        
        spec = xoneaiagents.__spec__
        locations = spec.submodule_search_locations
        
        assert locations is not None, "No submodule_search_locations"
        assert len(locations) > 0, "Empty submodule_search_locations"
        
        # Should NOT contain site-packages path without __init__.py
        for loc in locations:
            if "site-packages" in loc:
                import os
                init_path = os.path.join(loc, "__init__.py")
                # If it's in site-packages, it should have __init__.py
                # (this would be a proper install, not a stale namespace)
                if os.path.isdir(loc):
                    assert os.path.exists(init_path), (
                        f"Found stale namespace package at {loc} - "
                        "remove this directory to fix import issues"
                    )


class TestAgentImportIntegrity:
    """Tests for Agent class import integrity."""
    
    def test_agent_class_attributes(self):
        """Verify Agent class has expected attributes."""
        from xoneaiagents import Agent
        
        # Core attributes that should exist
        assert hasattr(Agent, '__init__')
        assert hasattr(Agent, 'start')
        assert hasattr(Agent, 'chat')
    
    def test_agents_class_import(self):
        """Verify Agents class can be imported (silent alias for AgentManager)."""
        from xoneaiagents import Agents
        assert Agents is not None
    
    def test_task_class_import(self):
        """Verify Task class can be imported."""
        from xoneaiagents import Task
        assert Task is not None
    
    def test_tool_decorator_import(self):
        """Verify tool decorator can be imported."""
        from xoneaiagents import tool
        assert tool is not None
        assert callable(tool)
    
    def test_tools_class_import(self):
        """Verify Tools class can be imported."""
        from xoneaiagents import Tools
        assert Tools is not None


class TestImportErrorMessages:
    """Tests for helpful error messages on import failures."""
    
    def test_import_error_is_informative(self):
        """Verify that import errors provide helpful information."""
        # This test documents expected behavior - if Agent import fails,
        # the error message should be informative
        try:
            from xoneaiagents import Agent
            # If we get here, import succeeded - that's good
            assert Agent is not None
        except ImportError as e:
            # If import fails, error should mention namespace package
            error_msg = str(e).lower()
            assert any(word in error_msg for word in [
                "namespace", "stale", "site-packages", "unknown location"
            ]), f"Import error should be informative, got: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
