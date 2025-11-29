# Debugging Pre-Commit Hook Problems

## Diagnosing Hook Issues

### Check If Hooks Are Installed

```bash
# List git hooks
ls -la .git/hooks/

# Check if husky is configured (Node projects)
cat .husky/_/pre-commit 2>/dev/null || echo "No husky config"

# Check if pre-commit is installed (Python projects)
cat .pre-commit-config.yaml 2>/dev/null || echo "No pre-commit config"
```

### Run Hooks Manually

```bash
# Run pre-commit hooks directly (if using pre-commit framework)
pre-commit run --all-files

# Run specific hook
pre-commit run eslint --all-files

# Run husky hooks manually
.husky/pre-commit
```

### Check Hook Configuration

**For Husky (Node.js):**
```bash
# Check package.json scripts
cat package.json | grep -A5 '"lint"'
cat package.json | grep -A5 '"prepare"'

# Check husky configuration
cat .husky/pre-commit
```

**For pre-commit (Python):**
```bash
# Check pre-commit configuration
cat .pre-commit-config.yaml

# Validate config
pre-commit validate-config
```

## Common Problems and Solutions

### Hook Not Running

**Symptoms:** Commits succeed without any checks running

**Diagnosis:**
```bash
# Check if hooks directory exists
ls .git/hooks/pre-commit

# Check if hooks are executable
file .git/hooks/pre-commit
```

**Solutions:**
```bash
# Reinstall hooks (Husky)
npm run prepare
# or
npx husky install

# Reinstall hooks (pre-commit)
pre-commit install
```

### Hook Fails With "Command Not Found"

**Symptoms:**
```
.husky/pre-commit: line 4: npx: command not found
```

**Solutions:**
```bash
# Ensure npm/node are in PATH for git hooks
# Add to .husky/pre-commit at the top:
export PATH="/usr/local/bin:$PATH"

# Or for nvm users:
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### Hook Runs But Checks Wrong Files

**Symptoms:** Linting old files, not staged files

**Diagnosis:**
```bash
# Check lint-staged configuration (if used)
cat package.json | grep -A10 '"lint-staged"'
```

**Solutions:**
- Ensure lint-staged is configured correctly
- Check file patterns in lint-staged config
- Run `git diff --cached --name-only` to see staged files

### Hook Times Out

**Symptoms:** Hook takes forever, or times out

**Solutions:**
1. Check for slow tests being run in hook
2. Limit hook to staged files only (use lint-staged)
3. Skip slow integration tests in pre-commit (run in CI instead)

### Hook Works Locally But Fails in CI

**Symptoms:** Pre-commit passes locally but CI complains

**Diagnosis:**
- Different Node/Python versions
- Missing system dependencies
- Different OS behaviors

**Solutions:**
```bash
# Pin versions in CI to match local
# Use .nvmrc or .python-version files
# Ensure CI installs same dependencies
```

## Emergency Procedures

### If Legitimately Need to Commit Without Hooks

**STOP:** This should be extremely rare. Ask yourself:
1. Is this a genuine emergency?
2. Have I tried fixing the hook issue?
3. Am I just being lazy?

If genuinely blocked (hook is broken, not your code):

```bash
# Document why in commit message
git commit -m "Emergency: [reason] - hook fix in next commit

Note: Bypassing broken hook, will fix immediately after.
Issue: [description of hook problem]"

# IMMEDIATELY create follow-up to fix hook
# Don't leave codebase in this state
```

### If Hook Is Genuinely Broken

1. **Don't bypass** - fix the hook
2. Check recent changes to hook configs
3. Reinstall hook framework:
   ```bash
   # Node
   rm -rf node_modules && npm install

   # Python
   pre-commit clean && pre-commit install
   ```
4. If hook config is broken, fix the config file
5. Then commit normally
