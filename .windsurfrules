# XoneAI Coding Conventions and AI Agent Instructions

Welcome, AI coding assistant! You are contributing to **XoneAI**, a production-ready Multi-AI Agents framework with self-reflection. This repository contains Python (`src/xoneai/`, `src/xoneai-agents/`), TypeScript (`src/xoneai-ts/`), and Rust (`src/xoneai-rust/`) packages.

## 🤖 General Agent Instructions
- **Context:** Always evaluate changes in the context of the entire multi-language workspace.
- **Conciseness:** Provide minimal, precise, and immediately actionable answers.
- **Completeness:** When writing code, output complete functions, classes, or files without truncating. Give full context.
- **Safety:** Do NOT commit sensitive data (API keys, secrets). Use `os.environ.get()` or `.env` files.
- **No Hallucination:** Only use modules and classes that exist in the codebase or standard libraries. Verify dependencies in `pyproject.toml`, `Cargo.toml`, or `package.json`.

## 🐍 Python Conventions (`src/xoneai/`, `src/xoneai-agents/`)
- **Version:** Python 3.10+ is supported.
- **Typing:** Use extensive type hinting from the `typing` module (`List`, `Dict`, `Optional`, `Any`, `Callable`, etc.).
- **Docstrings:** Use clear and descriptive docstrings for modules, classes, and complex functions.
- **Formatting & Style:** Adhere strictly to PEP 8 standards. Assume standard formatting tools (Black/Ruff) will run.
- **Async/Await:** Emphasize asynchronous operations wherever network calls, API requests, or IO bounds exist (e.g., `async def`, `await asyncio.gather()`).
- **Dependencies:** Avoid adding unnecessary third-party dependencies. When necessary, update `pyproject.toml` and ensure they are cross-platform compatible.
- **Logging vs Print:** Do not use plain `print()` statements for production logic. Use the `logging` module or `rich.console` for beautiful CLI outputs.
- **Pydantic:** Extensively use Pydantic models for structured data validation and agent output parsing.

## 🔷 TypeScript Conventions (`src/xoneai-ts/`)
- **Strict Typing:** Employ strict TypeScript typing. Avoid `any` unless absolutely necessary.
- **Interfaces & Types:** Define clear interfaces for all configuration objects and API responses.
- **Exporting:** Explicitly export public-facing classes and unexport internal utility functions.
- **Promises:** Prefer `async/await` syntax over raw `.then()` chaining.
- **Style:** Standard Prettier formatting rules apply.

## 🦀 Rust Conventions (`src/xoneai-rust/`)
- **Idiomatic Rust:** Follow idiomatic Rust practices (Clippy lints must pass).
- **Error Handling:** Use `Result` and `Option` properly. Avoid unwrapping `unwrap()` in production code where possible; handle errors explicitly or bubble them up with `?`.
- **Async:** Use `tokio` for async runtimes.
- **Traits:** Leverage traits for defining shared behavior between agents or tool integrations.

## 🛠️ Modifying Framework Architecture
- **Agents.yaml & Workflow.yaml:** Be aware of the `agents.yaml` and `workflow.yaml` parsing structures described in the documentation. Any changes to workflow steps must be backward-compatible with canonical field names (`agents`, `instructions`, `action`, `steps`).
- **Backwards Compatibility:** Maintaining API backward compatibility is crucial since XoneAI is published globally.
- **Tool Creation:** When creating new custom tools, subclass `BaseTool` or use the `@tool` decorator, and ensure inputs/outputs are strongly typed with descriptions.

## ✅ Testing & Verification
- Before presenting final changes, ensure they do not break existing tests.
- For Python, use `pytest`. Recommend creating test files (`tests/`) alongside new features.
