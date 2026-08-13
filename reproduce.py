"""Single entry point for the inexpensive artifact reproduction workflow."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "verify": ROOT / "reproduction/verify_artifact.py",
    "results": ROOT / "reproduction/reproduce_reported_results.py",
    "figures": ROOT / "reproduction/reproduce_figures.py",
}


def _run(name: str) -> None:
    subprocess.run((sys.executable, str(COMMANDS[name])), cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the deposit and reproduce reported summaries and Figures 1–5."
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("all", *COMMANDS),
        default="all",
        help="Workflow step to run (default: all inexpensive steps).",
    )
    args = parser.parse_args()
    names = tuple(COMMANDS) if args.command == "all" else (args.command,)
    for name in names:
        print(f"\n>>> {name}", flush=True)
        _run(name)


if __name__ == "__main__":
    main()
