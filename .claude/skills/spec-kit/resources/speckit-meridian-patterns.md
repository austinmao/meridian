# Spec-Kit Meridian Integration Patterns

## Pattern 1: Full Spec-Driven Feature Development

### When to Use
- Complex features requiring approval
- Multiple stakeholder review needed
- Cross-cutting changes affecting architecture

### Workflow
```
1. Constitution Phase (Optional)
   └─ /speckit.constitution
      ├─ Review project principles
      └─ Update .meridian/config.yaml if needed

2. Specification Phase
   └─ /speckit.specify [feature description]
      ├─ Hook captures requirements
      ├─ Review with stakeholders
      └─ Refine until approved

3. Planning Phase
   └─ /speckit.plan
      ├─ Hook saves to docs/artifacts/
      ├─ Review technical approach
      ├─ Identify risks and trade-offs
      └─ Get explicit approval

4. Task Creation Phase
   └─ Use task-manager skill
      ├─ Create TASK-###/
      ├─ Populate TASK-###.yaml with spec-kit requirements
      ├─ Copy approved plan to TASK-###-plan.md
      ├─ Add initial context entry
      └─ Update task-backlog.yaml

5. Breakdown Phase
   └─ /speckit.tasks
      ├─ Hook extracts task list
      ├─ Create Beads issues for each subtask
      └─ Link to TASK via beads_epic_id field

6. Implementation Phase
   └─ /speckit.implement OR manual execution
      ├─ Execute tasks using Beads workflow
      ├─ Update TASK-###-context.md with progress
      └─ Document decisions as they arise

7. Completion Phase
   └─ Meridian Definition of Done
      ├─ All tests pass
      ├─ Documentation updated
      ├─ Use memory-curator for architectural decisions
      └─ Mark task as done in task-backlog.yaml
```

### Example
```bash
# User: "Add user authentication with OAuth2"

# Step 1: Specify requirements
/speckit.specify OAuth2 authentication with Google and GitHub providers

# Step 2: Review captured requirements
# [Hook shows: Captured 8 requirements from /speckit.specify]

# Step 3: Create technical plan
/speckit.plan

# Step 4: Review saved plan
# [Hook shows: Technical plan saved to docs/artifacts/speckit-plan-20251129-143500.md]

# Step 5: Get approval (ask user explicitly)
# User approves plan

# Step 6: Create Meridian task
# Use task-manager skill to create TASK-043
# - Copy requirements from spec-kit output
# - Copy plan from docs/artifacts/speckit-plan-20251129-143500.md

# Step 7: Break down into tasks
/speckit.tasks

# Step 8: Create Beads issues
bd create "Implement OAuth2 provider abstraction"
bd create "Add Google OAuth2 integration"
bd create "Add GitHub OAuth2 integration"
bd create "Create auth middleware"
bd create "Add user session management"

# Step 9: Execute
bd ready
# ... work on first task ...
bd close "feat: implement OAuth2 provider abstraction"

# Repeat for remaining tasks
```

## Pattern 2: Lightweight Spec-Driven Development (No Meridian Task)

### When to Use
- Bug fixes
- Small refactoring
- Documentation updates
- Dependency updates
- Changes not requiring stakeholder approval

### Workflow
```
1. Quick Specification
   └─ /speckit.specify [brief description]
      └─ Generate lightweight spec

2. Simple Plan
   └─ /speckit.plan
      └─ Draft approach (review but don't save)

3. Execute
   └─ /speckit.implement
      └─ Spec-kit executes changes

4. Track with Beads
   └─ bd create "Fix: [description]"
      └─ bd close with commit SHA

5. No Meridian Task Created
   └─ Too lightweight for TASK-###
```

### Example
```bash
# User: "The search bar placeholder text is cut off on mobile"

/speckit.specify Fix search bar placeholder overflow on mobile

/speckit.plan
# Reviews simple CSS fix

/speckit.implement
# Makes the change

bd create "Fix search bar placeholder overflow on mobile"
bd close "fix(ui): prevent search placeholder text overflow on mobile screens"

# No TASK-### created - tracked only in Beads
```

## Pattern 3: Spec-Kit for Requirements Discovery + Manual Implementation

### When to Use
- You want spec-kit's requirement analysis but prefer manual coding
- Learning new domain/technology where spec-kit helps explore
- Prototyping where you want structure but hands-on implementation

### Workflow
```
1. Discovery Phase
   └─ /speckit.specify [feature]
      ├─ Hook captures requirements
      └─ Use as starting point, refine manually

2. Planning Phase
   └─ /speckit.plan
      ├─ Hook saves plan
      └─ Review, extract key insights

3. Task Creation
   └─ Create Meridian TASK-### with refined requirements
      └─ Use spec-kit outputs as input, not verbatim

4. Manual Implementation
   └─ Skip /speckit.implement
      ├─ Code manually following plan
      ├─ Update TASK-###-context.md
      └─ Use Beads for subtask tracking

5. Completion
   └─ Standard Meridian Definition of Done
```

### Example
```bash
# User: "Add real-time collaboration to the editor"

# Use spec-kit to understand requirements
/speckit.specify Real-time collaboration for code editor with conflict resolution

# Review requirements (8 captured)
# Identify gaps: "Needs offline support", "Needs conflict resolution strategy"

# Use spec-kit for technical exploration
/speckit.plan

# Review plan (WebSocket approach, operational transforms)
# Decision: Use CRDTs instead of OT (more suitable for our use case)

# Create Meridian task manually
# Use task-manager skill: Create TASK-044
# - Refine spec-kit requirements + add offline support
# - Modify plan to use CRDTs
# - Document decision: "Chose CRDTs over OT due to..."

# Implement manually (no /speckit.implement)
bd ready
# ... code CRDT implementation ...
bd close "feat: implement CRDT-based collaborative editing"

# Document architectural decision
# Use memory-curator skill to record CRDT decision
```

## Pattern 4: Hybrid Spec-Kit + Meridian Validation

### When to Use
- Using spec-kit implementation but want Meridian's verification rigor
- Spec-kit implements, you validate quality gates
- Automated implementation with manual quality control

### Workflow
```
1-3. Standard Spec-Kit Flow
    └─ /speckit.specify → /speckit.plan → Get approval

4. Create Meridian Task
   └─ Standard task creation with spec-kit outputs

5. Spec-Kit Implementation
   └─ /speckit.implement
      └─ Let spec-kit write code

6. Meridian Validation Gates
   └─ Run validation commands from TASK-###.yaml
      ├─ pnpm lint
      ├─ pnpm typecheck
      ├─ pnpm test
      └─ Manual verification steps

7. Iterate if Needed
   └─ If validation fails:
      ├─ Document failures in TASK-###-context.md
      ├─ Fix issues (manually or with spec-kit)
      └─ Re-run validation

8. Complete with Memory
   └─ Use memory-curator for lessons learned
      └─ "Spec-kit implementation required X fixes"
```

## Pattern 5: Spec-Kit Constitution as Project Standards

### When to Use
- Starting new project
- Onboarding new AI agents/developers
- Establishing coding conventions

### Workflow
```
1. Create Constitution
   └─ /speckit.constitution
      ├─ Define project principles
      ├─ Establish patterns
      └─ Set quality standards

2. Save to Meridian
   └─ Copy to .meridian/docs/constitution.md
      └─ Reference in CODE_GUIDE.md

3. Use in Task Creation
   └─ TASK-###.yaml implementation_notes:
      ├─ "CRITICAL: Follow .meridian/docs/constitution.md"
      └─ Reference specific constitutional principles

4. Validate Against Constitution
   └─ During code review:
      ├─ Check adherence to principles
      └─ Document violations/exceptions in context
```

## Integration Decision Matrix

| Feature Complexity | Approval Needed? | Use Spec-Kit? | Create Meridian Task? | Use Beads? |
|-------------------|------------------|---------------|----------------------|------------|
| Simple bug fix | No | Optional | No | Yes |
| Refactoring | No | Optional | No | Yes |
| Small feature | No | Yes (specify + plan) | No | Yes |
| Medium feature | Yes | Yes (full workflow) | Yes | Yes (subtasks) |
| Large feature | Yes | Yes (full workflow) | Yes | Yes (subtasks) |
| Architectural change | Yes | Yes (specify + plan) | Yes | Yes (subtasks) |

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Spec-Kit Bypassing Approval
```bash
# WRONG: Implementing without approval
/speckit.specify new feature
/speckit.plan
/speckit.implement  # ← NO! Get approval first
```

**Correct**:
```bash
/speckit.specify new feature
/speckit.plan
# → Get user approval ←
# → Create Meridian task ←
/speckit.implement
```

### ❌ Anti-Pattern 2: Duplicate Tracking Systems
```bash
# WRONG: Tracking in both spec-kit and Meridian without integration
/speckit.tasks  # Creates spec-kit task list
# Also create TASK-###.yaml with separate tasks
# Now two sources of truth
```

**Correct**:
```bash
/speckit.tasks
# Use output to create Beads issues OR add to TASK-###-context.md
# Single source of truth: Meridian (task-backlog.yaml)
```

### ❌ Anti-Pattern 3: Skipping Validation
```bash
# WRONG: Trusting spec-kit implementation without verification
/speckit.implement
git add .
git commit -m "feat: implemented by spec-kit"  # ← NO! Validate first
```

**Correct**:
```bash
/speckit.implement
# Run validation commands
pnpm lint && pnpm typecheck && pnpm test
# Review changes
# Then commit
```

### ❌ Anti-Pattern 4: Over-Using Spec-Kit for Simple Tasks
```bash
# WRONG: Full spec-kit workflow for trivial change
/speckit.constitution
/speckit.specify Fix typo in README
/speckit.plan
/speckit.tasks
/speckit.implement
# Creates TASK-045 with full brief
```

**Correct**:
```bash
# Just fix it
# Edit README directly
bd create "Fix typo in README"
bd close "docs: fix typo in installation section"
```

## Memory Documentation Patterns

After using spec-kit, document key decisions:

```json
{
  "id": "mem-XXXX",
  "timestamp": "2025-11-29T14:35:00Z",
  "summary": "**Decision:** Use spec-kit for feature planning, Meridian for execution tracking.\n**Problem:** Needed structured planning workflow.\n**Alternatives:** Manual planning (rejected: less structured); spec-kit only (rejected: lacks execution tracking).\n**Trade-offs:** Two systems add overhead but provide planning rigor + execution tracking.\n**Impact/Scope:** Use spec-kit specify/plan for requirements, create Meridian tasks post-approval, track with Beads.\n**Pattern:** Spec-kit generates, humans approve, Meridian tracks.",
  "tags": ["tooling", "spec-kit", "meridian", "pattern", "decision"],
  "links": [".claude/skills/spec-kit/", ".meridian/tasks/", "mem-0001"]
}
```

Use `memory-curator` skill to create these entries - don't edit memory.jsonl manually.
