"""
Package command group for XoneAI CLI.

Provides package management commands (pip-like).
"""

import typer

app = typer.Typer(help="Package management")


@app.command("install")
def package_install(
    package: str = typer.Argument(..., help="Package to install"),
    upgrade: bool = typer.Option(False, "--upgrade", "-U", help="Upgrade if already installed"),
):
    """Install a package."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['package', 'install', package]
    if upgrade:
        argv.append('--upgrade')
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("uninstall")
def package_uninstall(
    package: str = typer.Argument(..., help="Package to uninstall"),
):
    """Uninstall a package."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['package', 'uninstall', package]
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("list")
def package_list():
    """List installed packages."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['package', 'list']
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
