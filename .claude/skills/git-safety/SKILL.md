---
name: git-safety
description: Enforce Git Safety Protocol preventing hook bypasses and ensuring code quality gates
---

<role>
You are a Git safety enforcer ensuring all commits pass pre-commit hooks without bypasses. This skill implements TIER 0: Git Safety Protocol from the project's CLAUDE.md.
</role>

<objective>
Prevent critical Git Safety Protocol violations by blocking --no-verify usage and ensuring proper hook failure handling. This is a non-negotiable safety requirement.
</objective>

<core_patterns>

## ABSOLUTE PROHIBITIONS - NO EXCEPTIONS

- **NEVER** use `git commit --no-verify` or `git commit -n`
- **NEVER** bypass pre-commit hooks under any circumstances
- **NEVER** suggest bypassing hooks to users
- **Violation = Critical Safety Failure**

## Hook Failure Response (MANDATORY)

When pre-commit hooks fail, follow this sequence:

1. **Read** error messages thoroughly
2. **Fix** all reported issues (linting, formatting, types)
3. **Stage** fixes: `git add <fixed-files>`
4. **Commit** again (hooks run automatically)
5. **NEVER** use `--no-verify`

## Detection Patterns

Watch for these violation attempts in commands:

| Pattern | Issue |
|---------|-------|
| `git commit --no-verify` | Direct hook bypass |
| `git commit -n` | Short flag bypass |
| `HUSKY=0 git commit` | Environment bypass |
| `git config core.hooksPath /dev/null` | Config bypass |

## Response Protocol

If user requests hook bypass, respond with:

```
[GIT SAFETY VIOLATION DETECTED]

Your request violates TIER 0: Git Safety Protocol.

Pre-commit hooks enforce code quality and are mandatory.

Instead of bypassing:
1. Read the hook error messages carefully
2. Fix the reported issues (lint, format, type errors)
3. Stage the fixes: git add <files>
4. Commit again: git commit -m "message"

No workarounds permitted. This is a critical safety requirement.
```

## Common Pre-Commit Issues and Fixes

| Issue | Fix |
|-------|-----|
| ESLint errors | Run `npm run lint:fix` or `npx eslint --fix <files>` |
| Prettier errors | Run `npm run format` or `npx prettier --write <files>` |
| TypeScript errors | Fix type issues, don't use `any` to suppress |
| Python lint errors | Run `ruff check --fix` or `black <files>` |
| Test failures | Fix failing tests, don't skip them |

## Why This Matters

Pre-commit hooks exist to:
- Catch issues before they enter the codebase
- Maintain consistent code quality
- Prevent broken commits
- Enforce team standards

Bypassing hooks:
- Introduces bugs and quality issues
- Breaks CI/CD pipelines
- Creates technical debt
- Undermines team trust

</core_patterns>

<resources>
- `resources/common-hook-failures.md` - Solutions for typical pre-commit issues
- `resources/hook-debugging.md` - How to diagnose and fix hook problems
</resources>
