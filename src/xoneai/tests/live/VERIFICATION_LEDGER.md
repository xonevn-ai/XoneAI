# AI Code Editor Smoke Test Verification Ledger

**Date**: January 2026  
**Status**: VERIFIED  

## CLI Contract Table

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `xoneai chat` | Terminal-native REPL | `-m`, `-w`, `-f`, `-c`, `-s`, `--no-acp`, `--no-lsp` |
| `xoneai code` | Terminal-native code assistant | `-m`, `-w`, `-f`, `-c`, `-s`, `--no-acp`, `--no-lsp` |
| `xoneai tui` | Full TUI interface | `-w`, `-s`, `-m`, `-d`, `--log-jsonl` |
| `xoneai ui chat` | Browser-based chat | `--port`, `--host`, `--public` |
| `xoneai ui code` | Browser-based code | `--port`, `--host`, `--public` |
| `xoneai session list` | List sessions | - |
| `xoneai session export` | Export session | `--output` |
| `xoneai session import` | Import session | - |

## Approval Automation Mechanism

- **Environment Variable**: `XONE_APPROVAL_MODE=auto`
- **Effect**: Auto-approves all tool executions for non-interactive automation
- **Files Modified**:
  - `xoneai/cli/main.py` - Added env var check in `_process_interactive_prompt` and `_start_execution_worker`
  - `xoneai/cli/features/interactive_runtime.py` - Modified `read_only` property to bypass when auto mode

## Scenario Table (10 Scenarios)

| # | Scenario Name | CLI Command | Acceptance Checks | Status |
|---|---------------|-------------|-------------------|--------|
| 1 | implement_celsius_to_fahrenheit | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | function_exists, has_formula, tests_pass | PASS |
| 2 | fix_divide_by_zero | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | has_error_message, tests_pass | PASS |
| 3 | implement_mode_function | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | tests_pass | PASS |
| 4 | fix_mean_empty_list | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | has_error_message, tests_pass | PASS |
| 5 | add_cli_version_command | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | has_version_command, version_works | PASS |
| 6 | fix_lint_errors | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | ruff_clean | PASS |
| 7 | implement_fahrenheit_to_celsius | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | function_exists, tests_pass | PASS |
| 8 | fix_median_empty_list | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | has_error_message, tests_pass | PASS |
| 9 | add_type_hints_calculator | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | has_return_type, has_param_types | PASS |
| 10 | make_all_tests_pass | `xoneai code -m gpt-4o-mini -w <workspace> "<prompt>"` | all_tests_pass | PASS |

## Files Modified

### CLI Fixes
- `xoneai/cli/main.py` - Added XONE_APPROVAL_MODE=auto support, fixed import error handling
- `xoneai/cli/features/interactive_runtime.py` - Modified read_only property for auto mode
- `xoneai/api.py` - Fixed circular import

### Test Infrastructure
- `tests/live/runner.py` - CLI-first runner using `python -m xoneai code`
- `tests/live/scenarios/__init__.py` - 10 scenario definitions with acceptance checks
- `tests/live/test_ai_code_editor_smoke.py` - Pytest test suite

### Fixture
- `tests/fixtures/ai_code_editor_fixture/` - Single fixture template with intentional bugs

### Documentation
- `XoneAIDocs/docs/cli/realworld-examples.mdx` - Updated with CLI contract and scenarios

## Environment Guards

```bash
# Required for live tests
XONEAI_LIVE_SMOKE=1
OPENAI_API_KEY=<your-key>

# Optional
XONEAI_LIVE_MODEL=gpt-4o-mini  # Default model
XONE_APPROVAL_MODE=auto        # Auto-approve tools
```

## Run Commands

```bash
# Run all live smoke tests
XONEAI_LIVE_SMOKE=1 pytest tests/live/test_ai_code_editor_smoke.py -v

# Run single scenario
XONEAI_LIVE_SMOKE=1 pytest tests/live/test_ai_code_editor_smoke.py::TestIndividualScenarios::test_scenario_2_fix_divide_bug -v

# Run fixture verification only
XONEAI_LIVE_SMOKE=1 pytest tests/live/test_ai_code_editor_smoke.py::TestAICodeEditorSmoke::test_fixture_has_failing_tests -v
```

## Deprecated Flags (Removed)

- `--interactive` / `-i` - Use `xoneai chat` instead
- `--chat-mode` / `--chat` - Use `xoneai chat` instead
- `tui launch` - Use `xoneai tui` directly

## Missing = 0

All 10 scenarios defined and verified with CLI-first approach.
