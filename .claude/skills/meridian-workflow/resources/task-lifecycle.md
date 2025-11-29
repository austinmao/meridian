# Meridian Task Lifecycle

## Overview

Every task in Meridian follows a structured lifecycle that ensures quality, traceability, and knowledge preservation.

```
Idea → Plan → Approval → Task Brief → Execution → Verification → Completion → Memory
```

## Stage 1: Planning

### Trigger
- User requests a feature/fix/improvement
- Bug discovered during development
- Technical debt identified

### Actions
1. Analyze requirements
2. Research existing patterns in codebase
3. Draft implementation plan
4. Identify risks and constraints

### Output
- Clear plan document
- Acceptance criteria
- Estimated scope

### Checkpoint
```
☐ Is the plan detailed enough?
☐ Are acceptance criteria measurable?
☐ Are risks identified?
☐ Does it match CODE_GUIDE.md patterns?
```

## Stage 2: Approval

### Trigger
- Plan ready for review

### Actions
1. Present plan to user
2. Discuss alternatives
3. Address concerns
4. Get explicit approval

### Output
- Approved plan
- Any modifications from discussion

### Checkpoint
```
☐ User explicitly approved? (not assumed)
☐ Any changes incorporated?
☐ Scope is clear?
```

## Stage 3: Task Brief Creation

### Trigger
- Plan approved

### Actions
1. Use `task-manager` skill
2. Create task folder: `.meridian/tasks/TASK-###/`
3. Create files:
   - `TASK-###.yaml` (definition)
   - `TASK-###-plan.md` (approved plan)
   - `TASK-###-context.md` (empty, for notes)
4. Update `task-backlog.yaml`

### Output
- Complete task folder
- Task in backlog with status: `todo`

### Checkpoint
```
☐ Task ID assigned?
☐ All files created?
☐ Backlog updated?
```

## Stage 4: Execution

### Trigger
- Ready to start work

### Actions
1. Update status to `in_progress` in backlog
2. Follow the approved plan
3. Write code following CODE_GUIDE.md
4. Update context.md with:
   - Decisions made
   - Issues encountered
   - Solutions found
   - Key learnings

### Output
- Code changes
- Updated context.md

### Checkpoint (ongoing)
```
☐ Following the plan?
☐ Documenting decisions?
☐ Matching existing patterns?
☐ No security issues?
```

## Stage 5: Verification

### Trigger
- Implementation complete

### Actions
1. Run all tests
2. Run all linters
3. Run build
4. Review changes manually
5. Check for secrets in diff

### Output
- All checks passing
- No issues remaining

### Checkpoint
```
☐ npm test / pytest passes?
☐ npm run lint passes?
☐ npm run build passes?
☐ git diff shows no secrets?
☐ Changes match acceptance criteria?
```

## Stage 6: Completion

### Trigger
- All verification passes

### Actions
1. Update `TASK-###.yaml`:
   - status: done
   - completion notes
2. Update `task-backlog.yaml`:
   - status: done
3. Finalize `TASK-###-context.md`
4. Commit changes (follow Git Safety Protocol)

### Output
- Task marked complete
- Clean commit(s)

### Checkpoint
```
☐ Task YAML updated?
☐ Backlog updated?
☐ Context finalized?
☐ Commit created (no --no-verify)?
```

## Stage 7: Memory Curation

### Trigger
- Task complete
- Significant decision made
- Lesson learned

### Actions
1. Use `memory-curator` skill
2. Document in `memory.jsonl`:
   - Architectural decisions
   - Trade-offs made
   - Lessons learned
   - Patterns established

### Output
- Memory entry added

### Checkpoint
```
☐ Decision worth preserving?
☐ Memory entry complete?
☐ Links to related memories?
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping approval | Always get explicit user approval |
| No task brief | Create brief even for small tasks |
| Context not updated | Update as you work, not at end |
| Verification skipped | Run all checks before claiming done |
| Memory forgotten | Curate after significant decisions |
| Status stale | Update immediately when status changes |
