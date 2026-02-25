"""
Registry command group for XoneAI CLI.

Provides registry management commands.
"""

import typer

app = typer.Typer(help="Registry management")


@app.command("list")
def registry_list():
    """List registry entries."""
    from xoneai.cli.main import XoneAI
    import sys
    
    argv = ['registry', 'list']
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("serve")
def registry_serve(
    port: int = typer.Option(8080, "--port", "-p", help="Port to serve on"),
):
    """Start registry server.
    
    DEPRECATED: Use `xoneai serve registry` instead.
    """
    from xoneai.cli.main import XoneAI
    import sys
    
    # Print deprecation warning
    print("\n\033[93m⚠ DEPRECATION WARNING:\033[0m", file=sys.stderr)
    print("\033[93m'xoneai registry serve' is deprecated and will be removed in a future version.\033[0m", file=sys.stderr)
    print("\033[93mPlease use 'xoneai serve registry' instead.\033[0m\n", file=sys.stderr)
    
    argv = ['registry', 'serve', '--port', str(port)]
    
    original_argv = sys.argv
    sys.argv = ['xoneai'] + argv
    
    try:
        xone = XoneAI()
        xone.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
