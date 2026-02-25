"""
Realtime command group for XoneAI CLI.

Provides realtime interaction commands.
"""

from typing import Optional

import typer

app = typer.Typer(help="Realtime interaction mode")


@app.callback(invoke_without_command=True)
def realtime_main(
    ctx: typer.Context,
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Start realtime interaction mode.
    
    Examples:
        xoneai realtime
        xoneai realtime --model gpt-4o
    """
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['realtime']
    if model:
        argv.extend(['--model', model])
    if verbose:
        argv.append('--verbose')
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
