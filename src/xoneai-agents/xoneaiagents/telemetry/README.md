# XoneAI Agents Telemetry

This module provides minimal, privacy-focused telemetry for XoneAI Agents.

## Privacy Guarantees

- **No personal data is collected** - No prompts, responses, or user content
- **Anonymous metrics only** - Usage counts and feature adoption
- **Disabled by default** - Requires explicit opt-in to enable
- **Transparent collection** - See exactly what's tracked below

## What We Collect

We collect only anonymous usage metrics:
- Number of agent executions
- Number of task completions  
- Tool usage (names only, no arguments)
- Error types (no error messages)
- Framework version and OS type
- Anonymous session ID (regenerated each run)

## Enabling Telemetry

**NEW BEHAVIOR**: Telemetry is now **disabled by default** for better privacy. To enable telemetry, you must explicitly opt-in.

### 1. Environment Variables (Recommended)

To enable telemetry, set any of these environment variables:
```bash
export XONEAI_TELEMETRY_ENABLED=true
export XONEAI_PERFORMANCE_ENABLED=true
```

### Legacy Disable Flags (Still Supported)

The legacy disable flags still work for backward compatibility:
```bash
export XONEAI_TELEMETRY_DISABLED=true
export XONEAI_DISABLE_TELEMETRY=true
export DO_NOT_TRACK=true  # Universal standard
export XONEAI_PERFORMANCE_DISABLED=true
```

### 2. Programmatically Enable

```python
from xoneaiagents.telemetry import enable_telemetry
enable_telemetry()
```

### 3. At Runtime

```python
from xoneaiagents.telemetry import get_telemetry
telemetry = get_telemetry()
telemetry.enabled = True  # Enable telemetry (disabled by default)
```

### 4. Programmatically Disable (Legacy)

```python
from xoneaiagents.telemetry import disable_telemetry
disable_telemetry()
```

## Usage

The telemetry module integrates automatically with XoneAI Agents:

```python
import os
from xoneaiagents import Agent, Task, XoneAIAgents

# Enable telemetry (disabled by default)
os.environ['XONEAI_TELEMETRY_ENABLED'] = 'true'

agent = Agent(name="MyAgent", role="Assistant")
task = Task(description="Help user", agent=agent)

workflow = XoneAIAgents(agents=[agent], tasks=[task])
result = workflow.start()

# Check telemetry metrics
from xoneaiagents.telemetry import get_telemetry
telemetry = get_telemetry()
print(telemetry.get_metrics())
```

## Implementation Details

The telemetry implementation is minimal and lightweight:
- No external dependencies required
- No network calls in current implementation
- Metrics stored in memory only
- Future versions may send to PostHog or similar privacy-focused services

## Backward Compatibility

The module maintains compatibility with the previous telemetry interface:

```python
from xoneaiagents.telemetry import TelemetryCollector

collector = TelemetryCollector()
collector.start()

with collector.trace_agent_execution("MyAgent"):
    # Agent execution code
    pass

collector.stop()
```

## Contributing

When contributing to telemetry:
1. Never collect personal data or user content
2. Always make new metrics opt-out
3. Document what's collected
4. Keep the implementation minimal

## Future Plans

- Integration with PostHog for anonymous analytics
- Aggregate usage statistics dashboard
- Opt-in detailed performance metrics
- Self-hosted telemetry endpoint option