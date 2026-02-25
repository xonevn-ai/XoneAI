"""Example: Discover tools from installed packages."""

# Discover from xoneaiagents built-in tools
try:
    from xoneaiagents.tools import TOOL_MAPPINGS
    print("Built-in tools from xoneaiagents:")
    for name in list(TOOL_MAPPINGS.keys())[:10]:
        print(f"  - {name}")
    print(f"  ... and {len(TOOL_MAPPINGS) - 10} more")
except ImportError:
    print("xoneaiagents not installed")

# Discover from xoneai_tools
try:
    import xoneai_tools
    print("\nTools from xoneai_tools:")
    
    # Check for video module
    try:
        from xoneai_tools import video
        print("  - xoneai_tools.video (video editing)")
    except ImportError:
        pass
except ImportError:
    print("xoneai_tools not installed")
