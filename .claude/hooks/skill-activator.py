#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Skill auto-activation hook for UserPromptSubmit events.
Suggests relevant skills based on prompt keywords and file context.
"""

import sys
import json
import re
from pathlib import Path
import os


def load_skill_rules() -> dict:
    """Load skill-rules.json configuration."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    rules_path = Path(project_dir) / ".claude" / "skills" / "skill-rules.json"

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
        input_data = json.load(sys.stdin)

        prompt = input_data.get("prompt", "")
        files = input_data.get("files", [])

        # Load skill rules
        rules = load_skill_rules()

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
