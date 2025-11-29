#!/usr/bin/env python3

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional


def get_git_branch() -> Optional[str]:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_uncommitted_count() -> Optional[int]:
    """Get count of uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            lines = [l for l in result.stdout.strip().split("\n") if l]
            return len(lines)
    except Exception:
        pass
    return None


def get_github_issues(limit: int = 5) -> Optional[list]:
    """Get open GitHub issues if gh CLI is available and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "issue", "list", "--limit", str(limit), "--json", "number,title"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def format_git_context() -> str:
    """Format git context for display."""
    lines = []

    branch = get_git_branch()
    if branch:
        lines.append(f"- Branch: `{branch}`")

    uncommitted = get_git_uncommitted_count()
    if uncommitted is not None:
        if uncommitted == 0:
            lines.append("- Working tree: clean")
        else:
            lines.append(f"- Uncommitted changes: {uncommitted} file(s)")

    issues = get_github_issues()
    if issues:
        lines.append(f"- Open GitHub issues: {len(issues)}")
        for issue in issues[:3]:  # Show top 3
            lines.append(f"  - #{issue['number']}: {issue['title'][:50]}")

    if lines:
        return "\n".join(lines)
    return "- (git context unavailable)"


def read_file(path: Path) -> str:
    if path.is_file():
        return path.read_text()
    else:
        # Match bash helper behavior: print a "(missing: ...)" marker
        return f"(missing: {path})\n"


def main() -> int:
    claude_project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    base_dir = Path(claude_project_dir)

    # Determine project type and TDD mode (defaults)
    config_file = base_dir / ".meridian" / "config.yaml"
    project_type = "standard"
    tdd_mode = "false"

    if config_file.is_file():
        try:
            for line in config_file.read_text().splitlines():
                stripped = line.lstrip()
                if stripped.startswith("project_type:"):
                    pt_value = stripped.split(":", 1)[1].strip().lower()
                    if pt_value in {"hackathon", "standard", "production"}:
                        project_type = pt_value
                    else:
                        project_type = "standard"
                elif stripped.startswith("tdd_mode:"):
                    tdd_value = stripped.split(":", 1)[1].strip().lower()
                    if tdd_value in {"true", "yes", "on", "1"}:
                        tdd_mode = "true"
                    else:
                        tdd_mode = "false"
        except Exception:
            # On parse error, keep defaults
            project_type = "standard"
            tdd_mode = "false"

    # Build CODE_GUIDE_FILES snippet for insertion into the markdown
    code_guide_files = f"- `{claude_project_dir}/.meridian/CODE_GUIDE.md`"

    if project_type == "hackathon":
        code_guide_files += (
            f"\n- `{claude_project_dir}/.meridian/CODE_GUIDE_ADDON_HACKATHON.md`"
        )
    elif project_type == "production":
        code_guide_files += (
            f"\n- `{claude_project_dir}/.meridian/CODE_GUIDE_ADDON_PRODUCTION.md`"
        )

    if tdd_mode == "true":
        code_guide_files += (
            f"\n- `{claude_project_dir}/.meridian/CODE_GUIDE_ADDON_TDD.md`"
        )

    # Load session reload template
    reload_template_path = (
        base_dir / ".claude" / "hooks" / "prompts" / "session-reload.md"
    )
    reload_context = read_file(reload_template_path)

    # Expand $CLAUDE_PROJECT_DIR placeholders
    reload_context = reload_context.replace("$CLAUDE_PROJECT_DIR", claude_project_dir)

    # Inject the CODE_GUIDE_FILES block
    reload_context = reload_context.replace("{{CODE_GUIDE_FILES}}", code_guide_files)

    # Inject git context
    git_context = format_git_context()
    reload_context = reload_context.replace("{{GIT_CONTEXT}}", git_context)

    additional_context = (
        f"<reload_context_system_message>{reload_context}"
        f"</reload_context_system_message>"
    )

    # payload = {
    #     "systemMessage": (
    #         "[Meridian] Session restored. Key project files were reloaded so Claude can "
    #         "continue work without losing context. If you see any errors during this process, "
    #         "don't worry, they are intentional."
    #     ),
    #     "hookSpecificOutput": {
    #         "hookEventName": "SessionStart",
    #         "additionalContext": additional_context,
    #     },
    #     "suppressOutput": True,
    # }

    # print(json.dumps(payload, indent=2, ensure_ascii=False))

    print(additional_context, end="")

    # Create flag to force Claude to review context on next tool use
    needs_context_review = base_dir / ".meridian" / ".needs-context-review"
    try:
        needs_context_review.parent.mkdir(parents=True, exist_ok=True)
        needs_context_review.touch(exist_ok=True)
    except Exception:
        # Ignore errors to match bash behavior (no explicit error handling)
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
