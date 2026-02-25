"""
UI command group for XoneAI CLI.

Provides all browser-based UI commands.
ALL browser UIs are under this namespace - nothing outside 'xoneai ui' opens a browser.
"""

import typer

app = typer.Typer(help="Browser-based web UI (all browser modes)")


@app.callback(invoke_without_command=True)
def ui_main(
    ctx: typer.Context,
    port: int = typer.Option(8082, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
):
    """
    Start the default web UI (agents management).
    
    DEPRECATED: Use `xoneai serve ui` instead.
    
    All browser-based UIs are under this namespace:
    - xoneai ui         - Default agents UI
    - xoneai ui chat    - Chat interface
    - xoneai ui code    - Code assistant interface
    - xoneai ui realtime - Voice/realtime interface
    - xoneai ui gradio  - Gradio interface
    
    Examples:
        xoneai ui
        xoneai ui --port 3000
        xoneai ui --public
    """
    import sys
    
    # Print deprecation warning
    print("\n\033[93m⚠ DEPRECATION WARNING:\033[0m", file=sys.stderr)
    print("\033[93m'xoneai ui' is deprecated and will be removed in a future version.\033[0m", file=sys.stderr)
    print("\033[93mPlease use 'xoneai serve ui' instead.\033[0m\n", file=sys.stderr)
    
    # If a subcommand was invoked, don't run the default
    if ctx.invoked_subcommand is not None:
        return
    
    # Default: launch agents UI (Chainlit)
    _launch_chainlit_ui("agents", port, host, public)


@app.command("chat")
def ui_chat(
    port: int = typer.Option(8084, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
):
    """
    Start the browser-based chat UI (Chainlit).
    
    For terminal-native chat, use: xoneai chat
    
    Examples:
        xoneai ui chat
        xoneai ui chat --port 3000
    """
    _launch_chainlit_ui("chat", port, host, public)


@app.command("code")
def ui_code(
    port: int = typer.Option(8086, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
):
    """
    Start the browser-based code assistant UI (Chainlit).
    
    For terminal-native code assistant, use: xoneai code
    
    Examples:
        xoneai ui code
        xoneai ui code --port 3000
    """
    _launch_chainlit_ui("code", port, host, public)


@app.command("realtime")
def ui_realtime(
    port: int = typer.Option(8088, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
):
    """
    Start the browser-based realtime/voice UI (Chainlit).
    
    Examples:
        xoneai ui realtime
        xoneai ui realtime --port 3000
    """
    _launch_chainlit_ui("realtime", port, host, public)


@app.command("bot")
def ui_bot(
    port: int = typer.Option(8090, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
    agent: str = typer.Option(None, "--agent", "-a", help="Agent YAML configuration file"),
    model: str = typer.Option("gpt-4o-mini", "--model", "-m", help="LLM model to use"),
    memory: bool = typer.Option(False, "--memory", help="Enable memory"),
    web_search: bool = typer.Option(False, "--web", "--web-search", help="Enable web search"),
    web_provider: str = typer.Option("duckduckgo", "--web-provider", help="Web search provider"),
    tools: str = typer.Option(None, "--tools", help="Comma-separated tool names"),
    auto_approve: bool = typer.Option(False, "--auto-approve", help="Auto-approve tool executions"),
):
    """
    Start the bot chat UI with real-time streaming and tool visualization.
    
    This provides a Chainlit-based chat interface backed by a XoneAI Agent
    with real streaming (via StreamEventEmitter), tool call Steps, and hook firing.
    
    Examples:
        xoneai ui bot
        xoneai ui bot --model gpt-4o --memory --web
        xoneai ui bot --agent agents.yaml --tools DuckDuckGoTool,WikipediaTool
    """
    import os
    
    # Pass config to bot.py via environment variables
    os.environ["XONEAI_BOT_MODEL"] = model
    if agent:
        os.environ["XONEAI_BOT_AGENT_FILE"] = agent
    if memory:
        os.environ["XONEAI_BOT_MEMORY"] = "true"
    if web_search:
        os.environ["XONEAI_BOT_WEB_SEARCH"] = "true"
    os.environ["XONEAI_BOT_WEB_PROVIDER"] = web_provider
    if tools:
        os.environ["XONEAI_BOT_TOOLS"] = tools
    if auto_approve:
        os.environ["XONEAI_BOT_AUTO_APPROVE"] = "true"
    
    _launch_chainlit_ui("bot", port, host, public)


@app.command("gradio")
def ui_gradio(
    port: int = typer.Option(8080, "--port", "-p", help="Port to run UI on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    public: bool = typer.Option(False, "--public", help="Make UI publicly accessible"),
):
    """
    Start the Gradio-based web UI.
    
    Examples:
        xoneai ui gradio
        xoneai ui gradio --port 3000
    """
    _launch_gradio_ui(port, host, public)


def _launch_chainlit_ui(ui_type: str, port: int, host: str, public: bool):
    """Launch a Chainlit-based UI."""
    import os
    import sys
    
    try:
        import importlib.util
        CHAINLIT_AVAILABLE = importlib.util.find_spec("chainlit") is not None
    except ImportError:
        CHAINLIT_AVAILABLE = False
    
    if not CHAINLIT_AVAILABLE:
        install_extra = {
            "agents": "ui",
            "chat": "chat",
            "code": "code",
            "realtime": "realtime",
        }.get(ui_type, "ui")
        print(f"[red]ERROR: {ui_type.title()} UI is not installed. Install with:[/red]")
        print(f'\npip install "xoneai[{install_extra}]"\n')
        sys.exit(1)
    
    import xoneai
    
    # Set environment variables
    os.environ["CHAINLIT_PORT"] = str(port)
    os.environ["CHAINLIT_HOST"] = host
    
    root_path = os.path.join(os.path.expanduser("~"), ".xone")
    if "CHAINLIT_APP_ROOT" not in os.environ:
        os.environ["CHAINLIT_APP_ROOT"] = root_path
    
    # Determine UI script path
    ui_scripts = {
        "agents": "chainlit_ui.py",
        "chat": os.path.join("ui", "chat.py"),
        "code": os.path.join("ui", "code.py"),
        "realtime": os.path.join("ui", "realtime.py"),
        "bot": os.path.join("ui", "bot.py"),
    }
    
    ui_script = ui_scripts.get(ui_type, "chainlit_ui.py")
    ui_path = os.path.join(os.path.dirname(xoneai.__file__), ui_script)
    
    print(f"Starting {ui_type} UI at http://{host}:{port}")
    
    # Use subprocess to run chainlit with proper CLI args
    import subprocess
    
    cmd = ["chainlit", "run", ui_path, "--host", host, "--port", str(port)]
    if public:
        cmd.append("--public")
    
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        # Fallback: try running with python -m chainlit
        cmd = [sys.executable, "-m", "chainlit", "run", ui_path, "--host", host, "--port", str(port)]
        if public:
            cmd.append("--public")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nUI stopped.")


def _launch_gradio_ui(port: int, host: str, public: bool):
    """Launch the Gradio-based UI."""
    import sys
    import importlib.util
    
    GRADIO_AVAILABLE = importlib.util.find_spec("gradio") is not None
    
    if not GRADIO_AVAILABLE:
        print("[red]ERROR: Gradio UI is not installed. Install with:[/red]")
        print('\npip install "xoneai[gradio]"\n')
        sys.exit(1)
    
    from xoneai.cli.main import XoneAI
    xone = XoneAI()
    xone.create_gradio_interface()
