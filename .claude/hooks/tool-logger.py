#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Tool usage logger hook for PostToolUse events.
Creates comprehensive audit trail of all tool executions.
"""

import sys
import json
from pathlib import Path
import os
from datetime import datetime


def sanitize_content(data: dict, max_length: int = 200) -> dict:
    """Sanitize and truncate large content fields."""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str) and len(value) > max_length:
            sanitized[key] = f"<truncated: {len(value)} chars>"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_content(value, max_length)
        else:
            sanitized[key] = value
    return sanitized


def log_tool_use(data: dict) -> None:
    """Log tool usage to JSON file."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    logs_dir = Path(project_dir) / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Append to daily log file
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"tool-usage_{date_str}.jsonl"

    # Add timestamp
    data["timestamp"] = datetime.now().isoformat()

    # Append as JSONL (one JSON object per line)
    with open(log_file, "a") as f:
        f.write(json.dumps(data) + "\n")


def main() -> int:
    try:
        input_data = json.load(sys.stdin)

        tool = input_data.get("tool", "")
        tool_input = input_data.get("input", {})
        output = input_data.get("output", "")

        # Sanitize large content
        sanitized_input = sanitize_content(tool_input)

        # Extract relevant information
        log_entry = {
            "tool": tool,
            "input": sanitized_input,
            "output_length": len(str(output)) if output else 0,
            "success": not input_data.get("error", False),
        }

        # Don't log full content for file operations
        if tool in ["Read", "Write", "Edit"]:
            log_entry["file_path"] = tool_input.get("file_path", "unknown")

        log_tool_use(log_entry)
        return 0

    except Exception as e:
        sys.stderr.write(f"Tool logger error: {e}\n")
        return 0  # Non-blocking


if __name__ == "__main__":
    sys.exit(main())
