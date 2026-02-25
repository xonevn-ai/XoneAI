"""
Doctor command group for XoneAI CLI.

Wraps existing doctor functionality from features/doctor/.
Provides health checks and diagnostics.
"""

from typing import Optional

import typer

from ..output.console import get_output_controller

app = typer.Typer(help="Health checks and diagnostics")


def _run_doctor(args: list) -> int:
    """Run doctor command with args."""
    try:
        from ..features.doctor.handler import DoctorHandler
        handler = DoctorHandler()
        # DoctorHandler uses execute(action, action_args) pattern
        action = args[0] if args else None
        action_args = args[1:] if len(args) > 1 else []
        return handler.execute(action, action_args)
    except ImportError as e:
        output = get_output_controller()
        output.print_error(f"Doctor module not available: {e}")
        return 4
    except Exception as e:
        output = get_output_controller()
        output.print_error(f"Doctor error: {e}")
        return 1


@app.command("env")
def doctor_env(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
    timeout: float = typer.Option(10.0, "--timeout", help="Per-check timeout"),
):
    """Check environment variables and API keys."""
    args = ["env"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    args.extend(["--timeout", str(timeout)])
    raise typer.Exit(_run_doctor(args))


@app.command("config")
def doctor_config(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check configuration files."""
    args = ["config"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("tools")
def doctor_tools(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check tools availability."""
    args = ["tools"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("db")
def doctor_db(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check database connections."""
    args = ["db"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("mcp")
def doctor_mcp(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check MCP servers."""
    args = ["mcp"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("network")
def doctor_network(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check network connectivity."""
    args = ["network"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("performance")
def doctor_performance(
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Check performance metrics."""
    args = ["performance"]
    if deep:
        args.append("--deep")
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("selftest")
def doctor_selftest(
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Run self-test."""
    args = ["selftest"]
    if json_output:
        args.append("--json")
    raise typer.Exit(_run_doctor(args))


@app.command("cleanup")
def doctor_cleanup(
    dry_run: bool = typer.Option(True, "--dry-run/--execute", help="Show what would be removed without removing"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """
    Clean up stale package artifacts that can cause import errors.
    
    This removes stale xoneaiagents directories from site-packages that
    lack an __init__.py file (namespace package artifacts).
    
    Examples:
        xoneai doctor cleanup           # Show what would be removed
        xoneai doctor cleanup --execute # Actually remove stale artifacts
    """
    import os
    import site
    import shutil
    
    output = get_output_controller()
    
    stale_dirs = []
    
    # Check all site-packages directories
    try:
        site_packages = site.getsitepackages()
    except AttributeError:
        site_packages = []
    
    # Also check user site-packages
    user_site = site.getusersitepackages() if hasattr(site, 'getusersitepackages') else None
    if user_site:
        site_packages = list(site_packages) + [user_site]
    
    for sp in site_packages:
        xoneai_dir = os.path.join(sp, 'xoneaiagents')
        if os.path.isdir(xoneai_dir):
            init_path = os.path.join(xoneai_dir, '__init__.py')
            if not os.path.exists(init_path):
                stale_dirs.append(xoneai_dir)
    
    if not stale_dirs:
        output.print_success("No stale package artifacts found. Environment is clean.")
        raise typer.Exit(0)
    
    output.print_warning(f"Found {len(stale_dirs)} stale xoneaiagents directory(ies):")
    for d in stale_dirs:
        output.console.print(f"  • {d}")
    
    if dry_run:
        output.console.print("\n[dim]Run with --execute to remove these directories.[/dim]")
        raise typer.Exit(0)
    
    # Confirm before removing
    if not force:
        confirm = typer.confirm("\nRemove these directories?")
        if not confirm:
            output.print_info("Aborted.")
            raise typer.Exit(0)
    
    # Remove stale directories
    removed = 0
    for d in stale_dirs:
        try:
            shutil.rmtree(d)
            output.print_success(f"Removed: {d}")
            removed += 1
        except Exception as e:
            output.print_error(f"Failed to remove {d}: {e}")
    
    if removed == len(stale_dirs):
        output.print_success(f"\nSuccessfully cleaned up {removed} stale directory(ies).")
        output.console.print("[dim]Run 'pip install xoneaiagents' to reinstall if needed.[/dim]")
    else:
        output.print_warning(f"\nCleaned up {removed}/{len(stale_dirs)} directories.")
    
    raise typer.Exit(0 if removed == len(stale_dirs) else 1)


@app.command("troubleshoot")
def doctor_troubleshoot():
    """
    Show troubleshooting information for common import errors.
    
    This command displays diagnostic information and solutions for:
    - ImportError: cannot import name 'Agent' from 'xoneaiagents'
    - Namespace package shadowing issues
    - Stale package artifacts
    """
    output = get_output_controller()
    
    output.console.print("\n[bold cyan]XoneAI Import Troubleshooting[/bold cyan]\n")
    
    # Check current state
    output.console.print("[bold]1. Checking xoneaiagents package state...[/bold]")
    
    try:
        import xoneaiagents
        file_attr = xoneaiagents.__file__
        spec_origin = xoneaiagents.__spec__.origin if xoneaiagents.__spec__ else None
        
        if file_attr is None:
            output.print_error("  ✗ xoneaiagents.__file__ is None (namespace package detected)")
            output.console.print("    [yellow]This indicates stale artifacts in site-packages.[/yellow]")
        else:
            output.print_success(f"  ✓ xoneaiagents.__file__: {file_attr}")
        
        if spec_origin is None:
            output.print_error("  ✗ xoneaiagents.__spec__.origin is None")
        else:
            output.print_success(f"  ✓ xoneaiagents.__spec__.origin: {spec_origin}")
        
        # Try importing Agent
        output.console.print("\n[bold]2. Testing Agent import...[/bold]")
        try:
            from xoneaiagents import Agent
            output.print_success(f"  ✓ Agent imported successfully: {Agent}")
        except ImportError as e:
            output.print_error(f"  ✗ Agent import failed: {e}")
            
    except ImportError as e:
        output.print_error(f"  ✗ Cannot import xoneaiagents: {e}")
    
    # Check for stale directories
    output.console.print("\n[bold]3. Checking for stale artifacts...[/bold]")
    import site
    import os
    
    stale_found = False
    try:
        site_packages = site.getsitepackages()
    except AttributeError:
        site_packages = []
    
    for sp in site_packages:
        xoneai_dir = os.path.join(sp, 'xoneaiagents')
        if os.path.isdir(xoneai_dir):
            init_path = os.path.join(xoneai_dir, '__init__.py')
            if not os.path.exists(init_path):
                output.print_error(f"  ✗ Stale directory found: {xoneai_dir}")
                stale_found = True
            else:
                output.print_success(f"  ✓ Valid package at: {xoneai_dir}")
    
    if not stale_found:
        output.print_success("  ✓ No stale artifacts found")
    
    # Show solutions
    output.console.print("\n[bold]Solutions:[/bold]")
    output.console.print("""
[cyan]If you see import errors:[/cyan]

1. Run cleanup to remove stale artifacts:
   [green]xoneai doctor cleanup --execute[/green]

2. Reinstall xoneaiagents:
   [green]pip install --force-reinstall xoneaiagents[/green]

3. Or manually remove stale directory:
   [green]rm -rf $(python -c "import site; print(site.getsitepackages()[0])")/xoneaiagents/[/green]

[cyan]For editable installs:[/cyan]
   [green]pip install -e /path/to/xoneai-agents[/green]
""")
    
    raise typer.Exit(0)


@app.callback(invoke_without_command=True)
def doctor_callback(
    ctx: typer.Context,
    deep: bool = typer.Option(False, "--deep", help="Enable deeper probes"),
    json_output: bool = typer.Option(False, "--json", help="Output JSON"),
    strict: bool = typer.Option(False, "--strict", help="Treat warnings as failures"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Minimal output"),
):
    """Run all fast health checks."""
    if ctx.invoked_subcommand is None:
        args = []
        if deep:
            args.append("--deep")
        if json_output:
            args.append("--json")
        if strict:
            args.append("--strict")
        if quiet:
            args.append("--quiet")
        raise typer.Exit(_run_doctor(args))
