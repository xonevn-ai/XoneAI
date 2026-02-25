# XoneAI Profiling Examples

This directory contains examples for profiling XoneAI agent performance.

## Prerequisites

```bash
pip install xoneai
export OPENAI_API_KEY=your_key_here
```

## Examples

### 1. Basic Profiling (`basic_profiling.py`)

Demonstrates programmatic profiling of a single query:

```bash
python basic_profiling.py
```

### 2. Suite Profiling (`suite_profiling.py`)

Runs a comprehensive profiling suite with multiple scenarios:

```bash
python suite_profiling.py
```

### 3. Optimization Demo (`optimization_example.py`)

Demonstrates Tier 0/1/2 performance optimizations:

```bash
python optimization_example.py
```

## CLI Commands

You can also profile directly from the command line:

```bash
# Profile a query
xoneai profile query "What is 2+2?"

# Profile with file grouping
xoneai profile query "Hello" --show-files --limit 20

# Profile imports
xoneai profile imports

# Profile startup time
xoneai profile startup

# Run comprehensive suite
xoneai profile suite --quick

# Create performance baseline
xoneai profile snapshot --baseline

# Compare against baseline
xoneai profile snapshot current --compare

# Show optimization status
xoneai profile optimize --show
```

## Output

- **Text output**: Human-readable timing breakdown
- **JSON output**: Machine-readable for CI/CD (`--format json`)
- **Artifacts**: Binary cProfile data and reports (`--save ./results`)
- **Snapshots**: Performance baselines for regression detection

## Performance Optimizations

Enable opt-in optimizations via environment variables:

```bash
export XONEAI_LITE_MODE=1
export XONEAI_SKIP_TYPE_VALIDATION=1
export XONEAI_MINIMAL_IMPORTS=1
```
