"""
Commit command group for XoneAI CLI.

Provides git commit commands with AI assistance.
"""

import typer

app = typer.Typer(help="AI-assisted git commits")


@app.callback(invoke_without_command=True)
def commit_main(
    ctx: typer.Context,
    message: str = typer.Option(None, "--message", "-m", help="Commit message (auto-generated if not provided)"),
    all_files: bool = typer.Option(False, "--all", "-a", help="Stage all changes"),
    push: bool = typer.Option(False, "--push", "-p", help="Push after commit"),
):
    """
    Create AI-assisted git commits.
    
    Examples:
        xoneai commit
        xoneai commit -m "Fix bug"
        xoneai commit --all --push
    """
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['commit']
    if message:
        argv.extend(['--message', message])
    if all_files:
        argv.append('--all')
    if push:
        argv.append('--push')
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
