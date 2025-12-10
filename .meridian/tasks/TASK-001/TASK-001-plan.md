# Implementation Plan  TASK-001

**Approved**: 2025-11-29
**Approach**: Fork and adapt yoloshii/mcp-code-execution-enhanced

---

## Phase 1: Fork and Strip (R1)

### 1.1 Create Fork
```bash
# Fork yoloshii/mcp-code-execution-enhanced to austinmao/mcp-code-execution-meridian
gh repo fork yoloshii/mcp-code-execution-enhanced --clone --remote-name upstream
cd mcp-code-execution-meridian
```

### 1.2 Remove Sandbox Code
- Delete `src/runtime/sandbox/` directory entirely
- Edit `src/runtime/harness.py`:
  - Remove sandbox mode selection
  - Remove sandbox-related imports
  - Keep direct execution mode only
- Edit `mcp_config.json` schema:
  - Remove `sandbox` configuration section
  - Simplify to transport-only config

### 1.3 Update Tests
- Delete sandbox-related test files in `tests/`
- Run remaining tests: `uv run pytest`
- Fix any broken imports referencing sandbox modules

---

## Phase 2: Restructure for Plugin Format (R2)

### 2.1 Create Plugin Manifest
Create `.claude-plugin/plugin.json`:
```json
{
  "name": "mcp-code-execution",
  "version": "1.0.0",
  "description": "Code execution with MCP - 99.6% token efficiency via CLI scripts",
  "commands": ["commands/"],
  "skills": ["skills/"],
  "hooks": ["hooks/"],
  "agents": []
}
```

### 2.2 Migrate Skills
- Move `.claude/skills/*` ’ `.claude-plugin/skills/`
- Update any symlinks to use `${CLAUDE_PLUGIN_ROOT}` variable
- Update SKILL.md frontmatter for auto-activation:
```yaml
---
name: code-execution
description: Execute Python/CLI scripts with MCP tool access
auto_activate:
  triggers:
    - "execute code"
    - "run script"
    - "python"
    - "data processing"
---
```

### 2.3 Create Commands Directory
Create `.claude-plugin/commands/init-code-execution.md`:
- Scaffolds local scripts directory
- Copies mcp_config.example.json
- Runs `uv sync` for dependencies

---

## Phase 3: Implement Safety Hooks (R3)

### 3.1 PreToolUse Audit Hook
Create `.claude-plugin/hooks/code-execution-audit.py`:
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PreToolUse hook: logs code before execution for audit trail."""
import sys
import json
import os
from datetime import datetime
from pathlib import Path

def main():
    # Parse hook input
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only audit code execution tools
    if "execute" not in tool_name.lower() and "run" not in tool_name.lower():
        return

    # Create audit log
    log_dir = Path(".claude/logs/code-execution")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool": tool_name,
        "input": tool_input,
        "status": "pre-execution"
    }

    log_file = log_dir / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    main()
```

### 3.2 PostToolUse Result Hook
Create `.claude-plugin/hooks/code-execution-result.py`:
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""PostToolUse hook: logs execution results and errors."""
import sys
import json
from datetime import datetime
from pathlib import Path

def main():
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool_name", "")
    tool_result = input_data.get("tool_result", {})

    if "execute" not in tool_name.lower() and "run" not in tool_name.lower():
        return

    log_dir = Path(".claude/logs/code-execution")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool": tool_name,
        "result_summary": str(tool_result)[:500],  # Truncate large results
        "status": "post-execution"
    }

    log_file = log_dir / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    main()
```

### 3.3 Register Hooks in hooks.json
Create `.claude-plugin/hooks.json`:
```json
{
  "hooks": [
    {
      "matcher": {
        "tool_name": ".*execute.*|.*run.*"
      },
      "hooks": [
        {
          "type": "PreToolUse",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/code-execution-audit.py"
        }
      ]
    },
    {
      "matcher": {
        "tool_name": ".*execute.*|.*run.*"
      },
      "hooks": [
        {
          "type": "PostToolUse",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/code-execution-result.py"
        }
      ]
    }
  ]
}
```

---

## Phase 4: Meridian Integration (R4)

### 4.1 Update skill-rules.json
Add to existing `.claude/skills/skill-rules.json` (or create plugin-local version):
```json
{
  "code-execution": {
    "triggers": [
      "execute code",
      "run script",
      "python script",
      "data processing",
      "mcp tool",
      "workflow automation"
    ],
    "skill_path": "${CLAUDE_PLUGIN_ROOT}/skills/code-execution/"
  }
}
```

### 4.2 Memory Integration
Add optional memory logging in result hook:
```python
# In code-execution-result.py, after successful execution:
# Flag for memory-curator if pattern is reusable
if is_reusable_pattern(tool_result):
    print("MEMORY: Successful workflow pattern - consider saving via memory-curator",
          file=sys.stderr)
```

### 4.3 Task Context Integration
Modify hooks to include active task:
```python
# Check for active task
task_file = Path(".meridian/.active-task")
if task_file.exists():
    active_task = task_file.read_text().strip()
    log_entry["task"] = active_task
```

---

## Phase 5: Marketplace Registration (R5)

### 5.1 Update Plugin for Marketplace
Ensure `.claude-plugin/plugin.json` includes:
```json
{
  "marketplace": {
    "category": "code-execution",
    "tags": ["mcp", "automation", "scripts"],
    "repository": "https://github.com/austinmao/mcp-code-execution-meridian"
  }
}
```

### 5.2 Register in Basecamp
Add entry to austinmao/basecamp `marketplace.json`:
```json
{
  "plugins": [
    {
      "name": "mcp-code-execution",
      "description": "Code execution with MCP - 99.6% token efficiency",
      "source": "github:austinmao/mcp-code-execution-meridian",
      "version": "1.0.0"
    }
  ]
}
```

---

## Phase 6: Documentation (R6)

### 6.1 Update README
- Plugin installation section
- MCP server configuration
- Usage examples with CLI scripts
- Safety/audit logging documentation

### 6.2 Create SKILL.md Files
For each skill in `.claude-plugin/skills/`:
```markdown
---
name: simple-fetch
description: Single-tool MCP execution pattern
auto_activate:
  triggers:
    - fetch data
    - api call
---

# Simple Fetch Skill

Execute single MCP tool calls with CLI arguments.

## Usage
\`\`\`bash
uv run python -m runtime.harness scripts/simple_fetch.py --url "https://..."
\`\`\`

## Arguments
- `--url`: Target URL to fetch
- `--output`: Output format (json|text)
```

---

## Validation Checklist

- [ ] Fork created and sandbox removed
- [ ] Plugin manifest at `.claude-plugin/plugin.json`
- [ ] Skills migrated to `.claude-plugin/skills/`
- [ ] Audit hooks created and registered
- [ ] skill-rules.json includes code-execution triggers
- [ ] Tests pass (sandbox tests removed)
- [ ] Plugin installs via `/plugin install mcp-code-execution@basecamp`
- [ ] CLI scripts execute with logging
- [ ] README documents installation and usage
