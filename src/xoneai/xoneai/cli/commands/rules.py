"""
Rules command group for XoneAI CLI.

Provides rules management commands.
"""

import typer

app = typer.Typer(help="Rules management")


@app.command("list")
def rules_list():
    """List active rules."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['rules', 'list']
    
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
def rules_add(
    rule: str = typer.Argument(..., help="Rule to add"),
):
    """Add a rule."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['rules', 'add', rule]
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("clear")
def rules_clear():
    """Clear all rules."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['rules', 'clear']
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
