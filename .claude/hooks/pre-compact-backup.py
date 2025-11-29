#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Pre-compact backup hook.
Backs up critical context files before compaction to prevent data loss.
"""

import sys
import json
from pathlib import Path
import os
from datetime import datetime
import shutil


def backup_context() -> str:
    """Backup critical context files before compaction."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    base_dir = Path(project_dir)

    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = base_dir / ".meridian" / "backups" / f"compact_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed_up = []

    # Files to backup
    critical_files = [
        ".meridian/memory.jsonl",
        ".meridian/task-backlog.yaml",
        ".meridian/config.yaml",
    ]

    # Backup each critical file
    for file_path in critical_files:
        source = base_dir / file_path
        if source.exists():
            dest = backup_dir / source.name
            shutil.copy2(source, dest)
            backed_up.append(source.name)

    # Backup active tasks (in_progress or blocked)
    tasks_dir = base_dir / ".meridian" / "tasks"
    if tasks_dir.exists():
        tasks_backup = backup_dir / "tasks"
        for task_folder in tasks_dir.iterdir():
            if task_folder.is_dir() and task_folder.name.startswith("TASK-"):
                task_yaml = task_folder / f"{task_folder.name}.yaml"
                if task_yaml.exists():
                    # Check if task is active
                    content = task_yaml.read_text()
                    if "in_progress" in content or "blocked" in content:
                        # Backup entire task folder
                        dest_folder = tasks_backup / task_folder.name
                        shutil.copytree(task_folder, dest_folder)
                        backed_up.append(f"tasks/{task_folder.name}/")

    # Clean old backups (keep last 10)
    backups_root = base_dir / ".meridian" / "backups"
    if backups_root.exists():
        backups = sorted(
            [b for b in backups_root.iterdir() if b.is_dir()],
            key=lambda p: p.stat().st_mtime
        )
        for old_backup in backups[:-10]:
            shutil.rmtree(old_backup)

    return str(backup_dir), backed_up


def main() -> int:
    try:
        backup_path, backed_up = backup_context()
        if backed_up:
            items = ", ".join(backed_up)
            print(f"[PRE-COMPACT] Backed up: {items}\n  Location: {backup_path}")
        return 0
    except Exception as e:
        sys.stderr.write(f"Pre-compact backup error: {e}\n")
        return 0  # Non-blocking


if __name__ == "__main__":
    sys.exit(main())
