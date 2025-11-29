# Spec-Kit + Meridian Integration Documentation
**Date**: 2025-11-29
**Status**: Production Ready
**Version**: 1.0

## Executive Summary

GitHub's spec-kit is now integrated with Meridian's task management system, providing a structured spec-driven development workflow while maintaining Meridian's rigor for approval, tracking, and architectural memory.

**Key Principle**: Spec-kit generates specifications → Humans approve → Meridian tracks execution

## What Was Implemented

### 1. Automatic Capture Hook (`speckit-capture.py`)

**Location**: `.claude/hooks/speckit-capture.py`
**Type**: PostToolUse hook (runs after SlashCommand tool)
**Purpose**: Automatically captures spec-kit command outputs and bridges them to Meridian

**Features**:
- Detects `/speckit.*` commands automatically
- Captures `/speckit.specify` requirements (extracts structured data)
- Saves `/speckit.plan` outputs to `docs/artifacts/speckit-plan-TIMESTAMP.md`
- Captures `/speckit.tasks` breakdowns for Beads/Meridian integration
- Provides next-step guidance after each command
- Suggests memory.jsonl entries (doesn't write automatically per CLAUDE.md protocol)
- Non-blocking (exit code 0) - never interrupts workflow

**Testing**: ✅ Passed manual tests with simulated spec-kit outputs

### 2. Spec-Kit Skill (`spec-kit/SKILL.md`)

**Location**: `.claude/skills/spec-kit/`
**Auto-Activation Triggers**:
- File patterns: `docs/artifacts/speckit-*.md`
- Keywords: `spec-kit`, `speckit`, `specification`, `spec-driven`, `constitution`, `specify`, `plan feature`, `requirements`

**Structure**:
```
.claude/skills/spec-kit/
├── SKILL.md                              # <500 lines - main overview
└── resources/
    ├── speckit-meridian-patterns.md      # Integration workflows
    └── speckit-validation.md             # Output validation checklists
```

**Content**:
- Spec-kit overview and philosophy
- Integration decision tree (when to use what)
- Meridian-Spec-kit workflow (5 phases)
- Workflow mapping (spec-kit commands → Meridian artifacts)
- Best practices and anti-patterns
- Common troubleshooting

### 3. Configuration Updates

**`.claude/settings.json`**:
- Added PostToolUse hook for SlashCommand matcher
- Runs `speckit-capture.py` after every slash command
- Positioned before tool-logger for proper execution order

**`.claude/skills/skill-rules.json`**:
- Added spec-kit skill entry
- Auto-activation on spec-kit keywords and artifact files
- Triggers when users mention specification-related work

## Architecture Overview

### Integration Flow

```
User runs /speckit.* command
    ↓
Claude executes SlashCommand tool
    ↓
speckit-capture.py hook fires (PostToolUse)
    ↓
Hook analyzes output, saves artifacts, provides guidance
    ↓
User reviews spec-kit output
    ↓
User approves (explicit "yes")
    ↓
Use task-manager skill to create Meridian TASK-###
    ↓
Populate TASK-###.yaml with spec-kit requirements
    ↓
Copy approved plan to TASK-###-plan.md
    ↓
Execute using Meridian workflow + Beads for subtasks
```

### Workflow Mapping

| Spec-Kit Command | Output | Meridian Artifact | Purpose |
|------------------|--------|-------------------|---------|
| `/speckit.constitution` | Project principles | `.meridian/config.yaml` or `docs/` | Establish standards (optional) |
| `/speckit.specify` | Requirements list | `TASK-###.yaml` requirements section | What to build |
| `/speckit.plan` | Technical approach | `TASK-###-plan.md` | How to build (approved) |
| `/speckit.tasks` | Task breakdown | Beads issues OR `TASK-###-context.md` checklist | Execution steps |
| `/speckit.implement` | Code execution | Code + `TASK-###-context.md` updates | Implementation |

### Decision Tree: When to Use What

```
Is this a complex feature needing stakeholder approval?
├─ YES → Use spec-kit for planning, create Meridian TASK-###
│          └─ /speckit.specify → /speckit.plan → Approval → Meridian task
│
└─ NO → Is it an architectural decision?
    ├─ YES → Document in memory.jsonl (use memory-curator skill)
    │
    └─ NO → Is it a simple bug/refactor?
        └─ YES → Optional spec-kit + Beads only (no TASK-###)
```

## Usage Examples

### Example 1: Feature Development (Full Workflow)

```bash
# Step 1: Generate requirements
/speckit.specify OAuth2 authentication with Google and GitHub

# Hook output: "Captured 8 requirements from /speckit.specify"
# Review requirements in context

# Step 2: Create technical plan
/speckit.plan

# Hook output: "Technical plan saved to docs/artifacts/speckit-plan-20251129-143022.md"
# Review saved plan

# Step 3: Get user approval
# User: "Approved, let's proceed"

# Step 4: Create Meridian task
# Use task-manager skill to create TASK-045
# - Paste spec-kit requirements into TASK-045.yaml
# - Copy approved plan to TASK-045-plan.md

# Step 5: Break down tasks
/speckit.tasks

# Hook output: "Captured 12 tasks from /speckit.tasks"

# Step 6: Create Beads issues for subtasks
bd create "Implement OAuth2 provider abstraction"
bd create "Add Google OAuth2 integration"
# ... etc

# Step 7: Execute with Meridian workflow
# Work on tasks, update TASK-045-context.md

# Step 8: Complete following Definition of Done
# Mark TASK-045 as done in task-backlog.yaml
```

### Example 2: Quick Bug Fix (Lightweight)

```bash
# User: "Fix broken search on mobile"

/speckit.specify Fix search bar overflow on mobile screens

/speckit.plan
# Review simple approach

/speckit.implement
# Spec-kit makes the fix

bd create "Fix search bar overflow on mobile"
bd close "fix(ui): prevent search overflow on mobile"

# No TASK-### created - too lightweight
```

## Validation Requirements

Before creating Meridian tasks from spec-kit outputs, validate using checklists in `.claude/skills/spec-kit/resources/speckit-validation.md`:

**For /speckit.specify**:
- [ ] All requirements complete and testable?
- [ ] Clear acceptance criteria for each?
- [ ] Security/accessibility considered?
- [ ] Dependencies identified?

**For /speckit.plan**:
- [ ] Aligns with existing architecture?
- [ ] All layers addressed (UI/API/DB)?
- [ ] Risks identified with mitigations?
- [ ] Testing strategy defined?
- [ ] Rollback plan included?

**For /speckit.tasks**:
- [ ] Tasks properly scoped (2-6 hours each)?
- [ ] Dependencies ordered correctly?
- [ ] Tests included alongside implementation?
- [ ] All work captured?

## Best Practices

### Do's ✅
- **Always get approval** before creating Meridian task from spec-kit outputs
- **Review spec-kit plans** - they're drafts, not final specifications
- **Use memory-curator** to document spec-kit decisions
- **Update context during implementation** - spec-kit implements, you document
- **Combine with Beads** - use spec-kit tasks to create Beads issues

### Don'ts ❌
- **Don't bypass Meridian approval** - spec-kit generates, humans approve
- **Don't skip Definition of Done** - always verify tests, docs, validation
- **Don't duplicate systems** - Meridian is authoritative for execution state
- **Don't auto-commit spec-kit code** - review before committing (git-safety)

## Troubleshooting

### Hook Not Triggering
**Symptom**: Ran `/speckit.plan` but no output captured
**Solution**: Check `.claude/settings.json` has `speckit-capture.py` registered in PostToolUse hooks

### Can't Find Saved Plans
**Symptom**: Hook said it saved plan but can't find file
**Solution**: Check `docs/artifacts/` directory; files are timestamped `speckit-plan-YYYYMMDD-HHMMSS.md`

### Spec-Kit Output Too Generic
**Symptom**: `/speckit.specify` generated vague requirements
**Solution**: Provide more context in prompt; reference existing code/docs; use constitution

### Conflicting State Between Spec-Kit and Meridian
**Symptom**: Not sure which system has authoritative task state
**Solution**: Meridian `task-backlog.yaml` is always authoritative; spec-kit is for planning only

## Security Considerations

The spec-kit hook:
- ✅ Runs with exit code 0 (non-blocking, never interrupts workflow)
- ✅ Handles malformed JSON gracefully (silent failure)
- ✅ Does NOT write memory.jsonl automatically (suggests only)
- ✅ Creates artifacts in `docs/artifacts/` (not sensitive locations)
- ✅ No external API calls or network operations
- ✅ No execution of user-provided code

## Performance Impact

- Hook execution time: <100ms (minimal overhead)
- File I/O: Only when `/speckit.plan` saves artifacts
- Memory: Negligible (processes JSON in-memory)
- No performance impact on non-spec-kit commands

## Testing Results

### Manual Tests: ✅ All Passing

1. **`/speckit.specify` simulation**: Captured 3 requirements correctly
2. **`/speckit.plan` simulation**: Saved plan to `docs/artifacts/` correctly
3. **`/speckit.tasks` simulation**: Captured 5 tasks correctly
4. **Non-spec-kit command**: Passed through without interference
5. **Malformed JSON**: Handled gracefully (non-blocking)

### Static Analysis: ✅ Passing

- Python syntax check: ✅ No errors
- Hook executable: ✅ Chmod +x applied
- Type annotations: ✅ Corrected (`Any` import added)
- Resource cleanup: ✅ `stdin.close()` added

## Future Enhancements (Optional)

Potential improvements for future iterations:

1. **Structured Data Extraction**: Parse spec-kit YAML/JSON outputs directly (if spec-kit provides structured formats)
2. **Auto-Create TASK Brief**: Hook could scaffold TASK-###.yaml with spec-kit data (requires approval mechanism)
3. **Beads Integration**: Auto-create Beads issues from `/speckit.tasks` output (requires user preference)
4. **Template Customization**: Allow users to customize plan/task output templates
5. **Validation Automation**: Run validation checklists automatically and flag issues

## References

- **Spec-Kit Documentation**: https://github.com/github/spec-kit
- **Claude Code Hooks**: https://docs.claude.com/en/docs/claude-code/hooks
- **Meridian Task Manager**: `.claude/skills/task-manager/SKILL.md`
- **Spec-Kit Skill**: `.claude/skills/spec-kit/SKILL.md`
- **Memory Entries**: `.meridian/memory.jsonl` (mem-0001, mem-0002, mem-0003)

## Installation (For Other Meridian Users)

If you're setting up spec-kit integration in a different Meridian project:

1. **Install spec-kit CLI**:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. **Copy integration files**:
   ```bash
   cp .claude/hooks/speckit-capture.py <your-project>/.claude/hooks/
   chmod +x <your-project>/.claude/hooks/speckit-capture.py

   cp -r .claude/skills/spec-kit/ <your-project>/.claude/skills/
   ```

3. **Update configurations**:
   - Add PostToolUse hook to `.claude/settings.json` (see example above)
   - Add spec-kit skill to `.claude/skills/skill-rules.json`

4. **Create artifacts directory**:
   ```bash
   mkdir -p <your-project>/docs/artifacts
   ```

5. **Test installation**:
   ```bash
   echo '{"tool": "SlashCommand", "input": {"command": "/speckit.specify test"}, "output": "- Test requirement"}' | \
     <your-project>/.claude/hooks/speckit-capture.py
   ```

## Changelog

### Version 1.0 (2025-11-29)
- Initial implementation
- Created `speckit-capture.py` hook
- Created spec-kit skill with resources
- Updated `settings.json` and `skill-rules.json`
- Comprehensive testing and validation
- Documentation complete

---

**Questions or Issues?**
Refer to `.claude/skills/spec-kit/SKILL.md` for detailed usage or troubleshooting sections.
