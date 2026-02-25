# XoneAI Persistence CLI - End-to-End Guide

This guide demonstrates the CLI commands for database persistence.

## Prerequisites

```bash
pip install "xoneai[tools]"

# Start Docker containers
docker run -d --name xone-postgres -p 5432:5432 \
    -e POSTGRES_PASSWORD=xonevn123 \
    -e POSTGRES_DB=xoneai \
    postgres:16

docker run -d --name xone-qdrant -p 6333:6333 qdrant/qdrant
docker run -d --name xone-redis -p 6379:6379 redis:7
```

## 1. Doctor Command - Validate Connectivity

```bash
# Check all stores
xoneai persistence doctor \
    --conversation-url "postgresql://postgres:xonevn123@localhost:5432/xoneai" \
    --knowledge-url "http://localhost:6333" \
    --state-url "redis://localhost:6379"
```

**Expected Output:**
```
==================================================
XoneAI Persistence Doctor
==================================================

[Conversation Store] Testing: postgresql://postgres:****@localhost:5432/xoneai
  ✅ Connected (postgres)

[Knowledge Store] Testing: http://localhost:6333
  ✅ Connected (qdrant)

[State Store] Testing: redis://localhost:6379
  ✅ Connected (redis)

==================================================
Results: 3/3 stores connected successfully
==================================================
```

## 2. Run Command - Execute Agent with Persistence

```bash
# Run agent with persistence (dry-run first)
xoneai persistence run \
    --session-id "cli-demo-001" \
    --conversation-url "postgresql://postgres:xonevn123@localhost:5432/xoneai" \
    --dry-run \
    "Hello, my name is Bob"

# Actually run it
xoneai persistence run \
    --session-id "cli-demo-001" \
    --conversation-url "postgresql://postgres:xonevn123@localhost:5432/xoneai" \
    "Hello, my name is Bob"
```

**Expected Output:**
```
[Session: cli-demo-001]
Agent: Hello Bob! Nice to meet you. How can I help you today?
```

## 3. Resume Command - Continue a Session

```bash
# Show history
xoneai persistence resume \
    --session-id "cli-demo-001" \
    --conversation-url "postgresql://postgres:xonevn123@localhost:5432/xoneai" \
    --show-history

# Continue conversation
xoneai persistence resume \
    --session-id "cli-demo-001" \
    --conversation-url "postgresql://postgres:xonevn123@localhost:5432/xoneai" \
    --continue "What's my name?"
```

**Expected Output:**
```
[Session: cli-demo-001]
Messages in history: 2

--- Conversation History ---
[USER] Hello, my name is Bob
[ASSISTANT] Hello Bob! Nice to meet you...
--- End History ---

Agent: Your name is Bob!
```

## Environment Variables

Instead of passing URLs on command line, use environment variables:

```bash
export XONE_CONVERSATION_URL="postgresql://postgres:xonevn123@localhost:5432/xoneai"
export XONE_KNOWLEDGE_URL="http://localhost:6333"
export XONE_STATE_URL="redis://localhost:6379"
export OPENAI_API_KEY="your-key"

# Now commands are simpler
xoneai persistence doctor --all
xoneai persistence run --session-id "my-session" "Hello!"
```

## Full CLI Reference

```
xoneai persistence --help
xoneai persistence doctor --help
xoneai persistence run --help
xoneai persistence resume --help
```
