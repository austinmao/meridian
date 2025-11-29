#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Spec-kit capture hook for PostToolUse events.
Captures spec-kit slash command outputs and bridges them to Meridian task system.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any
import os

# Spec-kit command patterns
SPECKIT_COMMANDS = {
    "/speckit.constitution": "constitution",
    "/speckit.specify": "specify",
    "/speckit.plan": "plan",
    "/speckit.tasks": "tasks",
    "/speckit.implement": "implement",
}


def get_project_dir() -> Path:
    """Get project directory from environment."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.cwd()
    return Path(project_dir)


def extract_speckit_command(tool_name: str, tool_input: dict) -> str | None:
    """Extract spec-kit command from SlashCommand tool usage."""
    if tool_name != "SlashCommand":
        return None

    command = tool_input.get("command", "")
    for speckit_cmd in SPECKIT_COMMANDS:
        if command.startswith(speckit_cmd):
            return SPECKIT_COMMANDS[speckit_cmd]
    return None


def capture_specify_to_context(output: str) -> dict[str, str]:
    """
    Capture /speckit.specify output and prepare for TASK.yaml requirements.
    Returns structured data for requirements section.
    """
    lines = output.split("\n")
    requirements = []
    current_req = None

    for line in lines:
        # Look for requirement patterns
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            if current_req:
                requirements.append(current_req)
            current_req = line.strip()[2:]
        elif current_req and line.strip():
            current_req += f" {line.strip()}"

    if current_req:
        requirements.append(current_req)

    return {
        "type": "specify",
        "requirements": requirements,
        "raw_output": output,
    }


def capture_plan_to_markdown(output: str, project_dir: Path) -> Path | None:
    """
    Capture /speckit.plan output and save to docs/artifacts/.
    Returns path to saved plan file.
    """
    artifacts_dir = project_dir / "docs" / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    plan_file = artifacts_dir / f"speckit-plan-{timestamp}.md"

    plan_content = f"""# Spec-Kit Technical Plan
Generated: {datetime.now().isoformat()}

{output}

---
*This plan was captured from spec-kit output. Review and approve before creating a Meridian task.*
"""

    plan_file.write_text(plan_content)
    return plan_file


def capture_tasks_output(output: str) -> dict[str, Any]:
    """
    Capture /speckit.tasks output and prepare for task creation.
    Returns structured task data.
    """
    tasks = []
    lines = output.split("\n")

    for line in lines:
        line = line.strip()
        # Match task patterns like "1. Task description" or "- [ ] Task"
        if re.match(r"^\d+\.", line) or line.startswith("- [ ]"):
            task_text = re.sub(r"^(\d+\.|\- \[ \])\s*", "", line)
            if task_text:
                tasks.append(task_text)

    return {
        "type": "tasks",
        "task_list": tasks,
        "raw_output": output,
    }


def suggest_memory_entry(speckit_type: str) -> str:
    """
    Suggest memory.jsonl entry content - DO NOT write automatically.
    Returns suggestion text for memory-curator skill.
    """
    summary_map = {
        "specify": "**Decision:** Captured spec-kit requirements for consideration.\n**Problem:** Need structured requirements for implementation.\n**Pattern:** Use spec-kit /speckit.specify to generate initial requirements, then refine into Meridian TASK.yaml format.",
        "plan": "**Decision:** Captured spec-kit technical plan.\n**Problem:** Need implementation approach.\n**Pattern:** Use spec-kit /speckit.plan to draft approach, save to docs/artifacts/, review/approve before creating Meridian task.",
        "tasks": "**Decision:** Captured spec-kit task breakdown.\n**Problem:** Need actionable task list.\n**Pattern:** Use spec-kit /speckit.tasks for initial breakdown, then integrate with Meridian task system or Beads for execution.",
    }

    suggestion = summary_map.get(speckit_type, "")
    if suggestion:
        return f"\n💡 Consider using memory-curator skill to document:\n{suggestion}\nTags: [tooling, spec-kit, pattern]\n"
    return ""


def main() -> int:
    try:
        input_data = json.load(sys.stdin)
        sys.stdin.close()  # Close stdin after reading

        tool_name = input_data.get("tool", "")
        tool_input = input_data.get("input", {})
        tool_output = input_data.get("output", "")

        # Check if this is a spec-kit command
        speckit_type = extract_speckit_command(tool_name, tool_input)
        if not speckit_type:
            return 0  # Not a spec-kit command, pass through

        project_dir = get_project_dir()

        # Process based on spec-kit command type
        result_info = None

        if speckit_type == "specify":
            data = capture_specify_to_context(tool_output)
            result_info = f"\n[SPECKIT CAPTURE] Captured {len(data['requirements'])} requirements from /speckit.specify\n"
            result_info += "Next steps:\n"
            result_info += "  1. Review requirements in context\n"
            result_info += "  2. Run /speckit.plan to create technical approach\n"
            result_info += "  3. After approval, create Meridian task with these requirements\n"
            result_info += suggest_memory_entry(speckit_type)

        elif speckit_type == "plan":
            plan_file = capture_plan_to_markdown(tool_output, project_dir)
            if plan_file:
                result_info = f"\n[SPECKIT CAPTURE] Technical plan saved to {plan_file.relative_to(project_dir)}\n"
                result_info += "Next steps:\n"
                result_info += "  1. Review the saved plan\n"
                result_info += "  2. Get user approval\n"
                result_info += "  3. Use task-manager skill to create TASK-###-plan.md from this content\n"
                result_info += suggest_memory_entry(speckit_type)

        elif speckit_type == "tasks":
            data = capture_tasks_output(tool_output)
            result_info = f"\n[SPECKIT CAPTURE] Captured {len(data['task_list'])} tasks from /speckit.tasks\n"
            result_info += "Next steps:\n"
            result_info += "  1. Review task breakdown\n"
            result_info += "  2. Create Beads issues for individual tasks, OR\n"
            result_info += "  3. Add to TASK-###-context.md as implementation checklist\n"
            result_info += suggest_memory_entry(speckit_type)

        elif speckit_type == "implement":
            result_info = "\n[SPECKIT CAPTURE] /speckit.implement detected\n"
            result_info += "Reminder: Update TASK-###-context.md with progress notes during implementation\n"

        # Output info to user (shown in transcript)
        if result_info:
            print(result_info)

        return 0  # Non-blocking

    except Exception as e:
        sys.stderr.write(f"Speckit capture error: {e}\n")
        return 0  # Non-blocking - fail gracefully


if __name__ == "__main__":
    sys.exit(main())
