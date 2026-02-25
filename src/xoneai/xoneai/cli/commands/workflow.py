"""
Workflow command group for XoneAI CLI.

Provides workflow management commands.
"""

import typer

app = typer.Typer(help="Workflow management")


@app.command("run", context_settings={"allow_extra_args": True, "allow_interspersed_args": True, "ignore_unknown_options": True})
def workflow_run(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Workflow file path"),
    model: str = typer.Option(None, "--model", "-m", help="LLM model to use"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Run a workflow.
    
    Use --var key=value to pass variables to YAML workflows.
    Can be specified multiple times.
    
    Example: xoneai workflow run my_workflow.yaml --var topic="AI Tools" --var style="comprehensive"
    """
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['workflow', 'run', file]
    # Pass through extra args (includes --var arguments)
    argv.extend(ctx.args)
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


@app.command("list")
def workflow_list():
    """List available workflows."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['workflow', 'list']
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("create")
def workflow_create(
    name: str = typer.Argument(..., help="Workflow name"),
    template: str = typer.Option(None, "--template", "-t", help="Template to use"),
):
    """Create a new workflow."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['workflow', 'create', name]
    if template:
        argv.extend(['--template', template])
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
