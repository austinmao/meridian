---
name: init-meridian
description: Initialize Meridian task management framework in the current project
---

# Initialize Meridian Framework

You are initializing the Meridian task management framework in the user's current project.

## Pre-flight Checks

Before proceeding, check if `.meridian/` already exists in the current project:
- If it exists, ask the user if they want to:
  - Skip initialization (keep existing)
  - Merge (only add missing files)
  - Overwrite (replace all files)

## Scaffolding Steps

Create the following structure in the user's project:

### 1. Create Directory Structure

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
├── CODE_GUIDE.md
├── CODE_GUIDE_ADDON_TDD.md
├── CODE_GUIDE_ADDON_PRODUCTION.md
├── CODE_GUIDE_ADDON_HACKATHON.md
├── config.yaml
├── memory.jsonl
├── relevant-docs.md
└── task-backlog.yaml
```

### 2. File Contents

Use the following templates for each file:

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

### 3. Post-Initialization

After creating the files:
1. Confirm what was created
2. Explain the purpose of each key file:
   - `task-backlog.yaml`: Index of all tasks
   - `memory.jsonl`: Append-only log of architectural decisions
   - `config.yaml`: Project configuration
   - `tasks/`: Individual task briefs with plans and context
3. Suggest next steps:
   - Review and customize CODE_GUIDE.md for the project
   - Create first task using the task-manager skill
   - Add project-specific entries to relevant-docs.md

## Important Notes

- DO NOT overwrite existing files without user confirmation
- Create directories with proper permissions
- Use Write tool for file creation
- Report any errors clearly

## Completion Message

After successful initialization, display:

```
Meridian initialized successfully!

Created structure:
  .meridian/
  ├── config.yaml          # Project configuration
  ├── task-backlog.yaml    # Task index
  ├── memory.jsonl         # Architectural decisions log
  ├── CODE_GUIDE.md        # Coding standards
  └── tasks/               # Task briefs folder

Next steps:
1. Review .meridian/config.yaml and set project_type
2. Customize .meridian/CODE_GUIDE.md for your project
3. Use the 'task-manager' skill to create your first task
```
