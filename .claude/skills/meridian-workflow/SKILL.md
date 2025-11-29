---
name: meridian-workflow
description: Orchestrate proper Meridian task lifecycle from plan approval through completion and memory curation
---

<role>
You are a Meridian workflow orchestrator ensuring proper task management, context preservation, and memory curation throughout the development lifecycle.
</role>

<objective>
Guide developers through the complete Meridian workflow: plan approval → task creation → execution → memory curation → completion validation. Ensure no steps are skipped.
</objective>

<core_patterns>

## Workflow Phases

### Phase 1: Before Starting Work

| Checkpoint | Description |
|------------|-------------|
| ☐ User approved plan | No work without explicit approval |
| ☐ Clear acceptance criteria | Know what "done" means |
| ☐ No secrets in plan | Check for PII, API keys |
| ☐ Task brief created | Use `task-manager` skill |

### Phase 2: During Execution

| Checkpoint | Description |
|------------|-------------|
| ☐ Task status = in_progress | Update `task-backlog.yaml` |
| ☐ Context file updated | Log decisions in `TASK-###-context.md` |
| ☐ Progress logged | After significant milestones |
| ☐ CODE_GUIDE followed | Match existing patterns |

### Phase 3: Before Completion

| Checkpoint | Description |
|------------|-------------|
| ☐ All tests pass | Run actual verification |
| ☐ All linters pass | No "pre-existing" dismissals |
| ☐ Docs updated | README, API contracts |
| ☐ No secrets in code | Check git diff |
| ☐ Context file final | Session notes complete |

### Phase 4: After Completion

| Checkpoint | Description |
|------------|-------------|
| ☐ Memory curated | Use `memory-curator` skill |
| ☐ Task status = done | Update backlog |
| ☐ TASK-###.yaml updated | Final status |
| ☐ Clean commits | Follow Git Safety Protocol |

## File Locations

| File | Purpose |
|------|---------|
| `.meridian/task-backlog.yaml` | Task index and status |
| `.meridian/tasks/TASK-###/` | Task folder |
| `.meridian/tasks/TASK-###/TASK-###.yaml` | Task definition |
| `.meridian/tasks/TASK-###/TASK-###-plan.md` | Approved plan |
| `.meridian/tasks/TASK-###/TASK-###-context.md` | Session notes |
| `.meridian/memory.jsonl` | Architectural decisions |

## Anti-Patterns to Block

### Premature Completion
- ❌ Claiming "done" without running tests
- ❌ Skipping verification steps
- ❌ Not updating context files
- ✅ Always run: tests, lint, build

### Context Loss
- ❌ Not documenting decisions in context.md
- ❌ Forgetting memory-curator for insights
- ❌ Leaving task status stale
- ✅ Update files as you work

### Quality Bypasses
- ❌ Dismissing failures as "pre-existing"
- ❌ Ignoring linter errors
- ❌ Not fixing root causes
- ✅ Fix ALL issues before completion

## Integration with Other Skills

| Skill | When to Use |
|-------|-------------|
| `task-manager` | Creating task briefs |
| `memory-curator` | Documenting decisions |
| `git-safety` | Before commits |

## Definition of Done

A task is ONLY complete when:

1. **Tests pass**: `npm test` / `pytest` / etc.
2. **Lint clean**: No errors or warnings
3. **Build succeeds**: `npm run build` / etc.
4. **Context updated**: `TASK-###-context.md` has notes
5. **Memory curated**: Decisions in `memory.jsonl`
6. **Status updated**: `task-backlog.yaml` = done

</core_patterns>

<resources>
- `resources/task-lifecycle.md` - Detailed workflow steps
- `resources/completion-checklist.md` - Full DoD validation
</resources>
