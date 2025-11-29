---
name: init-meridian
description: Initialize Meridian task management framework in the current project
---

# Initialize Meridian Framework

You are initializing the Meridian task management framework in the user's current project.

## Pre-flight Checks

**ALWAYS check each file individually before creating.** Default behavior is **merge mode** - only create what's missing.

### Step 1: Detect existing installation

Run these checks silently (no user prompts needed):

```bash
# Check what exists
ls -la .meridian/ 2>/dev/null || echo "No .meridian folder"
```

### Step 2: Categorize files

For each file in the target structure, categorize as:
- **Missing**: File doesn't exist → CREATE IT
- **Exists**: File exists → SKIP IT (preserve user data)
- **Empty placeholder**: File exists but is empty/default → SKIP IT (user may have intentionally cleared)

### Step 3: Report plan before executing

Before creating any files, report:
```
Meridian Status:
  ✓ Exists (will skip): [list files]
  + Missing (will create): [list files]
```

Only ask for confirmation if `.meridian/` exists AND has significant content. Otherwise, proceed automatically.

## Required Files Checklist

Check each file and create ONLY if missing:

| Path | Check | Action if Missing |
|------|-------|-------------------|
| `.meridian/` | `test -d .meridian` | Create directory |
| `.meridian/tasks/` | `test -d .meridian/tasks` | Create directory |
| `.meridian/tasks/TASK-000-template/` | `test -d .meridian/tasks/TASK-000-template` | Create directory |
| `.meridian/backups/` | `test -d .meridian/backups` | Create directory |
| `.meridian/docs/` | `test -d .meridian/docs` | Create directory |
| `.meridian/prompts/` | `test -d .meridian/prompts` | Create directory |
| `.meridian/config.yaml` | `test -f .meridian/config.yaml` | Create from template |
| `.meridian/task-backlog.yaml` | `test -f .meridian/task-backlog.yaml` | Create from template |
| `.meridian/memory.jsonl` | `test -f .meridian/memory.jsonl` | Create empty file |
| `.meridian/relevant-docs.md` | `test -f .meridian/relevant-docs.md` | Create from template |
| `.meridian/CODE_GUIDE.md` | `test -f .meridian/CODE_GUIDE.md` | Create from template |
| `.meridian/CODE_GUIDE_ADDON_*.md` | Check each addon | Create from template |
| `.meridian/prompts/agent-operating-manual.md` | `test -f` | Create from template |
| `.meridian/tasks/TASK-000-template/*` | Check each file | Create from template |

### Target Structure (for reference)

```
.meridian/
├── tasks/
│   └── TASK-000-template/
│       ├── TASK-000.yaml
│       ├── TASK-000-plan.md
│       └── TASK-000-context.md
├── backups/
├── docs/
├── prompts/
│   └── agent-operating-manual.md
├── CODE_GUIDE.md
├── CODE_GUIDE_ADDON_TDD.md
├── CODE_GUIDE_ADDON_PRODUCTION.md
├── CODE_GUIDE_ADDON_HACKATHON.md
├── config.yaml
├── memory.jsonl
├── relevant-docs.md
└── task-backlog.yaml
```

## File Templates

Use the following templates for each file (create ONLY if file doesn't exist):

#### .meridian/config.yaml
```yaml
# Project-level configuration for the Claude workflow

# Project type affects which code guide add-on is loaded:
# - hackathon   → use CODE_GUIDE_ADDON_HACKATHON.md
# - standard    → baseline only
# - production  → use CODE_GUIDE_ADDON_PRODUCTION.md
project_type: standard

# Optional: Test-Driven Development mode.
# When true, inject CODE_GUIDE_ADDON_TDD.md and follow its rules.
tdd_mode: false
```

#### .meridian/task-backlog.yaml
```yaml
# Task Backlog
# Simple index of tasks - detailed definitions live in .meridian/tasks/TASK-###/

tasks: []
```

#### .meridian/memory.jsonl
Create an empty file (will be populated as architectural decisions are made).

#### .meridian/relevant-docs.md
```markdown
Always read these files before continuing your work:
```

#### .meridian/tasks/TASK-000-template/TASK-000.yaml
Copy the task template structure with fields for:
- id, title, status, priority
- objective, constraints, requirements
- deliverables, implementation_notes, risks
- validation, links, notes, resources

#### .meridian/CODE_GUIDE.md
Copy the comprehensive code guide with frontend and backend sections covering TypeScript, React, Next.js, and Node.js best practices.

## Post-Initialization

After processing all files:

1. **Report what happened** (be specific):
   ```
   Meridian initialization complete!

   ✓ Skipped (already existed): [list files]
   + Created: [list files]
   ```

2. **If nothing was created** (full installation exists):
   ```
   Meridian already fully installed - no changes needed.

   Existing structure verified:
     .meridian/config.yaml ✓
     .meridian/task-backlog.yaml ✓
     .meridian/memory.jsonl ✓
     ...
   ```

3. **Explain key files** (only for newly created ones):
   - `task-backlog.yaml`: Index of all tasks
   - `memory.jsonl`: Append-only log of architectural decisions
   - `config.yaml`: Project configuration (set project_type here)
   - `tasks/`: Individual task briefs with plans and context
   - `CODE_GUIDE.md`: Coding standards (customize for your project)

4. **Suggest next steps** (only if files were created):
   - Review and customize CODE_GUIDE.md for the project
   - Create first task using the task-manager skill
   - Add project-specific entries to relevant-docs.md

## Important Rules

- **NEVER overwrite existing files** - always skip if file exists
- **NEVER prompt user for merge/overwrite** - default is always merge (add missing only)
- **Preserve user data** - existing memory.jsonl, task-backlog.yaml, etc. contain valuable data
- Create directories with proper permissions
- Use Write tool for file creation
- Report any errors clearly

## Completion Messages

### Fresh install (no .meridian/ existed):
```
Meridian initialized successfully!

Created:
  .meridian/
  ├── config.yaml          # Project configuration
  ├── task-backlog.yaml    # Task index
  ├── memory.jsonl         # Architectural decisions log
  ├── CODE_GUIDE.md        # Coding standards
  ├── prompts/             # Agent prompts
  └── tasks/               # Task briefs folder

Next steps:
1. Review .meridian/config.yaml and set project_type
2. Customize .meridian/CODE_GUIDE.md for your project
3. Use the 'task-manager' skill to create your first task
```

### Partial install (some files existed):
```
Meridian updated!

Skipped (preserved existing):
  ✓ .meridian/memory.jsonl (12 entries)
  ✓ .meridian/task-backlog.yaml (3 tasks)
  ✓ .meridian/config.yaml

Created (was missing):
  + .meridian/CODE_GUIDE_ADDON_TDD.md
  + .meridian/prompts/agent-operating-manual.md
```

### Full install (everything existed):
```
Meridian already installed - nothing to update.

All required files present:
  ✓ .meridian/config.yaml
  ✓ .meridian/task-backlog.yaml
  ✓ .meridian/memory.jsonl
  ✓ .meridian/CODE_GUIDE.md
  ✓ .meridian/prompts/agent-operating-manual.md
  ✓ .meridian/tasks/
```
