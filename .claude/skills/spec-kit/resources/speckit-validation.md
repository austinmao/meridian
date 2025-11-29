# Spec-Kit Output Validation Guide

## Why Validate Spec-Kit Outputs?

Spec-kit uses AI to generate specifications and plans. While powerful, AI-generated content requires validation before becoming authoritative project documentation.

**Key principle**: Spec-kit generates drafts, humans approve final specifications.

## Validation Checklist by Command

### /speckit.constitution Validation

**Purpose**: Ensure project principles align with team values and technical constraints.

- [ ] **Completeness**: All relevant principles covered?
  - Coding standards
  - Architectural patterns
  - Security requirements
  - Performance expectations
  - Accessibility standards
- [ ] **Consistency**: Principles don't contradict each other
- [ ] **Feasibility**: Can be realistically followed
- [ ] **Specificity**: Concrete enough to guide decisions
  - ❌ "Write good code"
  - ✅ "Use TypeScript strict mode for all new files"
- [ ] **Alignment**: Matches existing .meridian/CODE_GUIDE.md

**Red flags**:
- Generic principles that could apply to any project
- Contradictory requirements (e.g., "move fast" + "never break things")
- Unrealistic standards (e.g., "100% test coverage for all code")

### /speckit.specify Validation

**Purpose**: Ensure requirements are complete, testable, and aligned with user needs.

- [ ] **Completeness**: All user needs captured?
  - Functional requirements
  - Non-functional requirements (performance, security, UX)
  - Edge cases and error handling
  - Accessibility requirements
- [ ] **Testability**: Each requirement has clear acceptance criteria
  - ❌ "The system should be fast"
  - ✅ "API endpoints respond in < 200ms for p95"
- [ ] **Clarity**: No ambiguous language
  - Avoid: "should", "might", "could", "usually"
  - Prefer: "must", "will", "shall"
- [ ] **Scope**: Bounded appropriately
  - Not too broad (multi-month effort)
  - Not too narrow (trivial change)
- [ ] **Dependencies**: External dependencies identified
  - APIs, services, data sources
  - Team dependencies, approvals needed
- [ ] **Out of Scope**: Explicitly list what's NOT included

**Validation questions**:
1. Can I build this with available resources?
2. How will I test each requirement?
3. What happens if [edge case]?
4. Are there security/privacy implications?
5. Does this align with system architecture?

**Example validation**:

Spec-kit output:
```
- User authentication system
- Social login support
- Remember me functionality
```

Validated version:
```
requirements:
  - id: R1
    description: User authentication with email/password
    acceptance_criteria: |
      - Users can register with email + password (min 8 chars, 1 special char)
      - Users receive email verification within 5 minutes
      - Failed login attempts rate-limited (5 attempts per 15min)
      - Passwords hashed with bcrypt (cost factor 12)
    status: todo

  - id: R2
    description: OAuth2 social login (Google, GitHub)
    acceptance_criteria: |
      - Users can login via Google OAuth2
      - Users can login via GitHub OAuth2
      - User profile synced from OAuth provider (name, email, avatar)
      - OAuth failures gracefully handled with error messages
    status: todo

  - id: R3
    description: "Remember me" persistent sessions
    acceptance_criteria: |
      - Sessions persist for 30 days when "remember me" checked
      - Sessions expire after 24 hours when unchecked
      - Refresh tokens rotated on each use (prevent replay attacks)
      - Users can view/revoke active sessions
    status: todo
```

### /speckit.plan Validation

**Purpose**: Ensure technical approach is sound, feasible, and aligns with architecture.

- [ ] **Architecture Alignment**: Fits existing system design
  - Uses established patterns
  - Doesn't introduce new tech stack without justification
  - Follows architectural principles from constitution
- [ ] **Completeness**: All layers addressed
  - UI/UX changes
  - API endpoints
  - Business logic
  - Data model/schema changes
  - Infrastructure/deployment
- [ ] **Risk Assessment**: Known risks identified
  - Performance bottlenecks
  - Security vulnerabilities
  - Breaking changes
  - Data migration complexity
- [ ] **Dependencies**: External dependencies called out
  - Third-party libraries (with versions)
  - Services/APIs
  - Database schema changes
- [ ] **Testing Strategy**: How will this be tested?
  - Unit tests
  - Integration tests
  - E2E tests
  - Manual testing steps
- [ ] **Rollback Plan**: How to undo if needed?
  - Database migrations reversible?
  - Feature flags for gradual rollout?
  - Backward compatibility maintained?

**Validation questions**:
1. Does this scale to expected load?
2. What's the blast radius if this fails?
3. Can we roll back safely?
4. Are there simpler approaches?
5. Does this create tech debt?

**Red flags**:
- "We'll use [new technology X]" without justification
- No mention of testing
- No consideration of existing code patterns
- Vague implementation steps
- No error handling strategy

**Example validation**:

Spec-kit plan:
```
Use WebSockets for real-time updates
```

Validated plan:
```
## Real-Time Updates Architecture

### Approach: Server-Sent Events (SSE) over WebSockets

**Decision**: Use SSE instead of WebSockets
**Rationale**:
- Unidirectional updates (server → client) sufficient for our use case
- Simpler implementation (HTTP-based, no handshake)
- Automatic reconnection built-in
- Works through corporate proxies (fallback to HTTP/2)

**Alternative considered**: WebSockets
**Rejected because**: Bidirectional communication not needed; adds complexity

### Implementation Plan

1. **Backend**: Add SSE endpoint `/api/events/stream`
   - Use EventSource API on frontend
   - Send keepalive every 15s (prevent timeout)
   - Filter events by user permissions

2. **Frontend**: EventSource client with reconnection
   - Libraries: native EventSource + reconnection wrapper
   - Handle connection failures gracefully
   - Update UI reactively on events

3. **Data Model**: No schema changes needed
   - Existing tables support event sourcing

4. **Testing Strategy**:
   - Unit: Event serialization/deserialization
   - Integration: SSE connection + event delivery
   - E2E: User sees updates in real-time
   - Load: 1000 concurrent connections

5. **Rollback Plan**:
   - Feature flag: `ENABLE_SSE_UPDATES` (default false)
   - Gradual rollout: 10% → 50% → 100%
   - Fallback: Polling (existing mechanism)

### Risks
- **Performance**: 1000+ concurrent connections may impact server
  - Mitigation: Load test before production; horizontal scaling ready
- **Browser compatibility**: EventSource unsupported in IE11
  - Mitigation: Polyfill or graceful degradation to polling
```

### /speckit.tasks Validation

**Purpose**: Ensure task breakdown is actionable, properly scoped, and complete.

- [ ] **Granularity**: Tasks are right-sized
  - Not too large (> 1 day effort)
  - Not too small (< 1 hour effort)
  - Each task has clear definition of done
- [ ] **Dependencies**: Task order makes sense
  - Schema changes before code changes
  - Infrastructure before application code
  - Tests alongside implementation
- [ ] **Completeness**: All work captured
  - Code implementation
  - Tests (unit, integration, E2E)
  - Documentation
  - Database migrations
  - Deployment steps
- [ ] **Clarity**: Each task is self-contained
  - Clear input/output
  - No ambiguous language
  - Specific file paths or components

**Validation process**:
1. Review each task: "Can I complete this independently?"
2. Check order: "Are dependencies satisfied?"
3. Estimate effort: "Is this 2-6 hours of work?"
4. Verify completeness: "Did we forget anything?"

**Example validation**:

Spec-kit tasks:
```
1. Implement authentication
2. Add tests
3. Update documentation
```

Validated tasks:
```
Beads issues (created via bd create):

1. [SCHEMA] Create users table with auth fields (id, email, password_hash, created_at)
   - Definition of done: Migration applied, rollback tested

2. [BACKEND] Implement user registration endpoint POST /api/auth/register
   - Definition of done: Endpoint works, validation present, unit tests pass

3. [BACKEND] Implement login endpoint POST /api/auth/login with JWT
   - Definition of done: Returns JWT token, refresh token, integration tests pass

4. [BACKEND] Add password hashing with bcrypt (cost factor 12)
   - Definition of done: Passwords never stored plaintext, unit tests confirm hashing

5. [BACKEND] Implement OAuth2 flow for Google
   - Definition of done: Google login works, user created/updated, E2E test passes

6. [BACKEND] Implement OAuth2 flow for GitHub
   - Definition of done: GitHub login works, user created/updated, E2E test passes

7. [FRONTEND] Create registration form component
   - Definition of done: Form validates, shows errors, submits to API

8. [FRONTEND] Create login form component with "remember me"
   - Definition of done: Email/password + social login buttons, session persistence works

9. [FRONTEND] Add OAuth2 redirect handlers
   - Definition of done: Google/GitHub callbacks handled, errors shown

10. [TESTS] Add E2E auth flow tests (register → login → protected route)
    - Definition of done: Full auth flow tested, edge cases covered

11. [DOCS] Update API documentation with auth endpoints
    - Definition of done: OpenAPI spec updated, examples provided

12. [SECURITY] Add rate limiting to auth endpoints
    - Definition of done: 5 attempts per 15min enforced, tests confirm
```

## Integration Validation: Spec-Kit → Meridian

Before creating Meridian task from spec-kit outputs:

- [ ] **Approval**: User explicitly approved plan
- [ ] **Requirements refined**: Spec-kit requirements validated and expanded
- [ ] **Plan complete**: Technical approach addresses all requirements
- [ ] **Risks identified**: Known risks documented with mitigations
- [ ] **Tasks scoped**: Task breakdown is actionable
- [ ] **Definition of Done clear**: Know when task is complete
- [ ] **Resources identified**: Links to relevant docs, code, examples

## Common Validation Failures

### Failure: Incomplete Requirements

**Symptom**: Spec-kit output missing critical details

**Example**:
```
- Add user profile page
```

**Problem**: No details on what "profile" includes

**Fix**:
```
- id: R1
  description: User profile page with editable fields
  acceptance_criteria: |
    - Display: name, email, avatar, bio, joined date
    - Editable: name, bio, avatar (upload max 5MB)
    - Save button persists changes to backend
    - Validation: name required, bio max 500 chars
    - Success/error messages shown
  status: todo
```

### Failure: Vague Technical Plan

**Symptom**: Plan lacks implementation details

**Example**:
```
Use a database to store data
```

**Problem**: Which database? What schema?

**Fix**:
```
## Data Storage: PostgreSQL with Prisma ORM

### Decision Rationale
- PostgreSQL: Already used in project, ACID guarantees needed
- Prisma ORM: Type-safe queries, migration management

### Schema Design
\`\`\`prisma
model User {
  id         String   @id @default(uuid())
  email      String   @unique
  passwordHash String?
  name       String
  avatar     String?
  bio        String?
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt
}
\`\`\`

### Migration Strategy
- Create migration: `prisma migrate dev --name add_user_profile`
- Test rollback: `prisma migrate resolve --rolled-back [migration]`
- Apply to staging first, then production
```

### Failure: Missing Testing Strategy

**Symptom**: Plan has no mention of how to verify correctness

**Example**:
```
Implement the feature and test it
```

**Problem**: What tests? How to verify?

**Fix**:
```
## Testing Strategy

### Unit Tests
- User registration validation logic
- Password hashing correctness
- JWT token generation/validation

### Integration Tests
- POST /api/auth/register creates user in DB
- POST /api/auth/login returns valid JWT
- OAuth2 callback updates user profile

### E2E Tests (Playwright)
- Full registration flow
- Login with email/password
- Login with Google OAuth
- Protected route requires auth
- Logout clears session

### Manual Testing Checklist
- [ ] Register new user
- [ ] Login with wrong password (should fail)
- [ ] Login with Google
- [ ] "Remember me" persists session after browser close
- [ ] Session expires after timeout
```

## Validation Workflow

```
1. Run spec-kit command
   └─ Output generated

2. Review output critically
   └─ Apply validation checklist

3. Identify gaps/issues
   └─ Document what's missing

4. Refine output
   └─ Fill gaps, clarify ambiguities

5. Get stakeholder approval
   └─ Explicit "yes" before proceeding

6. Create Meridian artifacts
   └─ Use validated, refined output
```

## When to Reject Spec-Kit Output

Sometimes spec-kit generates unusable content. Reject and regenerate if:

- **Too generic**: Could apply to any project
- **Incomplete**: Missing critical requirements or approach details
- **Infeasible**: Proposes approach that won't work with existing architecture
- **Contradictory**: Requirements conflict with each other
- **Unsafe**: Security/privacy issues not addressed

**How to improve**:
- Provide more context in prompt
- Reference existing code/docs: "following pattern in src/auth/..."
- Use constitution to guide: "adhering to .meridian/docs/constitution.md"
- Iterate: Run `/speckit.specify` again with refined prompt

## Validation Documentation

After validation, document what you changed:

**In TASK-###-context.md**:
```markdown
## Spec-Kit Validation Notes (2025-11-29)

### Requirements Refinement
- Added acceptance criteria for vague requirements
- Clarified "real-time updates" to mean < 1s latency
- Added error handling requirements (spec-kit missed these)

### Plan Modifications
- Changed from WebSockets to SSE (simpler for unidirectional updates)
- Added rollback plan (spec-kit didn't include)
- Specified exact libraries: EventSource polyfill for IE11 compat

### Tasks Expanded
- Broke "implement auth" into 12 specific tasks
- Added security task (rate limiting) - spec-kit missed this
- Ordered tasks by dependency (schema → backend → frontend)
```

**In memory.jsonl** (via memory-curator skill):
```json
{
  "id": "mem-XXXX",
  "summary": "**Decision:** Always validate spec-kit outputs before creating Meridian tasks.\n**Problem:** Spec-kit generates drafts that need refinement.\n**Pattern:** Run spec-kit → validate using checklists → refine gaps → get approval → create task.\n**Lesson:** Spec-kit for TASK-043 missed rate limiting requirement; now always check security explicitly.",
  "tags": ["lesson", "spec-kit", "validation", "security"]
}
```

This ensures future tasks benefit from lessons learned during validation.
