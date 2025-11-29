#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Security guard hook for PreToolUse events.
Blocks dangerous commands and sensitive file access.
"""

import sys
import json
import re
from pathlib import Path
import os

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',           # rm -rf variations
    r'sudo\s+rm',                           # privileged delete
    r'chmod\s+777',                         # world-writable
    r'>\s*/etc/',                           # write to system dirs
    r'curl.*\|\s*sh',                       # pipe to shell
    r'wget.*\|\s*bash',                     # download and execute
    r'dd\s+if=',                            # disk operations
    r'mkfs\.',                              # filesystem creation
    r':(){:|:&};:',                         # fork bomb
    r'git\s+commit\s+.*--no-verify',        # bypass pre-commit hooks
    r'git\s+commit\s+.*-n\b',               # bypass pre-commit hooks (short)
]

# Sensitive file patterns
SENSITIVE_FILE_PATTERNS = [
    r'\.env(?!\.sample|\.example|\.template)', # .env files (not samples)
    r'\.aws/credentials',                   # AWS credentials
    r'\.ssh/id_',                           # SSH private keys
    r'credentials\.json',                   # credential files
    r'\.pem$',                              # certificate files
]


def check_dangerous_command(command: str) -> tuple[bool, str]:
    """Check if command contains dangerous patterns."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Blocked dangerous pattern: {pattern}"
    return True, ""


def check_sensitive_file_access(tool: str, params: dict) -> tuple[bool, str]:
    """Check if tool accesses sensitive files."""
    if tool not in ["Read", "Write", "Edit"]:
        return True, ""

    file_path = params.get("file_path", "")
    if not file_path:
        return True, ""

    for pattern in SENSITIVE_FILE_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return False, f"Blocked access to sensitive file: {file_path}"

    return True, ""


def main() -> int:
    try:
        input_data = json.load(sys.stdin)

        tool = input_data.get("tool", "")
        params = input_data.get("input", {})

        # Check Bash commands for dangerous patterns
        if tool == "Bash":
            command = params.get("command", "")
            is_safe, reason = check_dangerous_command(command)
            if not is_safe:
                response = {
                    "decision": "block",
                    "reason": f"[SECURITY GUARD] {reason}\n\nCommand blocked for safety. If this is intentional, modify .claude/hooks/security-guard.py patterns."
                }
                print(json.dumps(response))
                sys.stderr.write(f"Security block: {reason}\n")
                return 2  # Block execution

        # Check file operations for sensitive files
        is_safe, reason = check_sensitive_file_access(tool, params)
        if not is_safe:
            response = {
                "decision": "block",
                "reason": f"[SECURITY GUARD] {reason}\n\nAccess to sensitive files is restricted."
            }
            print(json.dumps(response))
            sys.stderr.write(f"Security block: {reason}\n")
            return 2  # Block execution

        # Approved - allow execution
        return 0

    except Exception as e:
        sys.stderr.write(f"Security guard error: {e}\n")
        return 0  # Fail open - don't block on errors


if __name__ == "__main__":
    sys.exit(main())
