"""
XoneAI Branding - Single Source of Truth.

This module provides unified branding assets (logo, version, product name)
for all interactive UIs. All frontends should import from here.

Usage:
    from xoneai.cli.branding import get_logo, get_version, PRODUCT_NAME
"""

# Product name
PRODUCT_NAME = "Xone AI"

# ASCII Art Logos - responsive to terminal width
LOGO_LARGE = r"""
 ___    ___ ________  ________   _______           ________  ___     
|\  \  /  /|\   __  \|\   ___  \|\  ___ \         |\   __  \|\  \    
\ \  \/  / | \  \|\  \ \  \\ \  \ \   __/|        \ \  \|\  \ \  \   
 \ \    / / \ \  \\\  \ \  \\ \  \ \  \_|/__       \ \   __  \ \  \  
  /     \/   \ \  \\\  \ \  \\ \  \ \  \_|\ \       \ \  \ \  \ \  \ 
 /  /\   \    \ \_______\ \__\\ \__\ \_______\       \ \__\ \__\ \__\
/__/ /\ __\    \|_______|\|__| \|__|\|_______|        \|__|\|__|\|__|
|__|/ \|__|                                                          
"""

LOGO_MEDIUM = r"""
   _  ______  _   ________   ___    ____
  | |/ / __ \/ | / / ____/  /   |  /  _/
  |   / / / /  |/ / __/    / /| |  / /  
 /   / /_/ / /|  / /___   / ___ |_/ /   
/_/|_\____/_/ |_/_____/  /_/  |_/___/   
"""

LOGO_SMALL = "▶ Xone AI"

LOGO_MINIMAL = "Xone AI"


def get_version() -> str:
    """Get XoneAI version string."""
    try:
        from xoneai import __version__
        return __version__
    except Exception:
        return "1.0.0"


def get_logo(width: int = 80) -> str:
    """
    Get appropriate logo based on terminal width.
    
    Args:
        width: Terminal width in characters
        
    Returns:
        ASCII art logo string appropriate for the width
    """
    if width >= 75:
        return LOGO_LARGE
    elif width >= 40:
        return LOGO_MEDIUM
    else:
        return LOGO_SMALL


def get_banner(width: int = 80, show_version: bool = True, model: str = None) -> str:
    """
    Get full banner with logo, version, and optional model info.
    
    Args:
        width: Terminal width
        show_version: Whether to include version
        model: Optional model name to display
        
    Returns:
        Complete banner string
    """
    lines = []
    
    # Logo
    logo = get_logo(width)
    lines.append(logo.strip())
    lines.append("")
    
    # Version and model
    version_line = f"  v{get_version()}"
    if model:
        version_line += f" · Model: {model}"
    lines.append(version_line)
    lines.append("")
    
    return "\n".join(lines)


def get_welcome_tips() -> str:
    """Get welcome tips for new sessions."""
    return """  Type your message and press Enter. Use /help for commands.
  Use PageUp/PageDown or Ctrl+Up/Down to scroll."""
