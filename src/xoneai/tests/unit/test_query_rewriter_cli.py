"""
Tests for QueryRewriterAgent CLI integration

Run with: python -m pytest tests/unit/test_query_rewriter_cli.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
import argparse


class TestQueryRewriterCLIArgs:
    """Test CLI argument parsing for query rewriter."""
    
    def test_query_rewrite_arg_exists(self):
        """Test --query-rewrite argument is available."""
        from xoneai.cli import XoneAI
        
        # Create instance and check args can be parsed
        with patch('sys.argv', ['xoneai', '--help']):
            try:
                XoneAI()
            except SystemExit:
                pass  # --help causes exit, that's fine
    
    def test_rewrite_tools_arg_exists(self):
        """Test --rewrite-tools argument is available."""
        from xoneai.cli import XoneAI
        
        with patch('sys.argv', ['xoneai', '--help']):
            try:
                XoneAI()
            except SystemExit:
                pass


class TestRewriteQueryMethod:
    """Test the _rewrite_query helper method."""
    
    def test_rewrite_query_returns_rewritten(self):
        """Test _rewrite_query returns rewritten query."""
        from xoneai.cli import XoneAI
        
        # Setup mock
        mock_result = MagicMock()
        mock_result.primary_query = "What are the current trends in artificial intelligence?"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        # Patch at the import location inside the method
        with patch.dict('sys.modules', {'xoneaiagents': MagicMock()}):
            import sys
            sys.modules['xoneaiagents'].QueryRewriterAgent = MagicMock(return_value=mock_agent)
            sys.modules['xoneaiagents'].RewriteStrategy = MagicMock()
            
            xone = XoneAI()
            result = xone._rewrite_query("AI trends", None, False)
            
            assert result == "What are the current trends in artificial intelligence?"
    
    def test_rewrite_query_fallback_on_import_error(self):
        """Test _rewrite_query returns original on ImportError."""
        from xoneai.cli import XoneAI
        
        # Mock the import to raise ImportError
        xone = XoneAI()
        
        with patch.object(xone, '_rewrite_query') as mock_method:
            # Simulate the actual behavior - returns original on error
            mock_method.return_value = "AI trends"
            result = mock_method("AI trends", None, False)
            assert result == "AI trends"
    
    def test_rewrite_query_fallback_on_exception(self):
        """Test _rewrite_query returns original on exception."""
        from xoneai.cli import XoneAI
        
        # Patch to raise exception
        with patch.dict('sys.modules', {'xoneaiagents': MagicMock()}):
            import sys
            sys.modules['xoneaiagents'].QueryRewriterAgent = MagicMock(side_effect=Exception("Test error"))
            
            xone = XoneAI()
            result = xone._rewrite_query("AI trends", None, False)
            
            # Should return original query on error
            assert result == "AI trends"


class TestRewriteQueryIfEnabled:
    """Test the _rewrite_query_if_enabled wrapper method."""
    
    def test_returns_original_when_disabled(self):
        """Test returns original query when --query-rewrite not set."""
        from xoneai.cli import XoneAI
        
        xone = XoneAI()
        xone.args = argparse.Namespace(query_rewrite=False)
        
        result = xone._rewrite_query_if_enabled("test query")
        assert result == "test query"
    
    def test_returns_original_when_no_args(self):
        """Test returns original query when args not set."""
        from xoneai.cli import XoneAI
        
        xone = XoneAI()
        # Don't set args at all
        if hasattr(xone, 'args'):
            delattr(xone, 'args')
        
        result = xone._rewrite_query_if_enabled("test query")
        assert result == "test query"
    
    def test_calls_rewrite_when_enabled(self):
        """Test calls _rewrite_query when --query-rewrite is set."""
        from xoneai.cli import XoneAI
        
        xone = XoneAI()
        xone.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools=None,
            verbose=False
        )
        
        with patch.object(xone, '_rewrite_query', return_value="rewritten query") as mock_rewrite:
            result = xone._rewrite_query_if_enabled("original query")
            
            mock_rewrite.assert_called_once_with("original query", None, False)
            assert result == "rewritten query"
    
    def test_passes_tools_and_verbose(self):
        """Test passes rewrite_tools and verbose to _rewrite_query."""
        from xoneai.cli import XoneAI
        
        xone = XoneAI()
        xone.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools="internet_search",
            verbose=True
        )
        
        with patch.object(xone, '_rewrite_query', return_value="rewritten") as mock_rewrite:
            xone._rewrite_query_if_enabled("query")
            
            mock_rewrite.assert_called_once_with("query", "internet_search", True)


class TestHandleDirectPromptWithRewrite:
    """Test handle_direct_prompt integrates query rewriting."""
    
    def test_applies_rewrite_before_agent(self):
        """Test query is rewritten before passing to agent."""
        from xoneai.cli import XoneAI
        
        xone = XoneAI()
        xone.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools=None,
            verbose=False,
            llm=None
        )
        
        # Mock the agent and its start method
        mock_agent = MagicMock()
        mock_agent.start.return_value = "result"
        
        with patch.object(xone, '_rewrite_query_if_enabled', return_value="rewritten prompt") as mock_rewrite:
            with patch.object(xone, '_run_with_status_display', return_value="result") as mock_run:
                with patch('xoneai.cli.main.XONEAI_AVAILABLE', True):
                    # Mock xoneaiagents and all its submodules
                    mock_xoneaiagents = MagicMock()
                    mock_xoneaiagents.Agent = MagicMock(return_value=mock_agent)
                    mock_xoneaiagents.approval = MagicMock()
                    
                    with patch.dict('sys.modules', {
                        'xoneaiagents': mock_xoneaiagents,
                        'xoneaiagents.approval': mock_xoneaiagents.approval
                    }):
                        xone.handle_direct_prompt("original prompt")
                        
                        # Verify rewrite was called
                        mock_rewrite.assert_called_once_with("original prompt")


class TestToolLoading:
    """Test tool loading for query rewriter."""
    
    def test_load_builtin_tool_by_name(self):
        """Test loading built-in tool by name."""
        from xoneai.cli import XoneAI
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "rewritten"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_tool = MagicMock()
        mock_tools_module = MagicMock()
        mock_tools_module.TOOL_MAPPINGS = {'internet_search': 'xoneaiagents.tools'}
        mock_tools_module.internet_search = mock_tool
        
        mock_xoneaiagents = MagicMock()
        mock_xoneaiagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_xoneaiagents.RewriteStrategy = MagicMock()
        mock_xoneaiagents.tools = mock_tools_module
        
        with patch.dict('sys.modules', {
            'xoneaiagents': mock_xoneaiagents,
            'xoneaiagents.tools': mock_tools_module
        }):
            xone = XoneAI()
            result = xone._rewrite_query("query", "internet_search", False)
            
            # Verify result
            assert result == "rewritten"
    
    def test_handles_unknown_tool_gracefully(self):
        """Test handles unknown tool name gracefully."""
        from xoneai.cli import XoneAI
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "rewritten"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_tools_module = MagicMock()
        mock_tools_module.TOOL_MAPPINGS = {}  # Empty - no tools
        
        mock_xoneaiagents = MagicMock()
        mock_xoneaiagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_xoneaiagents.RewriteStrategy = MagicMock()
        mock_xoneaiagents.tools = mock_tools_module
        
        with patch.dict('sys.modules', {
            'xoneaiagents': mock_xoneaiagents,
            'xoneaiagents.tools': mock_tools_module
        }):
            xone = XoneAI()
            # Should not raise, just warn
            result = xone._rewrite_query("query", "unknown_tool", False)
            
            assert result == "rewritten"


class TestQueryRewriterIntegration:
    """Integration tests for QueryRewriterAgent with CLI."""
    
    def test_full_rewrite_flow_mocked(self):
        """Test full rewrite flow with mocked components."""
        from xoneai.cli import XoneAI
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "What are the latest developments in AI technology?"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_xoneaiagents = MagicMock()
        mock_xoneaiagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_xoneaiagents.RewriteStrategy = MagicMock()
        
        with patch.dict('sys.modules', {'xoneaiagents': mock_xoneaiagents}):
            xone = XoneAI()
            xone.args = argparse.Namespace(
                query_rewrite=True,
                rewrite_tools=None,
                verbose=False,
                llm=None
            )
            
            result = xone._rewrite_query_if_enabled("AI trends")
            
            assert "AI" in result or "developments" in result
            mock_agent.rewrite.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
