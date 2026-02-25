"""
Tools Doctor for XoneAI.

Diagnoses tool availability, checks dependencies, and reports issues.
Supports both human-readable and JSON output formats.
"""

import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class ToolsDoctor:
    """
    Diagnoses tool availability and dependencies.
    
    Checks:
    - xoneai-tools installation
    - Built-in tools availability
    - Custom tool directories
    - Optional dependency packages
    """
    
    # Default custom tool directories
    DEFAULT_TOOL_DIRS = [
        "~/.xone/tools",
        "~/.config/xone/tools",
    ]
    
    # Known tools and their optional dependencies
    TOOL_DEPENDENCIES = {
        "youtube_tool": ["pytube", "youtube-transcript-api"],
        "whisper_tool": ["openai-whisper", "torch"],
        "vision_tool": ["pillow", "opencv-python"],
        "tavily_search": ["tavily-python"],
        "arxiv_search": ["arxiv"],
        "wikipedia_search": ["wikipedia"],
    }
    
    def __init__(self, custom_dirs: Optional[List[str]] = None):
        """
        Initialize tools doctor.
        
        Args:
            custom_dirs: Additional custom tool directories to check
        """
        self._custom_dirs = custom_dirs or []
    
    def diagnose(self) -> Dict[str, Any]:
        """
        Run full diagnostics.
        
        Returns:
            Dict with diagnostic results
        """
        result = {
            "xoneai_tools_installed": self._check_xoneai_tools(),
            "xoneaiagents_installed": self._check_xoneaiagents(),
            "builtin_tools": self._get_builtin_tools(),
            "xoneai_tools_available": self._get_xoneai_tools_list(),
            "custom_tools_dirs": self._check_custom_dirs(),
            "tool_dependencies": self._check_tool_dependencies(),
            "issues": [],
        }
        
        # Collect issues
        if not result["xoneaiagents_installed"]:
            result["issues"].append({
                "severity": "error",
                "message": "xoneaiagents not installed",
                "hint": "pip install xoneaiagents"
            })
        
        if not result["xoneai_tools_installed"]:
            result["issues"].append({
                "severity": "warning",
                "message": "xoneai-tools not installed (optional)",
                "hint": "pip install xoneai-tools"
            })
        
        # Check for missing dependencies
        for tool, deps in result["tool_dependencies"].items():
            missing = [d for d in deps if not d["available"]]
            if missing:
                result["issues"].append({
                    "severity": "info",
                    "message": f"Tool '{tool}' has missing optional dependencies",
                    "hint": f"pip install {' '.join(d['name'] for d in missing)}"
                })
        
        return result
    
    def _check_xoneai_tools(self) -> bool:
        """Check if xoneai-tools is installed."""
        spec = importlib.util.find_spec("xoneai_tools")
        return spec is not None
    
    def _check_xoneaiagents(self) -> bool:
        """Check if xoneaiagents is installed."""
        spec = importlib.util.find_spec("xoneaiagents")
        return spec is not None
    
    def _get_builtin_tools(self) -> List[str]:
        """Get list of built-in tools."""
        tools = []
        try:
            from xoneaiagents.tools import TOOL_MAPPINGS
            tools = list(TOOL_MAPPINGS.keys())
        except ImportError:
            pass
        return tools
    
    def _get_xoneai_tools_list(self) -> List[str]:
        """Get list of tools from xoneai-tools package."""
        tools = []
        try:
            import xoneai_tools
            # Get all callable attributes that look like tools
            for name in dir(xoneai_tools):
                if not name.startswith("_"):
                    obj = getattr(xoneai_tools, name, None)
                    if callable(obj):
                        tools.append(name)
        except ImportError:
            pass
        return tools
    
    def _check_custom_dirs(self) -> List[Dict[str, Any]]:
        """Check custom tool directories."""
        dirs = []
        
        # Check default dirs
        for dir_path in self.DEFAULT_TOOL_DIRS:
            path = Path(dir_path).expanduser()
            tool_count = 0
            if path.exists():
                # Count Python files
                tool_count = len(list(path.glob("*.py")))
            
            dirs.append({
                "path": str(path),
                "exists": path.exists(),
                "tool_count": tool_count
            })
        
        # Check custom dirs
        for dir_path in self._custom_dirs:
            path = Path(dir_path).expanduser()
            tool_count = 0
            if path.exists():
                tool_count = len(list(path.glob("*.py")))
            
            dirs.append({
                "path": str(path),
                "exists": path.exists(),
                "tool_count": tool_count,
                "custom": True
            })
        
        return dirs
    
    def _check_tool_dependencies(self) -> Dict[str, List[Dict[str, Any]]]:
        """Check dependencies for known tools."""
        result = {}
        
        for tool, deps in self.TOOL_DEPENDENCIES.items():
            result[tool] = []
            for dep in deps:
                spec = importlib.util.find_spec(dep.replace("-", "_"))
                result[tool].append({
                    "name": dep,
                    "available": spec is not None
                })
        
        return result
    
    def diagnose_json(self) -> str:
        """
        Run diagnostics and return JSON output.
        
        Returns:
            JSON string with diagnostic results
        """
        result = self.diagnose()
        return json.dumps(result, indent=2)
    
    def diagnose_human(self) -> str:
        """
        Run diagnostics and return human-readable output.
        
        Returns:
            Formatted string with diagnostic results
        """
        result = self.diagnose()
        lines = []
        
        lines.append("=" * 60)
        lines.append("XoneAI Tools Doctor")
        lines.append("=" * 60)
        lines.append("")
        
        # Core packages
        lines.append("Core Packages:")
        status = "✓" if result["xoneaiagents_installed"] else "✗"
        lines.append(f"  {status} xoneaiagents")
        status = "✓" if result["xoneai_tools_installed"] else "✗"
        lines.append(f"  {status} xoneai-tools (optional)")
        lines.append("")
        
        # Built-in tools
        lines.append(f"Built-in Tools ({len(result['builtin_tools'])}):")
        if result["builtin_tools"]:
            for tool in result["builtin_tools"][:10]:
                lines.append(f"  • {tool}")
            if len(result["builtin_tools"]) > 10:
                lines.append(f"  ... and {len(result['builtin_tools']) - 10} more")
        else:
            lines.append("  (none found)")
        lines.append("")
        
        # xoneai-tools
        if result["xoneai_tools_available"]:
            lines.append(f"xoneai-tools ({len(result['xoneai_tools_available'])}):")
            for tool in result["xoneai_tools_available"][:10]:
                lines.append(f"  • {tool}")
            if len(result["xoneai_tools_available"]) > 10:
                lines.append(f"  ... and {len(result['xoneai_tools_available']) - 10} more")
            lines.append("")
        
        # Custom directories
        lines.append("Custom Tool Directories:")
        for dir_info in result["custom_tools_dirs"]:
            status = "✓" if dir_info["exists"] else "✗"
            count = f" ({dir_info['tool_count']} tools)" if dir_info["exists"] else ""
            custom = " [custom]" if dir_info.get("custom") else ""
            lines.append(f"  {status} {dir_info['path']}{count}{custom}")
        lines.append("")
        
        # Issues
        if result["issues"]:
            lines.append("Issues Found:")
            for issue in result["issues"]:
                icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(issue["severity"], "•")
                lines.append(f"  {icon} {issue['message']}")
                if issue.get("hint"):
                    lines.append(f"     Hint: {issue['hint']}")
            lines.append("")
        else:
            lines.append("✓ No issues found")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
