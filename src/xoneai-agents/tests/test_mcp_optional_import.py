"""
Test that MCP module imports are optional and don't break basic functionality.
This test verifies the fix for issue #1091.
"""
import pytest


class TestMCPOptionalImport:
    """Test that MCP is properly optional."""

    def test_xoneaiagents_import_without_mcp(self):
        """Test that xoneaiagents can be imported without mcp installed."""
        # This should not raise any ImportError
        import xoneaiagents
        assert xoneaiagents is not None

    def test_agent_import_without_mcp(self):
        """Test that Agent can be imported without mcp installed."""
        from xoneaiagents import Agent
        assert Agent is not None

    def test_mcp_lazy_loading(self):
        """Test that MCP is lazily loaded."""
        from xoneaiagents import MCP  # noqa: F401
        # MCP should either be available or None (not raise ImportError on access)
        # The actual ImportError should only be raised when trying to instantiate
        # if mcp package is not installed

    def test_mcp_module_import_no_crash(self):
        """Test that mcp module can be imported without crashing."""
        # This tests that the try/except in mcp.py works correctly
        try:
            from xoneaiagents.mcp import mcp as mcp_module
            assert hasattr(mcp_module, 'MCP_AVAILABLE')
        except ImportError:
            # If import fails, it should be because of missing mcp,
            # not because of a syntax error
            pass

    def test_mcp_sse_module_import_no_crash(self):
        """Test that mcp_sse module can be imported without crashing."""
        try:
            from xoneaiagents.mcp import mcp_sse
            assert hasattr(mcp_sse, 'MCP_AVAILABLE')
        except ImportError:
            pass

    def test_mcp_http_stream_module_import_no_crash(self):
        """Test that mcp_http_stream module can be imported without crashing."""
        try:
            from xoneaiagents.mcp import mcp_http_stream
            assert hasattr(mcp_http_stream, 'MCP_AVAILABLE')
        except ImportError:
            pass

    def test_basic_agent_creation_without_mcp_tools(self):
        """Test that agents can be created without MCP tools."""
        from xoneaiagents import Agent

        # Creating an agent without MCP tools should work
        agent = Agent(
            name="Test Agent",
            instructions="You are a test agent.",
            llm="gpt-4o-mini"
        )
        assert agent is not None

    def test_mcp_raises_import_error_when_unavailable(self):
        """Test that MCP raises ImportError with install instructions when mcp package unavailable."""
        import xoneaiagents.mcp.mcp as mcp_module

        # Save original value
        original_available = mcp_module.MCP_AVAILABLE

        # Simulate MCP not installed
        mcp_module.MCP_AVAILABLE = False

        try:
            from xoneaiagents.mcp.mcp import MCP
            with pytest.raises(ImportError) as exc_info:
                MCP('test-command')

            error_msg = str(exc_info.value)
            assert 'pip install xoneaiagents[mcp]' in error_msg
            assert 'MCP' in error_msg or 'Model Context Protocol' in error_msg
        finally:
            # Restore original value
            mcp_module.MCP_AVAILABLE = original_available

    def test_sse_client_raises_import_error_when_unavailable(self):
        """Test that SSEMCPClient raises ImportError with install instructions when mcp unavailable."""
        import xoneaiagents.mcp.mcp_sse as sse_module

        original_available = sse_module.MCP_AVAILABLE
        sse_module.MCP_AVAILABLE = False

        try:
            from xoneaiagents.mcp.mcp_sse import SSEMCPClient
            with pytest.raises(ImportError) as exc_info:
                SSEMCPClient('http://test.com/sse')

            error_msg = str(exc_info.value)
            assert 'pip install xoneaiagents[mcp]' in error_msg
        finally:
            sse_module.MCP_AVAILABLE = original_available

    def test_http_stream_client_raises_import_error_when_mcp_unavailable(self):
        """Test that HTTPStreamMCPClient raises ImportError when mcp unavailable."""
        import xoneaiagents.mcp.mcp_http_stream as http_module

        original_available = http_module.MCP_AVAILABLE
        http_module.MCP_AVAILABLE = False

        try:
            from xoneaiagents.mcp.mcp_http_stream import HTTPStreamMCPClient
            with pytest.raises(ImportError) as exc_info:
                HTTPStreamMCPClient('http://test.com/mcp')

            error_msg = str(exc_info.value)
            assert 'pip install xoneaiagents[mcp]' in error_msg
        finally:
            http_module.MCP_AVAILABLE = original_available

    def test_http_stream_client_raises_import_error_when_aiohttp_unavailable(self):
        """Test that HTTPStreamMCPClient raises ImportError when aiohttp unavailable."""
        import xoneaiagents.mcp.mcp_http_stream as http_module

        # Ensure MCP is available but aiohttp is not
        original_available = http_module.MCP_AVAILABLE
        original_aiohttp = http_module.aiohttp

        http_module.MCP_AVAILABLE = True
        http_module.aiohttp = None

        try:
            from xoneaiagents.mcp.mcp_http_stream import HTTPStreamMCPClient
            with pytest.raises(ImportError) as exc_info:
                HTTPStreamMCPClient('http://test.com/mcp')

            error_msg = str(exc_info.value)
            assert 'aiohttp' in error_msg.lower()
            assert 'pip install xoneaiagents[mcp]' in error_msg
        finally:
            http_module.MCP_AVAILABLE = original_available
            http_module.aiohttp = original_aiohttp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
