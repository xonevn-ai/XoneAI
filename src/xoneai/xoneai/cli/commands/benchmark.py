"""
Benchmark command group for XoneAI CLI.

Provides comprehensive performance benchmarking across all execution paths.
"""

from typing import Optional

import typer

app = typer.Typer(help="Comprehensive performance benchmarking")


@app.command("profile")
def benchmark_profile(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations per path"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save results to file"),
    deep: bool = typer.Option(False, "--deep", help="Enable deep cProfile profiling (per-function timing, call graphs)"),
    limit: int = typer.Option(30, "--limit", "-l", help="Top N functions to show in deep profile"),
):
    """
    Run full benchmark suite across all execution paths.
    
    Benchmarks:
    - OpenAI SDK (baseline)
    - XoneAI Agent
    - XoneAI CLI
    - XoneAI CLI with profiling
    - XoneAI Workflow (single agent)
    - XoneAI Workflow (multi-agent)
    - XoneAI via LiteLLM
    - LiteLLM standalone
    
    With --deep flag, includes:
    - Per-function timing (cProfile stats)
    - Self time vs cumulative time
    - Call counts per function
    - Caller/callee relationships
    - Module breakdown by category
    - Call graph data
    
    Examples:
        xoneai benchmark profile "What is 2+2?"
        xoneai benchmark profile "Hi" --iterations 5
        xoneai benchmark profile "Hi" --deep --limit 50
        xoneai benchmark profile "Hi" --deep --format json --output results.json
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    if deep:
        typer.echo("⚠️  Deep profiling enabled - this adds overhead to measurements", err=True)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        verbose=True,
        deep=deep,
        limit=limit
    )
    
    if output_format == "json":
        import json
        output = json.dumps(report.to_dict(), indent=2)
        if output_file:
            with open(output_file, "w") as f:
                f.write(output)
            typer.echo(f"Results saved to {output_file}")
        else:
            typer.echo(output)
    else:
        handler.print_report(report, deep=deep, limit=limit)
        if output_file:
            import json
            with open(output_file, "w") as f:
                f.write(json.dumps(report.to_dict(), indent=2))
            typer.echo(f"\nJSON results saved to {output_file}")


@app.command("compare")
def benchmark_compare(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(2, "--iterations", "-n", help="Number of iterations"),
):
    """
    Quick comparison of key execution paths.
    
    Compares OpenAI SDK, XoneAI Agent, XoneAI CLI, and LiteLLM.
    
    Examples:
        xoneai benchmark compare "Hi"
        xoneai benchmark compare "What is 2+2?" --iterations 3
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        paths=["openai_sdk", "xoneai_agent", "xoneai_cli", "litellm_standalone"],
        verbose=True
    )
    
    typer.echo("\n" + handler.create_comparison_table(report))


@app.command("sdk")
def benchmark_sdk(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
):
    """
    Benchmark OpenAI SDK only (baseline).
    
    Examples:
        xoneai benchmark sdk "Hi"
        xoneai benchmark sdk "What is 2+2?" --iterations 5
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(prompt=prompt, iterations=iterations, paths=["openai_sdk"], verbose=True)
    
    if output_format == "json":
        import json
        typer.echo(json.dumps(report.to_dict(), indent=2))
    else:
        handler.print_report(report)


@app.command("agent")
def benchmark_agent(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
):
    """
    Benchmark XoneAI Agent vs SDK baseline.
    
    Examples:
        xoneai benchmark agent "Hi"
        xoneai benchmark agent "What is 2+2?" --iterations 5
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        paths=["openai_sdk", "xoneai_agent"],
        verbose=True
    )
    
    if output_format == "json":
        import json
        typer.echo(json.dumps(report.to_dict(), indent=2))
    else:
        handler.print_report(report)


@app.command("cli")
def benchmark_cli(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
):
    """
    Benchmark XoneAI CLI vs SDK baseline.
    
    Examples:
        xoneai benchmark cli "Hi"
        xoneai benchmark cli "What is 2+2?" --iterations 5
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        paths=["openai_sdk", "xoneai_cli", "xoneai_cli_profile"],
        verbose=True
    )
    
    if output_format == "json":
        import json
        typer.echo(json.dumps(report.to_dict(), indent=2))
    else:
        handler.print_report(report)


@app.command("workflow")
def benchmark_workflow(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
):
    """
    Benchmark XoneAI Workflow (single and multi-agent) vs SDK baseline.
    
    Examples:
        xoneai benchmark workflow "Hi"
        xoneai benchmark workflow "What is 2+2?" --iterations 5
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        paths=["openai_sdk", "xoneai_workflow_single", "xoneai_workflow_multi"],
        verbose=True
    )
    
    if output_format == "json":
        import json
        typer.echo(json.dumps(report.to_dict(), indent=2))
    else:
        handler.print_report(report)


@app.command("litellm")
def benchmark_litellm(
    prompt: str = typer.Argument("Hi", help="Prompt to benchmark"),
    iterations: int = typer.Option(3, "--iterations", "-n", help="Number of iterations"),
    output_format: str = typer.Option("text", "--format", "-f", help="Output format: text or json"),
):
    """
    Benchmark LiteLLM paths vs SDK baseline.
    
    Examples:
        xoneai benchmark litellm "Hi"
        xoneai benchmark litellm "What is 2+2?" --iterations 5
    """
    try:
        from ..features.benchmark import BenchmarkHandler
    except ImportError as e:
        typer.echo(f"Error: Benchmark module not available: {e}", err=True)
        raise typer.Exit(1)
    
    handler = BenchmarkHandler()
    report = handler.run_full_benchmark(
        prompt=prompt, 
        iterations=iterations, 
        paths=["openai_sdk", "xoneai_litellm", "litellm_standalone"],
        verbose=True
    )
    
    if output_format == "json":
        import json
        typer.echo(json.dumps(report.to_dict(), indent=2))
    else:
        handler.print_report(report)


@app.callback(invoke_without_command=True)
def benchmark_callback(ctx: typer.Context):
    """Show benchmark help if no subcommand."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
