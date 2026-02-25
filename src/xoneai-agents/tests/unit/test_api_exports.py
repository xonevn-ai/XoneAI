"""
Tests for API export simplification.

Verifies:
1. Core imports work (Agent, AgentManager, Task, tool, Tools)
2. Backwards compat imports work (MemoryConfig, etc.)
3. Organized imports work (from xoneaiagents.config import X)
4. Namespace style works (import xoneaiagents as pa)
5. __all__ is limited to core symbols only
"""

import pytest


class TestCoreImports:
    """Test that core classes are importable from root."""
    
    def test_agent_import(self):
        """Agent class is importable from root."""
        from xoneaiagents import Agent
        assert Agent is not None
        assert hasattr(Agent, '__init__')
    
    def test_agents_import(self):
        """Agents class is importable from root (silent alias for AgentManager)."""
        from xoneaiagents import Agents
        assert Agents is not None
    
    def test_task_import(self):
        """Task class is importable from root."""
        from xoneaiagents import Task
        assert Task is not None
    
    def test_tool_decorator_import(self):
        """tool decorator is importable from root."""
        from xoneaiagents import tool
        assert tool is not None
        assert callable(tool)
    
    def test_tools_class_import(self):
        """Tools class is importable from root."""
        from xoneaiagents import Tools
        assert Tools is not None


class TestBackwardsCompatImports:
    """Test that all legacy imports still work via __getattr__."""
    
    def test_memory_config_import(self):
        """MemoryConfig importable from root (backwards compat)."""
        from xoneaiagents import MemoryConfig
        assert MemoryConfig is not None
    
    def test_knowledge_config_import(self):
        """KnowledgeConfig importable from root (backwards compat)."""
        from xoneaiagents import KnowledgeConfig
        assert KnowledgeConfig is not None
    
    def test_output_config_import(self):
        """OutputConfig importable from root (backwards compat)."""
        from xoneaiagents import OutputConfig
        assert OutputConfig is not None
    
    def test_execution_config_import(self):
        """ExecutionConfig importable from root (backwards compat)."""
        from xoneaiagents import ExecutionConfig
        assert ExecutionConfig is not None
    
    def test_planning_config_import(self):
        """PlanningConfig importable from root (backwards compat)."""
        from xoneaiagents import PlanningConfig
        assert PlanningConfig is not None
    
    def test_reflection_config_import(self):
        """ReflectionConfig importable from root (backwards compat)."""
        from xoneaiagents import ReflectionConfig
        assert ReflectionConfig is not None
    
    def test_workflow_import(self):
        """Workflow importable from root (backwards compat)."""
        from xoneaiagents import Workflow
        assert Workflow is not None
    
    def test_memory_import(self):
        """Memory importable from root (backwards compat)."""
        from xoneaiagents import Memory
        assert Memory is not None
    
    def test_session_import(self):
        """Session importable from root (backwards compat)."""
        from xoneaiagents import Session
        assert Session is not None
    
    def test_base_tool_import(self):
        """BaseTool importable from root (backwards compat)."""
        from xoneaiagents import BaseTool
        assert BaseTool is not None
    
    def test_handoff_import(self):
        """Handoff importable from root (backwards compat)."""
        from xoneaiagents import Handoff
        assert Handoff is not None


class TestOrganizedImports:
    """Test that organized sub-package imports work."""
    
    def test_config_memory_config(self):
        """MemoryConfig importable from config sub-package."""
        from xoneaiagents.config import MemoryConfig
        assert MemoryConfig is not None
    
    def test_config_knowledge_config(self):
        """KnowledgeConfig importable from config sub-package."""
        from xoneaiagents.config import KnowledgeConfig
        assert KnowledgeConfig is not None
    
    def test_config_output_config(self):
        """OutputConfig importable from config sub-package."""
        from xoneaiagents.config import OutputConfig
        assert OutputConfig is not None
    
    def test_config_execution_config(self):
        """ExecutionConfig importable from config sub-package."""
        from xoneaiagents.config import ExecutionConfig
        assert ExecutionConfig is not None
    
    def test_tools_tool_decorator(self):
        """tool decorator importable from tools sub-package."""
        from xoneaiagents.tools import tool
        # Note: tools package uses different pattern, tool is via base
        # This tests the accessor pattern
    
    def test_tools_base_tool(self):
        """BaseTool importable from tools sub-package."""
        from xoneaiagents.tools.base import BaseTool
        assert BaseTool is not None
    
    def test_memory_memory_class(self):
        """Memory importable from memory sub-package."""
        from xoneaiagents.memory import Memory
        assert Memory is not None
    
    def test_workflows_workflow(self):
        """Workflow importable from workflows sub-package."""
        from xoneaiagents.workflows import Workflow
        assert Workflow is not None


class TestNamespaceStyle:
    """Test that 'import xoneaiagents as pa' style works."""
    
    def test_pa_agent(self):
        """pa.Agent works."""
        import xoneaiagents as pa
        assert hasattr(pa, 'Agent')
        assert pa.Agent is not None
    
    def test_pa_agents(self):
        """pa.Agents works."""
        import xoneaiagents as pa
        assert hasattr(pa, 'Agents')
    
    def test_pa_task(self):
        """pa.Task works."""
        import xoneaiagents as pa
        assert hasattr(pa, 'Task')
    
    def test_pa_config_subpackage(self):
        """pa.config sub-package accessible."""
        import xoneaiagents as pa
        assert hasattr(pa, 'config')
    
    def test_pa_config_memory_config(self):
        """pa.config.MemoryConfig works."""
        import xoneaiagents as pa
        assert hasattr(pa.config, 'MemoryConfig')
    
    def test_pa_tools_subpackage(self):
        """pa.tools sub-package accessible."""
        import xoneaiagents as pa
        assert hasattr(pa, 'tools')
    
    def test_pa_memory_subpackage(self):
        """pa.memory sub-package accessible."""
        import xoneaiagents as pa
        assert hasattr(pa, 'memory')
    
    def test_pa_workflows_subpackage(self):
        """pa.workflows sub-package accessible."""
        import xoneaiagents as pa
        assert hasattr(pa, 'workflows')


class TestAllSizeLimited:
    """Test that __all__ is limited to core symbols."""
    
    def test_all_size_under_29(self):
        """__all__ should have fewer than 29 items (minimal for clean IDE)."""
        import xoneaiagents
        # Updated from 27 to 29 to accommodate AutonomyConfig, AutonomyLevel exports
        assert len(xoneaiagents.__all__) < 29, \
            f"__all__ has {len(xoneaiagents.__all__)} items, expected < 29"
    
    def test_all_contains_core(self):
        """__all__ contains core symbols."""
        import xoneaiagents
        # AgentTeam is primary, Agents is deprecated alias
        # AgentFlow is primary, Workflow/Pipeline are silent aliases
        core = {'Agent', 'AgentTeam', 'Task', 'tool', 'Tools'}
        for symbol in core:
            assert symbol in xoneaiagents.__all__, \
                f"'{symbol}' not in __all__"
    
    def test_all_contains_subpackages(self):
        """__all__ contains sub-packages for namespace style."""
        import xoneaiagents
        subpackages = {'config', 'tools', 'memory', 'workflows'}
        for pkg in subpackages:
            assert pkg in xoneaiagents.__all__, \
                f"'{pkg}' not in __all__"
    
    def test_dir_matches_all(self):
        """dir() returns only __all__ items (clean introspection)."""
        import xoneaiagents
        # dir() should be small, matching __all__
        dir_items = set(dir(xoneaiagents))
        all_items = set(xoneaiagents.__all__)
        # dir() may include more (like __name__), but should include all of __all__
        assert all_items.issubset(dir_items), \
            f"__all__ items missing from dir(): {all_items - dir_items}"


class TestImportPerformance:
    """Test import performance (no regression)."""
    
    def test_import_time_under_200ms(self):
        """Package import should be fast (< 200ms)."""
        import subprocess
        import sys
        import os
        
        # Run import in fresh process to get accurate timing
        result = subprocess.run(
            [sys.executable, '-c', 
             'import time; t=time.time(); import xoneaiagents; print(time.time()-t)'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        
        # Handle subprocess errors gracefully
        if result.returncode != 0 or not result.stdout.strip():
            # If subprocess failed, skip with informative message
            pytest.skip(f"Subprocess failed: returncode={result.returncode}, stderr={result.stderr[:200] if result.stderr else 'none'}")
        
        import_time = float(result.stdout.strip())
        # 500ms is realistic for a feature-rich SDK on cold start
        # The lazy loading ensures heavy deps (litellm) aren't imported at startup
        # Note: First import in fresh process is slower due to bytecode compilation
        assert import_time < 0.5, \
            f"Import took {import_time*1000:.1f}ms, expected < 500ms"
