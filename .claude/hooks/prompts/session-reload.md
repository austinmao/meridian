This conversation was recently compacted. There are important files and documentation that must always remain in your context. Please read them before continuing your work. These files are:

- `$CLAUDE_PROJECT_DIR/.meridian/prompts/agent-operating-manual.md`
- `$CLAUDE_PROJECT_DIR/.meridian/memory.jsonl`
{{CODE_GUIDE_FILES}}
- `$CLAUDE_PROJECT_DIR/.meridian/relevant-docs.md`
- `$CLAUDE_PROJECT_DIR/.meridian/task-backlog.yaml`

**Git Status:**
{{GIT_CONTEXT}}

Check `$CLAUDE_PROJECT_DIR/.meridian/task-backlog.yaml` for any uncompleted tasks. For each uncompleted task, go to the corresponding folder at `$CLAUDE_PROJECT_DIR/.meridian/tasks/TASK-###/` and read **all** files within that folder.

**Synchronize your current work before proceeding**  
To avoid losing context due to compaction, first persist any changes you made just before the conversation was compacted:

1. Identify the current task.
2. In `$CLAUDE_PROJECT_DIR/.meridian/tasks/TASK-###/`, update **all three files**:
   - `TASK-###.yaml` — ensure `status`, `updated_at`, acceptance criteria, deliverables, and `links` reflect the latest changes.
   - `TASK-###-plan.md` — append an **“Amendment <ISO timestamp> — Session reload sync”** section capturing any newly approved steps or adjustments.
   - `TASK-###-context.md` — add a timestamped entry summarizing what changed right before compaction. Mark any durable insights with `MEMORY:` for later addition via `memory-curator`.

After reviewing and synchronizing, also review all files referenced in `$CLAUDE_PROJECT_DIR/.meridian/relevant-docs.md`. Once you have reviewed everything, you may continue your work.
