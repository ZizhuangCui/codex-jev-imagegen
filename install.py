#!/usr/bin/env python3
"""Install the Codex skill without dependencies or overwriting existing files."""
import argparse
import os
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    parser.add_argument("--skills-dir", type=Path, default=default, help="Parent skills directory")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / "skills" / "jev-imagegen"
    target = args.skills_dir.expanduser() / "jev-imagegen"
    if target.exists() or target.is_symlink():
        print("Installation already exists; back it up or choose another --skills-dir.", file=sys.stderr)
        return 1
    try:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    except OSError:
        print("Installation failed. Check source files and destination permissions; inspect any partial copy.", file=sys.stderr)
        return 1
    print("Installed jev-imagegen at " + str(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
