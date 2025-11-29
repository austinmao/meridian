---
name: spec-kit
description: Use GitHub's spec-kit for spec-driven development workflow integrated with Meridian tasks
---

<role>
Spec-Kit Integration Specialist - Guide spec-driven development workflow from specification to implementation, bridging spec-kit outputs with Meridian's task management system.
</role>

<objective>
Enable spec-driven development by leveraging spec-kit's structured workflow (constitution → specify → plan → tasks → implement) while maintaining Meridian's task management rigor and architectural memory.
</objective>

<spec_kit_overview>
## What is Spec-Kit?

Spec-kit is GitHub's toolkit for spec-driven development - writing specifications BEFORE code, not after. Instead of coding first and documenting later, you create contracts that define behavior, then use AI agents to generate, test, and validate code against those specs.

**Core Philosophy**: Specifications are the source of truth. Code is generated to meet specs.

**Installation**:
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**Workflow Phases**:
1. **Constitution** (`/speckit.constitution`) - Project principles and guidelines
2. **Specify** (`/speckit.specify`) - Requirements and user stories (the "what")
3. **Plan** (`/speckit.plan`) - Technical implementation approach (the "how")
4. **Tasks** (`/speckit.tasks`) - Actionable task breakdown
5. **Implement** (`/speckit.implement`) - Execute tasks according to specs

</spec_kit_overview>

<integration_with_meridian>
## How Spec-Kit Integrates with Meridian

### Decision Tree: When to Use What

```
Complex feature needing stakeholder approval? → Meridian TASK-###
  ├─ Use /speckit.specify to draft requirements
  ├─ Use /speckit.plan to create technical approach
  └─ Create TASK-###.yaml with approved spec-kit outputs

Architectural decision or pattern? → memory.jsonl (memory-curator skill)
  └─ Capture spec-kit decisions about approach, trade-offs

Quick implementation or discovered bugs? → Beads issues
  └─ Use /speckit.tasks output to create Beads issues
```

### Meridian-Spec-Kit Workflow

**Phase 1: Specification (Pre-Approval)**
1. Run `/speckit.constitution` to align on project principles (if not already defined)
2. Run `/speckit.specify [feature description]` to generate requirements
   - Hook captures output automatically
   - Review requirements for completeness
3. Run `/speckit.plan` to draft technical approach
   - Hook saves to `docs/artifacts/speckit-plan-TIMESTAMP.md`
   - Review plan with stakeholders

**Phase 2: Task Creation (Post-Approval)**
4. Get explicit user approval of spec-kit plan
5. Use `task-manager` skill to create Meridian task:
   - `TASK-###.yaml` ← requirements from /speckit.specify
   - `TASK-###-plan.md` ← approved plan from /speckit.plan
   - `TASK-###-context.md` ← initial context entry
6. Update `.meridian/task-backlog.yaml` with new task

**Phase 3: Execution**
7. Run `/speckit.tasks` to break down implementation
   - Use output to create Beads issues, OR
   - Add as checklist to TASK-###-context.md
8. Run `/speckit.implement` (optional - spec-kit executes tasks)
   - Alternative: Execute tasks manually using Meridian workflow
9. Update TASK-###-context.md with progress notes during work

**Phase 4: Completion**
10. Follow Meridian Definition of Done (tests, docs, validation)
11. Use `memory-curator` to capture architectural decisions
12. Mark task as `done` in task-backlog.yaml

</integration_with_meridian>

<automation_hooks>
## Automatic Spec-Kit Capture

The `speckit-capture.py` hook (PostToolUse) automatically:

1. **Detects spec-kit commands**: Monitors for `/speckit.*` slash commands
2. **Captures outputs**:
   - `/speckit.specify` → Extracts requirements structure
   - `/speckit.plan` → Saves plan to `docs/artifacts/speckit-plan-TIMESTAMP.md`
   - `/speckit.tasks` → Extracts task list
3. **Creates memory entries**: Documents spec-kit usage patterns
4. **Provides next-step guidance**: Shows what to do with captured data

**No manual intervention required** - hook runs automatically after each spec-kit command.

</automation_hooks>

<workflow_mapping>
## Spec-Kit → Meridian Artifact Mapping

| Spec-Kit Command | Meridian Artifact | Purpose |
|------------------|-------------------|---------|
| `/speckit.constitution` | `.meridian/config.yaml` or `docs/` | Project principles (optional - use if missing) |
| `/speckit.specify` | `TASK-###.yaml` (requirements section) | What needs to be built |
| `/speckit.plan` | `TASK-###-plan.md` | How it will be built (approved approach) |
| `/speckit.tasks` | Beads issues OR `TASK-###-context.md` checklist | Task breakdown for execution |
| `/speckit.implement` | Code execution + context updates | Implementation with progress tracking |

</workflow_mapping>

<best_practices>
## Best Practices for Spec-Kit with Meridian

### Do's
- **Always get approval** before creating Meridian task from spec-kit outputs
- **Review spec-kit plans** - they're drafts, not gospel
- **Use memory-curator** to document spec-kit decisions (don't edit memory.jsonl manually)
- **Update context during implementation** - spec-kit implements, you document progress
- **Combine with Beads** - use spec-kit tasks to create Beads issues for lightweight tracking

### Don'ts
- **Don't bypass Meridian approval workflow** - spec-kit generates specs, humans approve
- **Don't skip Definition of Done** - spec-kit implements, but you verify (tests, docs, validation)
- **Don't duplicate systems** - if Meridian task exists, don't create parallel spec-kit tracking
- **Don't auto-commit spec-kit code** - review before committing (git-safety protocol)

### When to Skip Meridian Tasks

Use **only** spec-kit + Beads for:
- Simple bug fixes discovered during development
- Refactoring that doesn't change behavior
- Documentation updates
- Dependency updates

These don't need full Meridian task briefs.

</best_practices>

<common_patterns>
## Common Integration Patterns

### Pattern 1: Feature Planning with Spec-Kit
```
User: "I want to add dark mode to the dashboard"

1. /speckit.specify dark mode for dashboard
   → Hook captures requirements
2. /speckit.plan
   → Hook saves to docs/artifacts/speckit-plan-20251129-143022.md
3. Review plan with user, get approval
4. Use task-manager skill:
   - Create TASK-042
   - Paste spec-kit requirements into TASK-042.yaml
   - Paste approved plan into TASK-042-plan.md
5. /speckit.tasks
   → Hook extracts task list
6. Create Beads issues for each task (bd create "...")
   - Link to TASK-042 via beads_epic_id
7. Implement using Beads workflow (bd ready → work → bd close)
8. Update TASK-042-context.md with progress
9. Complete TASK-042 following Definition of Done
```

### Pattern 2: Quick Implementation (No Meridian Task)
```
User: "Fix the broken logout button"

1. /speckit.specify logout button fix
   → Quick spec generation
2. /speckit.plan
   → Simple approach
3. /speckit.implement
   → Spec-kit executes fix
4. Create Beads issue: bd create "Fix logout button"
5. bd close with commit SHA
6. No TASK-### needed (too lightweight)
```

### Pattern 3: Architectural Decision Documentation
```
During /speckit.plan, spec-kit recommends using WebSockets instead of polling.

1. Review spec-kit's reasoning
2. Make decision (approve or override)
3. Use memory-curator skill to document:
   - Decision: Use WebSockets for real-time updates
   - Alternatives: Polling, Server-Sent Events
   - Trade-offs: Complexity vs. performance
   - Rationale: From spec-kit analysis + team discussion
```

</common_patterns>

<troubleshooting>
## Common Issues

**Issue**: Spec-kit commands not triggering hook
- **Solution**: Check `.claude/settings.json` has `speckit-capture.py` in PostToolUse hooks
- **Solution**: Verify hook file is executable: `chmod +x .claude/hooks/speckit-capture.py`

**Issue**: Hook captures data but doesn't create memory entries
- **Solution**: Ensure `.meridian/memory.jsonl` exists
- **Solution**: Check hook error messages in stderr

**Issue**: Can't find saved spec-kit plans
- **Solution**: Check `docs/artifacts/` directory
- **Solution**: Plans are timestamped: `speckit-plan-YYYYMMDD-HHMMSS.md`

**Issue**: Spec-kit and Meridian have conflicting task states
- **Solution**: Use Meridian as authoritative state (task-backlog.yaml)
- **Solution**: Spec-kit is for planning, Meridian for tracking execution

</troubleshooting>

<resources>
## Additional Resources

- **Spec-Kit Documentation**: https://github.com/github/spec-kit
- **Meridian Task Manager**: `.claude/skills/task-manager/SKILL.md`
- **Meridian Workflow**: `.claude/skills/meridian-workflow/SKILL.md`
- **Memory Curator**: `.claude/skills/memory-curator/SKILL.md`
- **Beads Integration**: See `.meridian/memory.jsonl` entries mem-0001, mem-0002, mem-0003

For deeper technical details on spec-kit integration patterns, see:
- `resources/speckit-meridian-patterns.md` - Detailed integration workflows
- `resources/speckit-validation.md` - How to validate spec-kit outputs before task creation

</resources>
