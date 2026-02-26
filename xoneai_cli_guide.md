# 🚀 XoneAI CLI Quick Guide

XoneAI comes with a powerful Command-Line Interface (CLI) that provides various ways to interact with agents, workflows, and more!

## 0. Quick Setup (API Key)
Before using XoneAI, you must set an API key for your chosen LLM provider. The default model is `gpt-4o-mini`, which requires an OpenAI API key.

**Option A: Set an environment variable in your terminal**
```powershell
# PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Command Prompt (CMD)
set OPENAI_API_KEY=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
```

**Option B: Create a `.env` file** in your working directory:
```env
OPENAI_API_KEY=your-api-key-here
```

## 1. Interactive Mode
Starts an interactive terminal-based AI assistant with built-in tools (file editing, web search, command execution, and code intelligence).

```bash
xoneai --interactive
# or simply
xoneai -i
```
*Note: Works best when exploring your project. Use `/help` inside for available slash commands.*

## 2. Auto Mode
Provide a prompt directly, and the AI agent will automatically figure out how to solve it.

```bash
xoneai --auto "create a Python script that scrapes HackerNews"
```

## 3. Workflow Mode
Execute pre-defined workflows (e.g. from `workflow.yaml` or `agents.yaml`) or run inline workflows.

```bash
# Run a specific YAML workflow
xoneai workflow run agents.yaml

# Create an inline workflow with tools
xoneai "Research Python 3.13" --workflow "Search info, Summarize findings" --tools tavily
```

## 4. Deep Research Mode
Perform deep, multi-step research on complex topics.

```bash
xoneai research "What are the latest AI trends in 2025?"
# Add --save to write findings to a file!
```

## 5. Built-in Tools
Need to see what tools your agents can use?

```bash
xoneai tools list
```

## 6. Model / Provider Support
XoneAI supports 100+ LLMs. Just export your API key (e.g. `OPENAI_API_KEY`) and optionally the base URL (for Ollama, Groq, etc.):

```bash
# Example for passing a specific model
xoneai --auto "explain rust macros" --llm openai/gpt-4o-mini
```

---
**Tip:** Run `xoneai --help` to see all available flags and commands!
