# Task Completion Checklist

Use this checklist before marking any task as complete.

## Code Quality

```
☐ Code compiles without errors
☐ No TypeScript/type errors
☐ Linting passes (no warnings)
☐ Formatting applied (Prettier/Black)
☐ No debug code (console.log, print, debugger)
☐ No commented-out code (delete it)
☐ No TODO comments left unaddressed
```

## Testing

```
☐ All existing tests pass
☐ New tests added for new functionality
☐ Edge cases covered
☐ Error cases handled and tested
☐ Integration tests pass (if applicable)
☐ Manual testing completed
```

## Security

```
☐ No secrets in code (API keys, passwords)
☐ No secrets in git diff
☐ No .env files committed (only .env.example)
☐ Input validation in place
☐ No SQL injection risks
☐ No XSS vulnerabilities
☐ Proper authentication/authorization
```

## Documentation

```
☐ README updated (if applicable)
☐ API docs updated (if applicable)
☐ Code comments for complex logic
☐ Type definitions complete
☐ CHANGELOG entry added
```

## Meridian Files

```
☐ TASK-###.yaml status = done
☐ TASK-###-context.md has final notes
☐ task-backlog.yaml status = done
☐ memory.jsonl updated (if decisions made)
```

## Git

```
☐ Changes committed
☐ Pre-commit hooks pass
☐ NO --no-verify used
☐ Commit message is descriptive
☐ Branch up to date with main (if applicable)
```

## Final Verification Commands

Run these before declaring complete:

```bash
# JavaScript/TypeScript
npm test
npm run lint
npm run build
npm run type-check  # if separate from build

# Python
pytest
ruff check .
mypy .

# General
git diff  # Check for secrets
git status  # Check for uncommitted files
```

## Red Flags - DO NOT Complete If:

- ❌ Tests are failing
- ❌ Linter has errors
- ❌ Build is broken
- ❌ Type errors exist
- ❌ Secrets detected in code
- ❌ Context file not updated
- ❌ Acceptance criteria not met

## Completion Statement

Only after all checkboxes are verified, update:

1. `TASK-###.yaml`:
   ```yaml
   status: done
   completed_at: YYYY-MM-DD
   notes: |
     - Summary of what was done
     - Key decisions made
     - Any follow-up needed
   ```

2. `task-backlog.yaml`:
   ```yaml
   - id: TASK-###
     status: done
   ```

3. `TASK-###-context.md`:
   ```markdown
   ## Session: YYYY-MM-DD
   - Completed implementation
   - All tests passing
   - Merged to main
   ```
