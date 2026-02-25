# Persistence CLI Commands

## Quick Reference

```bash
# Check database connectivity
xoneai persistence doctor \
  --conversation-url postgresql://localhost:5432/xoneai \
  --state-url redis://localhost:6379

# Run agent with persistence
xoneai persistence run \
  --conversation-url postgresql://localhost:5432/xoneai \
  --session-id my-session

# Resume a session
xoneai persistence resume \
  --conversation-url postgresql://localhost:5432/xoneai \
  --session-id my-session

# Export session to file
xoneai persistence export \
  --conversation-url postgresql://localhost:5432/xoneai \
  --session-id my-session \
  --output session_backup.jsonl

# Import session from file
xoneai persistence import \
  --conversation-url postgresql://localhost:5432/xoneai \
  --file session_backup.jsonl

# Check schema status
xoneai persistence status \
  --conversation-url postgresql://localhost:5432/xoneai \
  --state-url redis://localhost:6379

# Apply migrations
xoneai persistence migrate \
  --conversation-url postgresql://localhost:5432/xoneai \
  --state-url redis://localhost:6379
```

## Environment Variables

Instead of CLI flags, you can use environment variables:

```bash
export XONE_CONVERSATION_URL=postgresql://localhost:5432/xoneai
export XONE_STATE_URL=redis://localhost:6379
export XONE_KNOWLEDGE_URL=http://localhost:6333

# Then run without URL flags
xoneai persistence doctor
xoneai persistence status
```

## Docker Setup

```bash
# Start all services
docker run -d --name xone-postgres \
  -e POSTGRES_PASSWORD=xonevn123 \
  -e POSTGRES_DB=xoneai \
  -p 5432:5432 postgres:16

docker run -d --name xone-redis \
  -p 6379:6379 redis:7

docker run -d --name xone-qdrant \
  -p 6333:6333 -p 6334:6334 qdrant/qdrant

# Verify
docker ps
```

## Example Workflow

```bash
# 1. Start services
docker-compose up -d

# 2. Check connectivity
xoneai persistence doctor

# 3. Run agent
xoneai persistence run --session-id demo-session

# 4. Export for backup
xoneai persistence export --session-id demo-session --output backup.jsonl

# 5. Import to another environment
xoneai persistence import --file backup.jsonl
```
