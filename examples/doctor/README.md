# XoneAI Doctor Examples

Examples demonstrating the XoneAI Doctor health check and diagnostics system.

## CLI Examples

| Command | Description |
|---------|-------------|
| `xoneai doctor` | Run all fast health checks |
| `xoneai doctor --version` | Show doctor version |
| `xoneai doctor --list-checks` | List all available checks |
| `xoneai doctor env` | Check environment configuration |
| `xoneai doctor config` | Validate configuration files |
| `xoneai doctor tools` | Check tool availability |
| `xoneai doctor db` | Check database drivers |
| `xoneai doctor mcp` | Check MCP configuration |
| `xoneai doctor obs` | Check observability providers |
| `xoneai doctor skills` | Check agent skills |
| `xoneai doctor memory` | Check memory storage |
| `xoneai doctor permissions` | Check filesystem permissions |
| `xoneai doctor network` | Check network connectivity |
| `xoneai doctor performance` | Check import times |
| `xoneai doctor ci` | CI mode with JSON output |
| `xoneai doctor selftest` | Test agent functionality |

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output in JSON format |
| `--format text\|json` | Output format |
| `--output PATH` | Write report to file |
| `--deep` | Enable deeper probes |
| `--timeout SEC` | Per-check timeout |
| `--strict` | Treat warnings as failures |
| `--quiet` | Minimal output |
| `--no-color` | Disable colors |
| `--only IDS` | Only run these checks |
| `--skip IDS` | Skip these checks |

## Python Examples

| File | Description |
|------|-------------|
| [basic_doctor.py](basic_doctor.py) | Programmatic health checks |
| [ci_integration.py](ci_integration.py) | CI/CD pipeline integration |

## Quick Start

```bash
# Run basic health checks
xoneai doctor

# Run with JSON output
xoneai doctor --json

# Run specific checks
xoneai doctor --only python_version,openai_api_key

# CI mode
xoneai doctor ci

# Save report to file
xoneai doctor --output report.json
```
