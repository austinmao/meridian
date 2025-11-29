# Common Pre-Commit Hook Failures

## JavaScript/TypeScript Projects

### ESLint Failures

**Symptoms:**
```
✖ eslint found some errors. Please fix them and try again.
error: 'foo' is defined but never used
error: Missing return type on function
```

**Fixes:**
```bash
# Auto-fix what's possible
npm run lint:fix
# or
npx eslint --fix src/

# Then manually fix remaining issues
# Commit again - hooks will re-run
```

### Prettier Failures

**Symptoms:**
```
[warn] src/file.ts: Check failed.
Code style issues found. Run Prettier to fix them.
```

**Fixes:**
```bash
# Format all files
npm run format
# or
npx prettier --write .

# Commit again
```

### TypeScript Type Errors

**Symptoms:**
```
error TS2322: Type 'string' is not assignable to type 'number'
error TS7006: Parameter 'x' implicitly has an 'any' type
```

**Fixes:**
1. Read the error message carefully
2. Fix the actual type issue (don't use `any` to suppress)
3. If a library lacks types, add `@types/library-name`
4. Stage and commit again

## Python Projects

### Ruff/Flake8 Failures

**Symptoms:**
```
error: F401 'os' imported but unused
error: E501 line too long (120 > 88)
```

**Fixes:**
```bash
# Auto-fix with Ruff
ruff check --fix .

# Format with Black
black .

# Commit again
```

### MyPy Type Errors

**Symptoms:**
```
error: Incompatible return value type
error: "None" has no attribute "foo"
```

**Fixes:**
1. Add proper type hints
2. Handle None cases explicitly
3. Don't use `# type: ignore` without understanding the issue
4. Stage and commit again

## General Strategies

### When Auto-Fix Doesn't Work

1. Read the specific error message
2. Look up the rule (e.g., "ESLint rule no-unused-vars")
3. Fix the code to comply with the rule
4. Don't disable the rule project-wide without team discussion

### When Tests Fail

1. Run tests locally: `npm test` or `pytest`
2. Fix failing tests (don't delete or skip them)
3. If test is genuinely obsolete, discuss with team first
4. Stage fixes and commit again

### When Multiple Hooks Fail

1. Fix one category at a time
2. Start with linting (easiest to auto-fix)
3. Then formatting
4. Then types
5. Then tests (may depend on above)
6. Commit after each successful fix

## What NOT to Do

| Bad Practice | Why It's Bad |
|--------------|--------------|
| `git commit --no-verify` | Bypasses all safety checks |
| `// eslint-disable-next-line` everywhere | Hides real issues |
| `any` type in TypeScript | Defeats type safety |
| `# type: ignore` in Python | Hides real issues |
| Deleting failing tests | Removes safety net |
| `HUSKY=0` environment variable | Disables hooks entirely |
