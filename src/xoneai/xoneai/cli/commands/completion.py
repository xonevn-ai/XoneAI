"""
Completion command group for XoneAI CLI.

Provides shell completion script generation:
- completion bash: Generate bash completions
- completion zsh: Generate zsh completions
- completion fish: Generate fish completions
"""

import typer

from ..output.console import get_output_controller

app = typer.Typer(help="Shell completion scripts")


BASH_COMPLETION = '''
# XoneAI bash completion
_xoneai_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Top-level commands
    opts="run config traces env session schedule serve completion version debug lsp diag doctor acp mcp chat code call realtime train ui context research memory rules workflow hooks knowledge tools todo docs commit skills profile eval templates recipe endpoints agents thinking compaction output deploy registry package install uninstall"
    
    # Subcommands for specific commands
    case "${prev}" in
        config)
            COMPREPLY=( $(compgen -W "list get set reset path" -- ${cur}) )
            return 0
            ;;
        traces)
            COMPREPLY=( $(compgen -W "enable disable status list" -- ${cur}) )
            return 0
            ;;
        env)
            COMPREPLY=( $(compgen -W "view check doctor" -- ${cur}) )
            return 0
            ;;
        session)
            COMPREPLY=( $(compgen -W "list resume delete export show" -- ${cur}) )
            return 0
            ;;
        schedule)
            COMPREPLY=( $(compgen -W "start stop list logs restart delete describe save stop-all stats" -- ${cur}) )
            return 0
            ;;
        serve)
            COMPREPLY=( $(compgen -W "start stop status" -- ${cur}) )
            return 0
            ;;
        completion)
            COMPREPLY=( $(compgen -W "bash zsh fish" -- ${cur}) )
            return 0
            ;;
        debug)
            COMPREPLY=( $(compgen -W "interactive lsp acp trace" -- ${cur}) )
            return 0
            ;;
        lsp)
            COMPREPLY=( $(compgen -W "start stop status logs" -- ${cur}) )
            return 0
            ;;
        diag)
            COMPREPLY=( $(compgen -W "export" -- ${cur}) )
            return 0
            ;;
        doctor)
            COMPREPLY=( $(compgen -W "env config tools db mcp obs skills memory permissions network performance ci selftest" -- ${cur}) )
            return 0
            ;;
        mcp)
            COMPREPLY=( $(compgen -W "list add remove test" -- ${cur}) )
            return 0
            ;;
        *)
            ;;
    esac
    
    # Global options
    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "--help --version --output-format --json --no-color --quiet --verbose --screen-reader" -- ${cur}) )
        return 0
    fi
    
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _xoneai_completion xoneai
'''

ZSH_COMPLETION = '''
#compdef xoneai

_xoneai() {
    local -a commands
    local -a subcommands
    
    commands=(
        'run:Run agents'
        'config:Configuration management'
        'traces:Trace collection management'
        'env:Environment and diagnostics'
        'session:Session management'
        'schedule:Scheduler management'
        'serve:API server management'
        'completion:Shell completion scripts'
        'version:Version information'
        'debug:Debug and test interactive flows'
        'lsp:LSP service lifecycle'
        'diag:Diagnostics export'
        'doctor:Health checks and diagnostics'
        'acp:Agent Client Protocol server'
        'mcp:MCP server management'
        'chat:Start chat UI'
        'code:Start code UI'
        'call:Start call server'
        'realtime:Start realtime interface'
        'train:Training commands'
        'ui:Start UI'
        'context:Context engineering'
        'research:Deep research'
        'memory:Memory management'
        'rules:Rules management'
        'workflow:Workflow management'
        'hooks:Hooks management'
        'knowledge:Knowledge management'
        'tools:Tools management'
        'todo:Todo management'
        'docs:Documentation'
        'commit:Git commit'
        'skills:Skills management'
        'profile:Profile management'
        'eval:Evaluation'
        'templates:Templates'
        'recipe:Recipe management'
        'endpoints:Endpoints'
        'agents:Agents management'
        'deploy:Deployment'
        'registry:Registry'
        'package:Package management'
        'install:Install packages'
        'uninstall:Uninstall packages'
    )
    
    _arguments -C \\
        '--help[Show help]' \\
        '--version[Show version]' \\
        '--output-format[Output format]:format:(text json stream-json)' \\
        '--json[JSON output]' \\
        '--no-color[Disable colors]' \\
        '--quiet[Minimal output]' \\
        '--verbose[Verbose output]' \\
        '--screen-reader[Screen reader mode]' \\
        '1: :->command' \\
        '*::arg:->args'
    
    case $state in
        command)
            _describe 'command' commands
            ;;
        args)
            case $words[1] in
                config)
                    subcommands=('list:List config' 'get:Get value' 'set:Set value' 'reset:Reset config' 'path:Show path')
                    _describe 'subcommand' subcommands
                    ;;
                traces)
                    subcommands=('enable:Enable traces' 'disable:Disable traces' 'status:Show status' 'list:List traces')
                    _describe 'subcommand' subcommands
                    ;;
                env)
                    subcommands=('view:View env vars' 'check:Check API keys' 'doctor:Run diagnostics')
                    _describe 'subcommand' subcommands
                    ;;
                session)
                    subcommands=('list:List sessions' 'resume:Resume session' 'delete:Delete session' 'export:Export session' 'show:Show session')
                    _describe 'subcommand' subcommands
                    ;;
                schedule)
                    subcommands=('start:Start scheduler' 'stop:Stop scheduler' 'list:List jobs' 'logs:View logs' 'restart:Restart' 'delete:Delete job' 'describe:Describe job' 'save:Save config' 'stop-all:Stop all' 'stats:Show stats')
                    _describe 'subcommand' subcommands
                    ;;
                serve)
                    subcommands=('start:Start server' 'stop:Stop server' 'status:Show status')
                    _describe 'subcommand' subcommands
                    ;;
                completion)
                    subcommands=('bash:Bash completion' 'zsh:Zsh completion' 'fish:Fish completion')
                    _describe 'subcommand' subcommands
                    ;;
                debug)
                    subcommands=('interactive:Interactive debug' 'lsp:LSP debug' 'acp:ACP debug' 'trace:Trace debug')
                    _describe 'subcommand' subcommands
                    ;;
                lsp)
                    subcommands=('start:Start LSP' 'stop:Stop LSP' 'status:LSP status' 'logs:LSP logs')
                    _describe 'subcommand' subcommands
                    ;;
                diag)
                    subcommands=('export:Export diagnostics')
                    _describe 'subcommand' subcommands
                    ;;
                doctor)
                    subcommands=('env:Check env' 'config:Check config' 'tools:Check tools' 'db:Check DB' 'mcp:Check MCP' 'obs:Check observability' 'skills:Check skills' 'memory:Check memory' 'permissions:Check permissions' 'network:Check network' 'performance:Check performance' 'ci:CI checks' 'selftest:Self test')
                    _describe 'subcommand' subcommands
                    ;;
                mcp)
                    subcommands=('list:List servers' 'add:Add server' 'remove:Remove server' 'test:Test server')
                    _describe 'subcommand' subcommands
                    ;;
            esac
            ;;
    esac
}

_xoneai "$@"
'''

FISH_COMPLETION = '''
# XoneAI fish completion

# Top-level commands
complete -c xoneai -f -n "__fish_use_subcommand" -a "run" -d "Run agents"
complete -c xoneai -f -n "__fish_use_subcommand" -a "config" -d "Configuration management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "traces" -d "Trace collection management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "env" -d "Environment and diagnostics"
complete -c xoneai -f -n "__fish_use_subcommand" -a "session" -d "Session management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "schedule" -d "Scheduler management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "serve" -d "API server management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "completion" -d "Shell completion scripts"
complete -c xoneai -f -n "__fish_use_subcommand" -a "version" -d "Version information"
complete -c xoneai -f -n "__fish_use_subcommand" -a "debug" -d "Debug and test interactive flows"
complete -c xoneai -f -n "__fish_use_subcommand" -a "lsp" -d "LSP service lifecycle"
complete -c xoneai -f -n "__fish_use_subcommand" -a "diag" -d "Diagnostics export"
complete -c xoneai -f -n "__fish_use_subcommand" -a "doctor" -d "Health checks and diagnostics"
complete -c xoneai -f -n "__fish_use_subcommand" -a "acp" -d "Agent Client Protocol server"
complete -c xoneai -f -n "__fish_use_subcommand" -a "mcp" -d "MCP server management"
complete -c xoneai -f -n "__fish_use_subcommand" -a "chat" -d "Start chat UI"
complete -c xoneai -f -n "__fish_use_subcommand" -a "code" -d "Start code UI"

# Global options
complete -c xoneai -l help -d "Show help"
complete -c xoneai -l version -d "Show version"
complete -c xoneai -l output-format -x -a "text json stream-json" -d "Output format"
complete -c xoneai -l json -d "JSON output"
complete -c xoneai -l no-color -d "Disable colors"
complete -c xoneai -l quiet -s q -d "Minimal output"
complete -c xoneai -l verbose -s v -d "Verbose output"
complete -c xoneai -l screen-reader -d "Screen reader mode"

# config subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from config" -a "list" -d "List config"
complete -c xoneai -f -n "__fish_seen_subcommand_from config" -a "get" -d "Get value"
complete -c xoneai -f -n "__fish_seen_subcommand_from config" -a "set" -d "Set value"
complete -c xoneai -f -n "__fish_seen_subcommand_from config" -a "reset" -d "Reset config"
complete -c xoneai -f -n "__fish_seen_subcommand_from config" -a "path" -d "Show path"

# traces subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from traces" -a "enable" -d "Enable traces"
complete -c xoneai -f -n "__fish_seen_subcommand_from traces" -a "disable" -d "Disable traces"
complete -c xoneai -f -n "__fish_seen_subcommand_from traces" -a "status" -d "Show status"
complete -c xoneai -f -n "__fish_seen_subcommand_from traces" -a "list" -d "List traces"

# env subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from env" -a "view" -d "View env vars"
complete -c xoneai -f -n "__fish_seen_subcommand_from env" -a "check" -d "Check API keys"
complete -c xoneai -f -n "__fish_seen_subcommand_from env" -a "doctor" -d "Run diagnostics"

# session subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from session" -a "list" -d "List sessions"
complete -c xoneai -f -n "__fish_seen_subcommand_from session" -a "resume" -d "Resume session"
complete -c xoneai -f -n "__fish_seen_subcommand_from session" -a "delete" -d "Delete session"
complete -c xoneai -f -n "__fish_seen_subcommand_from session" -a "export" -d "Export session"
complete -c xoneai -f -n "__fish_seen_subcommand_from session" -a "show" -d "Show session"

# completion subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from completion" -a "bash" -d "Bash completion"
complete -c xoneai -f -n "__fish_seen_subcommand_from completion" -a "zsh" -d "Zsh completion"
complete -c xoneai -f -n "__fish_seen_subcommand_from completion" -a "fish" -d "Fish completion"

# debug subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from debug" -a "interactive" -d "Interactive debug"
complete -c xoneai -f -n "__fish_seen_subcommand_from debug" -a "lsp" -d "LSP debug"
complete -c xoneai -f -n "__fish_seen_subcommand_from debug" -a "acp" -d "ACP debug"
complete -c xoneai -f -n "__fish_seen_subcommand_from debug" -a "trace" -d "Trace debug"

# doctor subcommands
complete -c xoneai -f -n "__fish_seen_subcommand_from doctor" -a "env" -d "Check env"
complete -c xoneai -f -n "__fish_seen_subcommand_from doctor" -a "config" -d "Check config"
complete -c xoneai -f -n "__fish_seen_subcommand_from doctor" -a "tools" -d "Check tools"
complete -c xoneai -f -n "__fish_seen_subcommand_from doctor" -a "db" -d "Check DB"
complete -c xoneai -f -n "__fish_seen_subcommand_from doctor" -a "mcp" -d "Check MCP"
'''


@app.command("bash")
def completion_bash():
    """Generate bash completion script."""
    print(BASH_COMPLETION.strip())


@app.command("zsh")
def completion_zsh():
    """Generate zsh completion script."""
    print(ZSH_COMPLETION.strip())


@app.command("fish")
def completion_fish():
    """Generate fish completion script."""
    print(FISH_COMPLETION.strip())


@app.callback(invoke_without_command=True)
def completion_callback(ctx: typer.Context):
    """Show completion installation instructions."""
    if ctx.invoked_subcommand is None:
        output = get_output_controller()
        output.print_panel(
            "Generate shell completion scripts.\n\n"
            "Usage:\n"
            "  # Bash\n"
            "  xoneai completion bash >> ~/.bashrc\n\n"
            "  # Zsh\n"
            "  xoneai completion zsh > ~/.zsh/completions/_xoneai\n\n"
            "  # Fish\n"
            "  xoneai completion fish > ~/.config/fish/completions/xoneai.fish",
            title="Shell Completions"
        )
