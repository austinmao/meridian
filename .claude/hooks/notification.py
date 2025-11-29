#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Notification hook - fires when Claude Code sends notifications.
Logs notifications and optionally announces via system TTS.

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


def log_notification(input_data: dict, project_dir: Path) -> None:
    """Log notification to logs/notification.jsonl."""
    log_dir = project_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "notification.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "message": input_data.get("message", ""),
        "session_id": input_data.get("session_id", "unknown"),
        "data": input_data,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def announce_notification(message: str) -> None:
    """
    Announce notification via system TTS.
    Uses macOS 'say' command, or espeak on Linux.
    Fails silently if not available.
    """
    try:
        # Try macOS 'say' command
        if sys.platform == "darwin":
            subprocess.run(
                ["say", "-v", "Samantha", message],
                capture_output=True,
                timeout=10,
            )
        # Try Linux espeak
        elif sys.platform.startswith("linux"):
            subprocess.run(
                ["espeak", message],
                capture_output=True,
                timeout=10,
            )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass  # TTS is optional, fail silently


def main() -> int:
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--notify",
            action="store_true",
            help="Enable TTS notifications",
        )
        parser.add_argument(
            "--log-only",
            action="store_true",
            help="Only log, no TTS even if --notify is set",
        )
        args = parser.parse_args()

        input_data = json.load(sys.stdin)
        sys.stdin.close()

        project_dir = get_project_dir()

        # Log the notification
        log_notification(input_data, project_dir)

        # Announce if enabled and message indicates user input needed
        message = input_data.get("message", "")
        if (
            args.notify
            and not args.log_only
            and "waiting" in message.lower()
        ):
            announce_notification("Your agent needs your input")

        return 0  # Non-blocking

    except json.JSONDecodeError:
        return 0
    except Exception as e:
        sys.stderr.write(f"Notification hook error: {e}\n")
        return 0  # Non-blocking


if __name__ == "__main__":
    sys.exit(main())
