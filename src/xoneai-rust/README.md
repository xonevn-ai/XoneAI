# XoneAI Rust SDK

High-performance, agentic AI framework for Rust.

## Quick Start

```rust
use xoneai::{Agent, tool, Tool};

#[tool(description = "Search the web")]
async fn search(query: String) -> String {
    format!("Results for: {}", query)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let agent = Agent::new()
        .instructions("You are a helpful assistant")
        .tool(SearchTool::new())
        .build()?;
    
    let response = agent.chat("Hello!").await?;
    println!("{}", response);
    Ok(())
}
```

## Installation

Add to your `Cargo.toml`:

```toml
[dependencies]
xoneai = "0.1"
tokio = { version = "1", features = ["full"] }
```

## CLI Usage

```bash
# Install CLI
cargo install xoneai-cli

# Interactive chat
xoneai-rust chat

# Single-shot prompt
xoneai-rust "What is 2+2?"

# Run workflow from YAML
xoneai-rust run agents.yaml
```

## Features

- **Agent-Centric**: Every design decision centers on Agents
- **Multi-Provider LLM**: OpenAI, Anthropic, Ollama support via rig-core
- **Tool System**: `#[tool]` macro for easy tool creation
- **Multi-Agent Workflows**: AgentTeam, AgentFlow patterns
- **Memory**: Conversation history and long-term storage
- **Async-First**: Built on Tokio for high performance

## Crates

| Crate | Description |
|-------|-------------|
| `xoneai` | Core library (Agent, Tools, Workflows) |
| `xoneai-derive` | Proc macros (`#[tool]`) |
| `xoneai-cli` | CLI binary |

## API Parity with Python

```python
# Python
from xoneaiagents import Agent, tool

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

agent = Agent(instructions="Be helpful", tools=[search])
response = agent.start("Hello!")
```

```rust
// Rust
use xoneai::{Agent, tool, Tool};

#[tool(description = "Search the web")]
async fn search(query: String) -> String {
    format!("Results for: {}", query)
}

let agent = Agent::new()
    .instructions("Be helpful")
    .tool(SearchTool::new())
    .build()?;
let response = agent.chat("Hello!").await?;
```

## License

MIT
