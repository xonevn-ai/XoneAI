# Recipe Async Jobs Example

This example demonstrates how to submit recipes as async jobs to a jobs server.

## Prerequisites

```bash
pip install xoneai xoneaiagents httpx uvicorn
export OPENAI_API_KEY="your-api-key"
```

## Start the Jobs Server

```bash
python -m uvicorn xoneai.jobs.server:create_app --port 8005 --factory
```

## Python Example

```bash
python example_jobs.py
```

## CLI Examples

### Submit a job

```bash
# Basic submission
xoneai run submit "Analyze AI trends"

# Submit with recipe
xoneai run submit "Analyze news" --recipe news-analyzer

# Wait for completion
xoneai run submit "Quick task" --wait

# Stream progress
xoneai run submit "Long task" --stream

# With webhook
xoneai run submit "Task" --webhook-url https://example.com/callback

# With idempotency
xoneai run submit "Task" --idempotency-key order-123

# With metadata
xoneai run submit "Task" --metadata user=john --metadata priority=high
```

### Check status

```bash
xoneai run status <job_id>
xoneai run status <job_id> --json
```

### Get result

```bash
xoneai run result <job_id>
xoneai run result <job_id> --json
```

### Stream progress

```bash
xoneai run stream <job_id>
```

### List jobs

```bash
xoneai run list
xoneai run list --status running
```

### Cancel job

```bash
xoneai run cancel <job_id>
```

## Key Features

- **Server-based**: Jobs persist across restarts
- **Webhooks**: Get notified when jobs complete
- **Idempotency**: Prevent duplicate submissions
- **Streaming**: Real-time progress updates
- **Metadata**: Attach custom data to jobs

## Safe Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `timeout` | 3600 | Maximum execution time (1 hour) |
| `api_url` | http://127.0.0.1:8005 | Jobs server URL |
