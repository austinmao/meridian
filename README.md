![Logo](https://github.com/user-attachments/assets/9eb140c8-b938-4e77-ab94-0461a6d919fd)
# **Meridian** — a zero‑config Claude Code setup for Tasks, Memory & Guardrails

Make Claude Code **predictable**: preserved context, enforced rules, in‑repo tasks, optional TDD—without changing how you talk to Claude.

* **Zero‑config install**: copy two folders, make scripts executable, and go.
* **Deterministic behavior**: hooks *enforce* the right steps (not just suggest them).
* **Persistent context**: tasks, memory, and docs live in your repo.
* **Plug‑in rules**: baseline `CODE_GUIDE.md` + project‑type add‑ons + optional **TDD** override.
* **Zero behavior change**: no commands, no scripts, no special phrasing. You talk to Claude normally; Meridian handles everything behind the scenes.

> If this setup helps, please ⭐ star the repo and share it.

---

## Why this setup exists

Default Claude Code often loses context after compaction, forgets history, and drifts from standards. Claude is customizable—**hooks** and **skills** let you shape behavior—but you need a structure that **can’t be skipped**.

**Meridian** adds lightweight guardrails so Claude:

* **Documents tasks** (brief, approved plan, context) in your repo.
* **Follows guides** (baseline + add‑ons) every session—re‑injected by hooks.
* **Reads relevant docs** you list—every startup/reload.
* **Curates memory** of durable decisions (append‑only `memory.jsonl`).
* **Never loses context after compaction**: hooks reinject the essential docs, standards, and the task Claude was working on so it always returns with full context.

You keep chatting normally; **Claude** does the rest.

---

## Zero‑config (really)

* No API keys or service wiring required.
* No code changes to your project.
* No subagent orchestration to maintain.

Just copy two folders, make scripts executable, and continue working with Claude as usual.
No workflow changes for the developer — no slash commands, no scripts, no special instructions. You interact with Claude exactly as you already do.

---

## Quick start

### Option 1: Install as Claude Code Plugin (Recommended)

Add Meridian to your project's `.claude/settings.json`:

```json
{
  "plugins": ["plugin:austinmao/meridian@main"]
}
```

Then initialize the `.meridian/` folder in your project:

```
/init-meridian
```

This gives you all skills, agents, commands, and hooks without copying files—they load from the Meridian repository.

### Option 2: Manual Installation (Full Control)

```bash
# 0) Get this setup
git clone https://github.com/austinmao/meridian.git meridian-setup
cd meridian-setup

# 1) Copy to your project root
cp -R .claude .meridian /path/to/your/project
cd /path/to/your/project

# 2) Make hooks & skills executable
find .claude -type f -name '*.py' -print0 | xargs -0 chmod +x

# 3) (Optional) choose project type / TDD in config
#    .meridian/config.yaml → project_type: hackathon|standard|production; tdd_mode: true|false
```

Open your repo in **Claude Code** and talk to Claude as always.
Hooks inject the system prompt, guides, tasks, memory, and docs—and **Claude** follows them.

---

## Talk in **Plan mode** (important)

**Describe work in Plan mode** so Claude proposes a plan you can approve.
When you approve the plan, a hook **forces Claude** to create a task (`TASK-###` folder with brief/plan/context) and update the backlog—**every time**.

Why Plan mode?

* Planning quality improves (fewer back‑and‑forths).
* Exiting Plan mode is a reliable signal for the hook to persist the task plan.
* Your repo becomes the *single source of truth* for ongoing work.

> Shortcut: **Shift + Tab** to switch modes in Claude Code.

---

## What this setup includes

### Main agent manual

The core system prompt that sets behavior and guardrails.
**Default file:** `.meridian/prompts/agent-operating-manual.md`

### Guides

* **Baseline:** `.meridian/CODE_GUIDE.md` (Next.js/React + Node/TS + general rules).
* **Add‑ons (auto‑injected by config):**

  * `CODE_GUIDE_ADDON_HACKATHON.md` — loosens requirements for simpler projects (not only hackathons).
  * `CODE_GUIDE_ADDON_PRODUCTION.md` — tightens requirements for production needs.
  * `CODE_GUIDE_ADDON_TDD.md` — **overrides all testing rules**; tests first (Red→Green→Refactor), even in hackathon mode.

### Tasks (after every **approved plan**)

Each task lives in `.meridian/tasks/TASK-###/`:

* `TASK-###.yaml` — brief (objective, scope, constraints, acceptance criteria, deliverables, risks, links)
* `TASK-###-plan.md` — the **approved plan** (amendments tracked)
* `TASK-###-context.md` — timestamped notes (decisions, blockers, PR links; `MEMORY:` markers)

Backlog: `.meridian/task-backlog.yaml` tracks status (`todo`, `in_progress`, `blocked`, `done`).

These task folders aren’t just for the developer — Claude actively uses them to restore context after startup or compaction.

### Relevant docs

List any must‑read docs in `.meridian/relevant-docs.md`. Claude loads them on startup/reload.

**Example:**

```md
Always read these files before continuing your work:
- `.meridian/docs/langgraph.md`
- `backend/feature/email/subscriptions.md`
```

### Memory (append‑only)

`memory.jsonl` stores durable decisions and patterns. Claude reads it automatically.

This memory exists primarily for Claude’s benefit: issues it encountered, architectural decisions, pitfalls, and patterns it should not repeat.

* Claude uses the script (never edits manually):

  ```
  .claude/skills/memory-curator/scripts/add_memory_entry.py \
    --summary "Decision/Pattern…" --tags architecture,pattern --links "TASK-012 services/x.ts"
  ```

---

## Project types (what they mean)

Set in `.meridian/config.yaml`:

```yaml
project_type: standard   # hackathon | standard | production
tdd_mode: false          # true enables TDD add-on and overrides testing rules
```

* **hackathon** — a *loosened* mode for simpler projects and fast iteration.
  Use it whenever you don’t need production‑level code quality.
* **standard** — the baseline defaults; balanced for most work.
* **production** — a *stricter* mode for production‑grade needs: security, reliability, perf.

**TDD (`tdd_mode: true`)**: Tests are written **first** for each behavior slice; this **overrides** any testing guidance from hackathon/production/baseline.

**Precedence:** baseline → project‑type add‑on → **TDD** (if enabled; TDD wins on test rules).

---

## How it actually runs (Claude does the work)

1. **Startup/Reload**
   Hooks inject the Agent Operating Manual, guides, memory, backlog, relevant docs, and the active task state. Claude cannot proceed until it has reabsorbed this context, ensuring no loss after compaction.
2. **Plan**
   You describe the task in Plan mode; Claude proposes a plan.

3. **Approve plan**
   A hook forces Claude to create `TASK-###` (brief/plan/context) and update the backlog.

4. **Implement**
   Claude writes code following the guides, reads docs listed in `relevant-docs.md`, updates `TASK-###-context.md`, and—if needed—adds memory entries via the script.

   * **If TDD is on:** Claude writes a failing test first, makes it pass, then refactors (per slice).

5. **Compaction/Resume**
   Reload hook re-injects guidelines, memory, docs, and the task Claude was working on. A guard blocks tools until Claude finishes reviewing this restored context and syncs task notes.
   
6. **Stop**
   Stop hook blocks exit until Claude verifies tests/lint/build are clean and task/memory/doc updates are saved. If nothing changed, Claude states it and stops.

> You don’t perform these steps manually—**Claude does**. You chat, approve, and review as normal.

---

## Hooks (what each one enforces)

* **`claude-init.py`** — on session start
  Injects the manual, baseline guide, the selected project-type add-on, TDD (if enabled), memory, backlog, relevant docs, and the active task context. This ensures Claude always starts with the correct context. Sets a “must review” flag.
  
* **`session-reload.py` + `prompts/session-reload.md`** — on compaction/resume
  Re-injects all essential context Claude needs after compaction (guidelines, memory, docs, active task). Ensures Claude cannot “come back empty.” Asks Claude to sync task notes before continuing. Sets the “must review” flag again.
  
* **`post-compact-guard.py`** — before tool use
  If the review flag exists, denies tool usage once with a reminder, then clears the flag.

* **`plan-approval-reminder.py`** — when exiting Plan mode
  Blocks until Claude creates `TASK-###` via **task‑manager** and updates the backlog (skips for tiny one‑off fixes).

* **`pre-stop-update.py`** — on stop
  Blocks until Claude updates task files/backlog/memory and verifies tests/lint/build (or states “nothing to update”).

These guardrails turn guidance into **deterministic behavior**.

---

## Skills (how Claude writes things down)

* **task‑manager**
  Script `create-task.py` creates `TASK-###` from a template and enforces filenames.
  Skill doc `SKILL.md` defines when to create tasks, status transitions, and templates.

* **memory‑curator**
  Script `add_memory_entry.py` appends a JSON line (auto id + UTC timestamp).
  Skill doc `SKILL.md` defines the concise summary format and tag taxonomy.

---

## FAQ

**Is “hackathon” only for hackathons?**
No. It’s just a label for the *looser* mode—use it for any simpler project where production strength isn’t required.

**Why not subagents?**
They don’t share the full live context, re‑read docs (token waste), can’t be resumed after interrupts, and their actions may not make it back into memory. This setup focuses on making every single interaction more efficient and traceable. You can still add subagents for specialized work if you like.

**Will TDD slow me down?**
In hackathon mode, tests remain minimal but are still **first**. For critical paths, TDD tends to reduce regressions and rework.

**Can I add project‑specific rules?**
Yes—edit `CODE_GUIDE.md` (e.g., “use Drizzle instead of Prisma”). Because the guide is injected each session, Claude will follow it.

---

## Contribute & License

PRs and issues welcome
License: MIT

---

## Star & share

If Meridian improves your Claude sessions:

* ⭐ **Star this repo** so others can find it.
