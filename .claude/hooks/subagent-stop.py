#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
SubagentStop hook - fires when a subagent (Task tool) completes.
Logs subagent completion and optionally converts transcript to chat log.

Based on patterns from: https://github.com/disler/claude-code-hooks-mastery
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def get_project_dir() -> Path:
    """Get project directory from environment."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.cwd()
    return Path(project_dir)


def log_subagent_stop(input_data: dict, project_dir: Path) -> None:
    """Log subagent completion to logs/subagent_stop.jsonl."""
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "subagent_stop.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": input_data.get("session_id", "unknown"),
        "subagent_type": input_data.get("subagent_type", "unknown"),
        "stop_hook_active": input_data.get("stop_hook_active", False),
        "data": input_data,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def convert_transcript_to_chat(input_data: dict, project_dir: Path) -> None:
    """Convert subagent transcript to chat.json for analysis."""
    transcript_path = input_data.get("transcript_path")
    if not transcript_path or not os.path.exists(transcript_path):
        return

    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    try:
        chat_data = []
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        chat_data.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        # Save with timestamp to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        chat_file = log_dir / f"subagent_chat_{timestamp}.json"
        with open(chat_file, "w") as f:
            json.dump(chat_data, f, indent=2)

    except Exception:
        pass  # Fail silently


def announce_completion() -> None:
    """Announce subagent completion via system TTS."""
    try:
        if sys.platform == "darwin":
            subprocess.run(
                ["say", "-v", "Samantha", "Subagent complete"],
                capture_output=True,
                timeout=10,
            )
        elif sys.platform.startswith("linux"):
            subprocess.run(
                ["espeak", "Subagent complete"],
                capture_output=True,
                timeout=10,
            )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass


def main() -> int:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--chat",
            action="store_true",
            help="Copy transcript to chat.json",
        )
        parser.add_argument(
            "--notify",
            action="store_true",
            help="Enable TTS completion announcement",
        )
        args = parser.parse_args()

        input_data = json.load(sys.stdin)
        sys.stdin.close()

        project_dir = get_project_dir()

        # Log the subagent stop event
        log_subagent_stop(input_data, project_dir)

        # Optionally convert transcript to chat format
        if args.chat:
            convert_transcript_to_chat(input_data, project_dir)

        # Optionally announce completion
        if args.notify:
            announce_completion()

        return 0  # Non-blocking

    except json.JSONDecodeError:
        return 0
    except Exception as e:
        sys.stderr.write(f"SubagentStop hook error: {e}\n")
        return 0  # Non-blocking


if __name__ == "__main__":
    sys.exit(main())
