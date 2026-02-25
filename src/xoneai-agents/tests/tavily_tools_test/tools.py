"""
Tools for tavily_tools_test recipe.

Demonstrates usage of tavily_search and tavily_extract from xoneai-tools.
Also shows how to define variables in tools.py.
"""

# Import tavily tools from xoneai-tools
from xoneai_tools.tools import tavily_search, tavily_extract

# Variables can be defined in tools.py
DEFAULT_MAX_RESULTS = 5
SEARCH_DEPTH = "advanced"

# Export tools for use in agents.yaml
TOOLS = [tavily_search, tavily_extract]


def get_all_tools():
    """Get all tools defined in this recipe."""
    return TOOLS
