# Recipe Background Tasks Example

This example demonstrates how to run recipes and agents as background tasks.

## Prerequisites

```bash
pip install xoneai xoneaiagents
export OPENAI_API_KEY="your-api-key"
```

## Python Example

```bash
python example_background.py
```

## CLI Examples

### Submit a recipe as background task

```bash
# Submit recipe to background
xoneai background submit --recipe my-recipe --input '{"query": "test"}'

# Check status
xoneai background status <task_id>

# List all tasks
xoneai background list

# Cancel a task
xoneai background cancel <task_id>

# Clear completed tasks
xoneai background clear
```

### Run recipe with --background flag

```bash
# Run recipe in background
xoneai recipe run my-recipe --background

# With input
xoneai recipe run my-recipe --background --input '{"topic": "AI"}'

# With session ID
xoneai recipe run my-recipe --background --session-id session_123
```

## Key Features

- **Async Execution**: Tasks run in the background without blocking
- **Progress Tracking**: Monitor task progress and status
- **Cancellation**: Cancel running tasks when needed
- **Result Retrieval**: Get results when tasks complete
- **Concurrency Control**: Limit concurrent tasks

## Safe Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `timeout_sec` | 300 | Maximum execution time |
| `max_concurrent` | 5 | Maximum concurrent tasks |
| `cleanup_delay_sec` | 3600 | Auto-cleanup delay |
