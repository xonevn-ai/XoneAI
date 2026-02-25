"""
Hooks command group for XoneAI CLI.

Provides hook management commands.
"""

import typer

app = typer.Typer(help="Hook management")


@app.command("list")
def hooks_list():
    """List available hooks."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['hooks', 'list']
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("add")
def hooks_add(
    name: str = typer.Argument(..., help="Hook name"),
    event: str = typer.Option(..., "--event", "-e", help="Event to hook into"),
):
    """Add a hook."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['hooks', 'add', name, '--event', event]
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("remove")
def hooks_remove(
    name: str = typer.Argument(..., help="Hook name to remove"),
):
    """Remove a hook."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['hooks', 'remove', name]
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
