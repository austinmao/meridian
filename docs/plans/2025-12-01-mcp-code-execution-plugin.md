# MCP Code Execution Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fork yoloshii/mcp-code-execution-enhanced and adapt it into a Meridian-compatible Claude Code plugin with hybrid MCP server + skills/hooks architecture.

**Architecture:** The plugin will provide 99.6% token-efficient code execution via CLI-based Python scripts that call MCP tools. It integrates with Meridian's existing hook infrastructure for audit logging and skill-activator for auto-discovery. No sandbox/container isolation—direct local execution with timeout enforcement.

**Tech Stack:** Python 3.11+, UV package manager, Pydantic, MCP SDK, Claude Code plugin manifest

---

## Task 1: Fork Repository

**Files:**
- Create: Local clone of `austinmao/mcp-code-execution-meridian`

**Step 1: Fork the source repo on GitHub**

Run:
```bash
gh repo fork yoloshii/mcp-code-execution-enhanced --clone=false --fork-name mcp-code-execution-meridian
```

Expected: Success message with new repo URL at `austinmao/mcp-code-execution-meridian`

**Step 2: Clone the forked repo locally**

Run:
```bash
cd /Users/austinmao/Documents/GitHub
git clone git@github.com:austinmao/mcp-code-execution-meridian.git
cd mcp-code-execution-meridian
```

Expected: Cloned repository with full source code

**Step 3: Add upstream remote for tracking**

Run:
```bash
git remote add upstream https://github.com/yoloshii/mcp-code-execution-enhanced.git
git remote -v
```

Expected: Two remotes listed: `origin` (fork) and `upstream` (original)

**Step 4: Commit**

```bash
# No commit needed - this is just setup
```

---

## Task 2: Explore Repository Structure

**Files:**
- Read: `README.md`, `pyproject.toml`, `src/runtime/`, `tests/`

**Step 1: List top-level structure**

Run:
```bash
ls -la
```

Expected: `README.md`, `pyproject.toml`, `src/`, `tests/`, `.claude/`, `scripts/`, `docs/`

**Step 2: Identify sandbox-related files**

Run:
```bash
find . -name "*sandbox*" -o -name "*container*" | grep -v __pycache__ | grep -v .git
```

Expected: List of files to remove (likely `src/runtime/sandbox/`, related tests)

**Step 3: Review harness.py for sandbox logic**

Run:
```bash
cat src/runtime/harness.py | head -100
```

Expected: See sandbox mode selection logic to identify removal points

**Step 4: Document sandbox removal targets**

Create checklist of files/code sections to remove (no commit needed—this is research).

---

## Task 3: Remove Sandbox Directory

**Files:**
- Delete: `src/runtime/sandbox/` (entire directory)

**Step 1: Verify sandbox directory exists**

Run:
```bash
ls -la src/runtime/sandbox/
```

Expected: List of sandbox-related Python files

**Step 2: Remove sandbox directory**

Run:
```bash
rm -rf src/runtime/sandbox/
```

Expected: Directory removed (no output)

**Step 3: Verify removal**

Run:
```bash
ls src/runtime/ | grep -i sandbox
```

Expected: No output (sandbox directory gone)

**Step 4: Commit**

```bash
git add -A
git commit -m "refactor: remove sandbox directory

Meridian plugin uses direct local execution without container isolation.
Safety provided via hook-based audit logging and timeout enforcement."
```

---

## Task 4: Strip Sandbox Imports from harness.py

**Files:**
- Modify: `src/runtime/harness.py`

**Step 1: Find sandbox imports**

Run:
```bash
grep -n "sandbox\|container\|docker\|podman" src/runtime/harness.py
```

Expected: Line numbers with sandbox-related imports/code

**Step 2: Read current harness.py**

Run:
```bash
cat src/runtime/harness.py
```

Expected: Full file content to understand structure

**Step 3: Remove sandbox imports and mode selection**

Edit `src/runtime/harness.py`:
- Remove imports like `from .sandbox import ...`
- Remove sandbox mode CLI arguments
- Remove sandbox execution path in main logic
- Keep only direct execution mode

(Exact edits depend on file content from Step 2)

**Step 4: Verify syntax**

Run:
```bash
python -m py_compile src/runtime/harness.py
```

Expected: No output (clean syntax)

**Step 5: Commit**

```bash
git add src/runtime/harness.py
git commit -m "refactor: strip sandbox mode from harness.py

Direct execution only - no container/sandbox mode selection."
```

---

## Task 5: Remove Sandbox from Configuration Schema

**Files:**
- Modify: `mcp_config.example.json` or schema definition files

**Step 1: Find config schema files**

Run:
```bash
find . -name "*.json" -o -name "*config*" | grep -v node_modules | grep -v __pycache__ | head -20
```

Expected: List of config-related files

**Step 2: Read config example**

Run:
```bash
cat mcp_config.example.json 2>/dev/null || cat mcp_config.json 2>/dev/null || echo "Config file not found"
```

Expected: JSON config with sandbox section to remove

**Step 3: Remove sandbox configuration section**

Edit config files to remove `"sandbox": { ... }` blocks.

**Step 4: Update any Pydantic config models**

Run:
```bash
grep -rn "sandbox" src/ --include="*.py" | grep -v __pycache__
```

Remove sandbox fields from Pydantic models.

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor: remove sandbox from configuration schema

Simplified config: transport settings only, no container options."
```

---

## Task 6: Delete Sandbox Tests

**Files:**
- Delete: `tests/*sandbox*`, `tests/*container*`

**Step 1: Find sandbox test files**

Run:
```bash
find tests/ -name "*sandbox*" -o -name "*container*" 2>/dev/null | grep -v __pycache__
```

Expected: List of test files to remove

**Step 2: Remove sandbox test files**

Run:
```bash
find tests/ \( -name "*sandbox*" -o -name "*container*" \) -type f -delete 2>/dev/null
```

Expected: Files removed (no output)

**Step 3: Verify remaining tests**

Run:
```bash
ls tests/
```

Expected: Non-sandbox test files remain

**Step 4: Commit**

```bash
git add -A
git commit -m "test: remove sandbox-related tests

129 tests → ~100 tests after sandbox removal."
```

---

## Task 7: Run Tests to Verify Non-Sandbox Functionality

**Files:**
- Test: All remaining test files

**Step 1: Install dependencies**

Run:
```bash
uv sync
```

Expected: Dependencies installed successfully

**Step 2: Run test suite**

Run:
```bash
uv run pytest -v --tb=short 2>&1 | head -100
```

Expected: Tests run, some may fail due to sandbox import references

**Step 3: Fix broken imports**

If tests fail with import errors referencing sandbox:
- Find affected files: `grep -rn "from.*sandbox" tests/`
- Remove or update imports

**Step 4: Re-run tests until green**

Run:
```bash
uv run pytest -v
```

Expected: All remaining tests PASS

**Step 5: Commit fixes**

```bash
git add -A
git commit -m "fix: repair test imports after sandbox removal

All non-sandbox tests now passing."
```

---

## Task 8: Create Plugin Directory Structure

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/hooks/` directory
- Create: `.claude-plugin/commands/` directory

**Step 1: Create plugin directories**

Run:
```bash
mkdir -p .claude-plugin/hooks .claude-plugin/commands
```

Expected: Directories created (no output)

**Step 2: Create plugin.json manifest**

Create `.claude-plugin/plugin.json`:
```json
{
  "name": "mcp-code-execution",
  "description": "Code execution with MCP - 99.6% token efficiency via CLI scripts",
  "version": "1.0.0",
  "author": {
    "name": "Austin Mao",
    "url": "https://github.com/austinmao"
  },
  "homepage": "https://github.com/austinmao/mcp-code-execution-meridian",
  "repository": "austinmao/mcp-code-execution-meridian",
  "license": "MIT",
  "keywords": [
    "mcp",
    "code-execution",
    "automation",
    "scripts",
    "cli"
  ],
  "commands": "commands/",
  "agents": "",
  "skills": ".claude/skills/",
  "hooks": ".claude-plugin/hooks.json"
}
```

**Step 3: Verify JSON syntax**

Run:
```bash
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

Expected: No output (valid JSON)

**Step 4: Commit**

```bash
git add .claude-plugin/
git commit -m "feat: add plugin manifest structure

Meridian-compatible .claude-plugin/ with plugin.json manifest."
```

---

## Task 9: Write PreToolUse Audit Hook

**Files:**
- Create: `.claude-plugin/hooks/code-execution-audit.py`

**Step 1: Create the audit hook file**

Create `.claude-plugin/hooks/code-execution-audit.py`:
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PreToolUse hook: logs code execution requests for audit trail.
Triggers on harness/execute/run tool invocations.
"""

import sys
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    try:
        input_data = json.load(sys.stdin)

        tool = input_data.get("tool", "")
        params = input_data.get("input", {})

        # Only audit code execution tools
        tool_lower = tool.lower()
        if not any(kw in tool_lower for kw in ["execute", "run", "harness", "script"]):
            return 0  # Allow, no logging needed

        # Create audit log directory
        log_dir = Path(".claude/logs/code-execution")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Build log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "pre-execution",
            "tool": tool,
            "command": params.get("command", ""),
            "script": params.get("script", ""),
            "args": params.get("args", []),
        }

        # Check for active Meridian task
        task_file = Path(".meridian/.active-task")
        if task_file.exists():
            log_entry["task"] = task_file.read_text().strip()

        # Append to daily log file
        log_file = log_dir / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Allow execution
        return 0

    except Exception as e:
        sys.stderr.write(f"Audit hook error: {e}\n")
        return 0  # Fail open - don't block on logging errors


if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: Make executable**

Run:
```bash
chmod +x .claude-plugin/hooks/code-execution-audit.py
```

Expected: No output

**Step 3: Verify syntax**

Run:
```bash
python -m py_compile .claude-plugin/hooks/code-execution-audit.py
```

Expected: No output (valid syntax)

**Step 4: Commit**

```bash
git add .claude-plugin/hooks/code-execution-audit.py
git commit -m "feat: add PreToolUse audit hook for code execution

Logs all code execution requests to .claude/logs/code-execution/YYYY-MM-DD.jsonl"
```

---

## Task 10: Write PostToolUse Result Hook

**Files:**
- Create: `.claude-plugin/hooks/code-execution-result.py`

**Step 1: Create the result hook file**

Create `.claude-plugin/hooks/code-execution-result.py`:
```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
PostToolUse hook: logs code execution results and errors.
Captures exit codes, truncated output, and timing.
"""

import sys
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    try:
        input_data = json.load(sys.stdin)

        tool = input_data.get("tool", "")
        result = input_data.get("result", {})

        # Only audit code execution tools
        tool_lower = tool.lower()
        if not any(kw in tool_lower for kw in ["execute", "run", "harness", "script"]):
            return 0  # Skip non-execution tools

        # Create audit log directory
        log_dir = Path(".claude/logs/code-execution")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Extract result summary (truncate large outputs)
        result_str = str(result)
        if len(result_str) > 1000:
            result_str = result_str[:1000] + "... [truncated]"

        # Build log entry
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "post-execution",
            "tool": tool,
            "success": not bool(result.get("error")),
            "exit_code": result.get("exit_code", 0),
            "result_summary": result_str,
        }

        # Check for active Meridian task
        task_file = Path(".meridian/.active-task")
        if task_file.exists():
            log_entry["task"] = task_file.read_text().strip()

        # Append to daily log file
        log_file = log_dir / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        # Flag successful patterns for memory consideration
        if log_entry["success"]:
            sys.stderr.write("MEMORY: Successful execution - consider saving pattern via memory-curator\n")

        return 0

    except Exception as e:
        sys.stderr.write(f"Result hook error: {e}\n")
        return 0  # Fail open


if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: Make executable**

Run:
```bash
chmod +x .claude-plugin/hooks/code-execution-result.py
```

Expected: No output

**Step 3: Verify syntax**

Run:
```bash
python -m py_compile .claude-plugin/hooks/code-execution-result.py
```

Expected: No output (valid syntax)

**Step 4: Commit**

```bash
git add .claude-plugin/hooks/code-execution-result.py
git commit -m "feat: add PostToolUse result hook for code execution

Logs execution results, flags successful patterns for memory-curator."
```

---

## Task 11: Create hooks.json Hook Registration

**Files:**
- Create: `.claude-plugin/hooks.json`

**Step 1: Create hooks.json**

Create `.claude-plugin/hooks.json`:
```json
[
  {
    "event": "PreToolUse",
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "\"${CLAUDE_PLUGIN_ROOT}\"/.claude-plugin/hooks/code-execution-audit.py"
      }
    ]
  },
  {
    "event": "PostToolUse",
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "\"${CLAUDE_PLUGIN_ROOT}\"/.claude-plugin/hooks/code-execution-result.py"
      }
    ]
  }
]
```

**Step 2: Verify JSON syntax**

Run:
```bash
python -c "import json; json.load(open('.claude-plugin/hooks.json'))"
```

Expected: No output (valid JSON)

**Step 3: Commit**

```bash
git add .claude-plugin/hooks.json
git commit -m "feat: register audit hooks in hooks.json

PreToolUse and PostToolUse hooks for Bash command auditing."
```

---

## Task 12: Create Init Command

**Files:**
- Create: `.claude-plugin/commands/init-code-execution.md`

**Step 1: Create the init command**

Create `.claude-plugin/commands/init-code-execution.md`:
```markdown
# Initialize MCP Code Execution

Set up the MCP code execution environment in the current project.

## Steps

1. Create scripts directory if it doesn't exist:
   ```bash
   mkdir -p scripts
   ```

2. Copy example MCP config:
   ```bash
   cp "${CLAUDE_PLUGIN_ROOT}/mcp_config.example.json" ./mcp_config.json
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Create logs directory:
   ```bash
   mkdir -p .claude/logs/code-execution
   ```

5. Verify installation:
   ```bash
   uv run python -c "from runtime.mcp_client import MCPClient; print('MCP client ready')"
   ```

## Usage

After initialization, execute scripts via:
```bash
uv run python -m runtime.harness scripts/your_script.py --arg1 value1
```

See `.claude/skills/` for available skill patterns.
```

**Step 2: Commit**

```bash
git add .claude-plugin/commands/init-code-execution.md
git commit -m "feat: add /init-code-execution command

Scaffolds project for MCP code execution with config and dependencies."
```

---

## Task 13: Update SKILL.md Files with Auto-Activation

**Files:**
- Modify: `.claude/skills/*/SKILL.md`

**Step 1: List existing skills**

Run:
```bash
ls -la .claude/skills/
```

Expected: List of skill directories (e.g., `simple-fetch/`, `multi-tool-pipeline/`)

**Step 2: Read existing SKILL.md**

Run:
```bash
cat .claude/skills/simple-fetch/SKILL.md 2>/dev/null || echo "No SKILL.md found"
```

Expected: Current SKILL.md content or error

**Step 3: Update SKILL.md with auto-activation frontmatter**

For each skill, ensure YAML frontmatter includes:
```yaml
---
name: simple-fetch
description: Single-tool MCP execution pattern
auto_activate:
  triggers:
    - fetch data
    - api call
    - single tool
---
```

**Step 4: Commit**

```bash
git add .claude/skills/
git commit -m "feat: add auto-activation triggers to skill frontmatter

Skills now auto-activate via skill-activator.py on matching prompts."
```

---

## Task 14: Create skill-rules.json for Plugin

**Files:**
- Create: `.claude-plugin/skill-rules.json`

**Step 1: Create skill-rules.json**

Create `.claude-plugin/skill-rules.json`:
```json
{
  "code-execution": {
    "triggers": [
      "execute code",
      "run script",
      "python script",
      "data processing",
      "mcp tool",
      "workflow automation",
      "harness"
    ],
    "skill_path": "${CLAUDE_PLUGIN_ROOT}/.claude/skills/code-execution/"
  },
  "simple-fetch": {
    "triggers": [
      "fetch data",
      "api call",
      "single tool",
      "get document"
    ],
    "skill_path": "${CLAUDE_PLUGIN_ROOT}/.claude/skills/simple-fetch/"
  },
  "multi-tool-pipeline": {
    "triggers": [
      "pipeline",
      "multi-tool",
      "chain tools",
      "workflow"
    ],
    "skill_path": "${CLAUDE_PLUGIN_ROOT}/.claude/skills/multi-tool-pipeline/"
  }
}
```

**Step 2: Verify JSON syntax**

Run:
```bash
python -c "import json; json.load(open('.claude-plugin/skill-rules.json'))"
```

Expected: No output (valid JSON)

**Step 3: Commit**

```bash
git add .claude-plugin/skill-rules.json
git commit -m "feat: add skill-rules.json for auto-activation

Maps trigger phrases to skill paths for skill-activator integration."
```

---

## Task 15: Update README for Plugin Installation

**Files:**
- Modify: `README.md`

**Step 1: Read current README**

Run:
```bash
head -100 README.md
```

Expected: Current README content

**Step 2: Add plugin installation section**

Add to README.md (after existing installation section):
```markdown
## Plugin Installation (Meridian/Claude Code)

### Quick Install

```bash
# Add basecamp marketplace (one-time)
/plugin marketplace add austinmao/basecamp

# Install plugin
/plugin install mcp-code-execution@basecamp
```

### Manual Install

Add to your `~/.claude.json`:
```json
{
  "plugins": [
    "github:austinmao/mcp-code-execution-meridian"
  ]
}
```

Then initialize in your project:
```
/init-code-execution
```

### Features

- **99.6% token reduction** via CLI scripts pattern
- **Audit logging** via PreToolUse/PostToolUse hooks
- **Auto-activation** via skill-rules.json triggers
- **Meridian integration** for task context and memory
```

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add plugin installation instructions

Documents both quick install via basecamp and manual configuration."
```

---

## Task 16: Add Marketplace Metadata to plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

**Step 1: Read current plugin.json**

Run:
```bash
cat .claude-plugin/plugin.json
```

Expected: Current manifest content

**Step 2: Add marketplace section**

Add to `.claude-plugin/plugin.json`:
```json
{
  "marketplace": {
    "category": "code-execution",
    "tags": ["mcp", "automation", "scripts", "cli", "python"],
    "featured": false
  }
}
```

**Step 3: Verify JSON syntax**

Run:
```bash
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
```

Expected: No output (valid JSON)

**Step 4: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: add marketplace metadata to plugin.json

Ready for basecamp marketplace registration."
```

---

## Task 17: Push Fork to GitHub

**Files:**
- None (git operations only)

**Step 1: Verify all commits**

Run:
```bash
git log --oneline -15
```

Expected: All commits from Tasks 3-16

**Step 2: Push to origin**

Run:
```bash
git push origin main
```

Expected: Push successful

**Step 3: Verify on GitHub**

Run:
```bash
gh repo view austinmao/mcp-code-execution-meridian --web
```

Expected: Browser opens to repo with all changes visible

---

## Task 18: Register in Basecamp Marketplace

**Files:**
- Modify: `austinmao/basecamp/marketplace.json` (separate repo)

**Step 1: Clone basecamp repo**

Run:
```bash
cd /Users/austinmao/Documents/GitHub
git clone git@github.com:austinmao/basecamp.git 2>/dev/null || cd basecamp && git pull
cd basecamp
```

Expected: Basecamp repo cloned or updated

**Step 2: Read current marketplace.json**

Run:
```bash
cat marketplace.json
```

Expected: Current marketplace content

**Step 3: Add mcp-code-execution plugin**

Add to `marketplace.json` plugins array:
```json
{
  "name": "mcp-code-execution",
  "description": "Code execution with MCP - 99.6% token efficiency via CLI scripts",
  "source": "github:austinmao/mcp-code-execution-meridian",
  "version": "1.0.0",
  "author": "austinmao",
  "tags": ["mcp", "automation", "scripts"]
}
```

**Step 4: Commit and push**

```bash
git add marketplace.json
git commit -m "feat: add mcp-code-execution plugin to marketplace"
git push origin main
```

Expected: Push successful

---

## Task 19: Test Plugin Installation

**Files:**
- Test in a fresh project directory

**Step 1: Create test directory**

Run:
```bash
cd /tmp
mkdir mcp-test-project
cd mcp-test-project
git init
```

Expected: Empty git repo initialized

**Step 2: Install plugin (simulate)**

Run:
```bash
# Create minimal .claude.json to test plugin reference
echo '{"plugins": ["github:austinmao/mcp-code-execution-meridian"]}' > .claude.json
```

Expected: Config created

**Step 3: Verify plugin structure accessible**

Run:
```bash
# Verify repo is accessible
gh repo view austinmao/mcp-code-execution-meridian --json name
```

Expected: JSON output with repo name

**Step 4: Clean up test**

Run:
```bash
cd /Users/austinmao/Documents/GitHub/mcp-code-execution-meridian
rm -rf /tmp/mcp-test-project
```

Expected: Cleanup complete

---

## Task 20: Final Verification and Push

**Files:**
- All plugin files

**Step 1: Run full test suite**

Run:
```bash
uv run pytest -v
```

Expected: All tests PASS

**Step 2: Verify plugin structure**

Run:
```bash
ls -la .claude-plugin/
cat .claude-plugin/plugin.json
```

Expected: Complete plugin structure visible

**Step 3: Create release tag**

Run:
```bash
git tag -a v1.0.0 -m "Initial Meridian plugin release

- Forked from yoloshii/mcp-code-execution-enhanced
- Removed sandbox/container isolation
- Added .claude-plugin/ manifest structure
- Added audit hooks (PreToolUse/PostToolUse)
- Added skill-rules.json for auto-activation
- Added /init-code-execution command
- Registered in basecamp marketplace"
git push origin v1.0.0
```

Expected: Tag created and pushed

**Step 4: Commit any final changes**

```bash
git status
# If changes exist:
git add -A
git commit -m "chore: final cleanup for v1.0.0 release"
git push origin main
```

---

## Validation Checklist

After completing all tasks, verify:

- [ ] Fork exists at `austinmao/mcp-code-execution-meridian`
- [ ] No `src/runtime/sandbox/` directory exists
- [ ] `uv run pytest -v` passes all tests
- [ ] `.claude-plugin/plugin.json` has valid schema
- [ ] `.claude-plugin/hooks.json` registers audit hooks
- [ ] `.claude-plugin/hooks/code-execution-audit.py` exists and is executable
- [ ] `.claude-plugin/hooks/code-execution-result.py` exists and is executable
- [ ] `.claude-plugin/commands/init-code-execution.md` exists
- [ ] `.claude-plugin/skill-rules.json` has trigger mappings
- [ ] README documents plugin installation
- [ ] Plugin registered in `austinmao/basecamp/marketplace.json`
- [ ] Git tag `v1.0.0` exists and is pushed

---

Plan complete and saved to `docs/plans/2025-12-01-mcp-code-execution-plugin.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
