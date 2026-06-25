#!/usr/bin/env python
"""Run LaTeX engine from Python.

Usage examples:
  python run_latex.py --cmd pdflatex --file paper/test.tex --runs 1
  python run_latex.py --cmd latexmk --file paper/test.tex --extra "-pdf" --runs 1

This script checks that the requested engine is on PATH and runs it, streaming output.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a LaTeX engine from Python")
    parser.add_argument("--cmd", default="pdflatex", help="LaTeX command to run (pdflatex, latexmk, etc.)")
    parser.add_argument("--file", required=True, help="Path to .tex file to compile")
    parser.add_argument("--runs", type=int, default=1, help="Number of times to run the engine")
    parser.add_argument("--workdir", help="Working directory to run in (defaults to file parent)")
    parser.add_argument("--extra", nargs="*", help="Extra args to pass to the engine")

    args = parser.parse_args(argv)

    cmd = args.cmd
    tex_path = Path(args.file)
    if not tex_path.exists():
        print(f"Error: file does not exist: {tex_path}")
        return 2

    engine_path = shutil.which(cmd)
    if engine_path is None:
        print(f"Error: '{cmd}' not found on PATH. Install TeX (TeX Live / MikTeX) or add it to PATH.")
        return 3

    workdir = Path(args.workdir) if args.workdir else tex_path.parent
    extra = args.extra or []

    # Prepare base command. For pdflatex, use nonstopmode to avoid interactive prompts.
    base_cmd = [engine_path]
    if cmd.lower().endswith("pdflatex"):
        base_cmd += ["-interaction=nonstopmode"]

    base_cmd += extra

    full_cmd = base_cmd + [str(tex_path.name)]

    print(f"Using engine: {engine_path}")
    print(f"Working directory: {workdir}")
    print(f"Command: {' '.join(full_cmd)}")

    # Run the specified number of times
    for i in range(1, args.runs + 1):
        print(f"--- Run {i}/{args.runs} ---")
        try:
            proc = subprocess.run(full_cmd, cwd=str(workdir), check=False)
        except KeyboardInterrupt:
            print("Interrupted by user")
            return 4
        if proc.returncode != 0:
            print(f"Engine exited with code {proc.returncode}")
            return proc.returncode

    print("Finished successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
