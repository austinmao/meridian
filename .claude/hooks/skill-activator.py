#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Skill auto-activation hook for UserPromptSubmit events.
Suggests relevant skills based on prompt keywords and file context.
Also logs prompts and manages session data.

Based on patterns from: https://github.com/disler/claude-code-hooks-mastery
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
import os


def get_project_dir() -> Path:
    """Get project directory from environment."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.cwd()
    return Path(project_dir)


def log_user_prompt(input_data: dict, project_dir: Path) -> None:
    """Log user prompt to logs/user_prompts.jsonl."""
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "user_prompts.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": input_data.get("session_id", "unknown"),
        "prompt": input_data.get("prompt", ""),
        "files": input_data.get("files", []),
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def manage_session_data(session_id: str, prompt: str, project_dir: Path) -> None:
    """Store prompts per session for context."""
    sessions_dir = project_dir / ".claude" / "data" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    session_file = sessions_dir / f"{session_id}.json"

    if session_file.exists():
        try:
            session_data = json.loads(session_file.read_text())
        except (json.JSONDecodeError, ValueError):
            session_data = {"session_id": session_id, "prompts": []}
    else:
        session_data = {"session_id": session_id, "prompts": []}

    session_data["prompts"].append({
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
    })

    # Keep only last 50 prompts per session
    session_data["prompts"] = session_data["prompts"][-50:]

    session_file.write_text(json.dumps(session_data, indent=2))


def validate_prompt(prompt: str) -> tuple[bool, str | None]:
    """
    Validate prompt for blocked patterns.
    Returns (is_valid, reason_if_blocked).
    """
    # Define blocked patterns (customize as needed)
    blocked_patterns = [
        # Add patterns here if needed, e.g.:
        # (r"delete\s+all", "Bulk deletion requests require explicit confirmation"),
    ]

    prompt_lower = prompt.lower()
    for pattern, reason in blocked_patterns:
        if re.search(pattern, prompt_lower):
            return False, reason

    return True, None


def load_skill_rules(project_dir: Path) -> dict:
    """Load skill-rules.json configuration."""
    rules_path = project_dir / ".claude" / "skills" / "skill-rules.json"

    if not rules_path.exists():
        return {"skills": []}

    try:
        return json.loads(rules_path.read_text())
    except Exception as e:
        sys.stderr.write(f"Failed to load skill-rules.json: {e}\n")
        return {"skills": []}


def match_skill(skill_config: dict, prompt: str, files: list) -> bool:
    """Check if skill should activate based on triggers."""
    triggers = skill_config.get("triggers", {})

    # Check prompt keywords
    keywords = triggers.get("prompt_keywords", [])
    prompt_lower = prompt.lower()
    for keyword in keywords:
        if keyword.lower() in prompt_lower:
            return True

    # Check file patterns
    file_patterns = triggers.get("file_patterns", [])
    for file_path in files:
        for pattern in file_patterns:
            # Simple glob-like matching
            pattern_regex = pattern.replace("**", ".*").replace("*", "[^/]*")
            if re.search(pattern_regex, file_path):
                return True

    # Check tool patterns in prompt
    tool_patterns = triggers.get("tool_patterns", [])
    for tool_pattern in tool_patterns:
        if tool_pattern.lower() in prompt_lower:
            return True

    return False


def main() -> int:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--validate",
            action="store_true",
            help="Validate prompts against blocked patterns",
        )
        parser.add_argument(
            "--log-prompts",
            action="store_true",
            help="Log all user prompts",
        )
        parser.add_argument(
            "--store-session",
            action="store_true",
            help="Store prompts per session",
        )
        args = parser.parse_args()

        input_data = json.load(sys.stdin)
        sys.stdin.close()

        prompt = input_data.get("prompt", "")
        files = input_data.get("files", [])
        session_id = input_data.get("session_id", "unknown")

        project_dir = get_project_dir()

        # Log prompt if enabled
        if args.log_prompts:
            log_user_prompt(input_data, project_dir)

        # Store session data if enabled
        if args.store_session:
            manage_session_data(session_id, prompt, project_dir)

        # Validate prompt if enabled
        if args.validate:
            is_valid, reason = validate_prompt(prompt)
            if not is_valid:
                print(f"[PROMPT BLOCKED] {reason}", file=sys.stderr)
                return 2  # Block the prompt

        # Load skill rules
        rules = load_skill_rules(project_dir)

        # Find matching skills
        matching_skills = []
        for skill in rules.get("skills", []):
            if match_skill(skill, prompt, files):
                skill_name = skill["name"]
                skill_desc = skill.get("description", "")
                matching_skills.append((skill_name, skill_desc))

        # Output suggestions if any matches found
        if matching_skills:
            suggestions = "\n".join(
                [f"  - **{name}**: {desc}" for name, desc in matching_skills]
            )
            output = f"""
[SKILL ACTIVATOR] Relevant skills detected:

{suggestions}

Consider using the Skill tool to load these before proceeding.
"""
            print(output)

        return 0

    except Exception as e:
        sys.stderr.write(f"Skill activator error: {e}\n")
        return 0  # Non-blocking


if __name__ == "__main__":
    sys.exit(main())
