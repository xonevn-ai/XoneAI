#!/bin/bash
# MCP CLI Tools Examples
#
# Demonstrates the new CLI commands for MCP tool management:
# - xoneai mcp tools search
# - xoneai mcp tools info
# - xoneai mcp tools schema
# - xoneai mcp list-tools (with pagination)
#
# Usage:
#   chmod +x cli_tools_example.sh
#   ./cli_tools_example.sh

echo "========================================"
echo "MCP CLI Tools Examples"
echo "MCP Protocol Version: 2025-11-25"
echo "========================================"

echo ""
echo "--- List Tools (with pagination) ---"
echo "Command: xoneai mcp list-tools --limit 5"
xoneai mcp list-tools --limit 5

echo ""
echo "--- List Tools (JSON output) ---"
echo "Command: xoneai mcp list-tools --json --limit 3"
xoneai mcp list-tools --json --limit 3

echo ""
echo "--- Tools Help ---"
echo "Command: xoneai mcp tools --help"
xoneai mcp tools --help

echo ""
echo "--- Search Tools ---"
echo "Command: xoneai mcp tools search 'workflow'"
xoneai mcp tools search "workflow"

echo ""
echo "--- Search Read-Only Tools ---"
echo "Command: xoneai mcp tools search --read-only"
xoneai mcp tools search --read-only

echo ""
echo "--- Search with JSON Output ---"
echo "Command: xoneai mcp tools search 'memory' --json"
xoneai mcp tools search "memory" --json

echo ""
echo "========================================"
echo "Examples completed!"
echo "========================================"
