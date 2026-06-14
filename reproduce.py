#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reproduce.py — run every numbered stage of the Beating Substrate Framework and report a summary.

Each stage is a self-contained, pre-registered numerical experiment (observable + null hypothesis
declared before running), with negative controls where relevant. This driver executes them all in
order and reports, for each, whether it ran cleanly and a one-line digest of its output.

It does NOT judge physics — it only checks reproducibility (that each script runs and produces its
reported output). The honest status of each result (forced / conditional / adopted / open) lives in
CHARTER.md, not here.

Usage:
    python reproduce.py            # run all stages
    python reproduce.py --quiet    # summary only
    python reproduce.py 34 41      # run only stages whose number is in {34, 41}

Requirements: Python 3.10+, NumPy, SciPy (and scikit-learn for a few early stages).
"""
import os
import re
import sys
import glob
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# stage scripts may live in ./scripts/ or alongside this file
SEARCH_DIRS = [os.path.join(HERE, "scripts"), HERE]
TIMEOUT = 600  # seconds per stage


def stage_key(path):
    """Sort key: numeric prefix then any letter suffix (so stage14 < stage14b < stage14c < stage15)."""
    name = os.path.basename(path)
    m = re.match(r"stage(\d+)([a-z]*)_", name)
    if not m:
        return (10**9, "", name)
    return (int(m.group(1)), m.group(2), name)


def find_stages(selectors):
    files = {}
    for d in SEARCH_DIRS:
        for f in glob.glob(os.path.join(d, "stage*_*.py")):
            files[os.path.basename(f)] = f  # dedupe by basename, prefer scripts/ (listed first)
    paths = sorted(files.values(), key=stage_key)
    if selectors:
        wanted = set(selectors)
        paths = [p for p in paths if str(stage_key(p)[0]) in wanted]
    return paths


def first_signal_line(out):
    """A short digest: the last non-empty, non-separator line of stdout (usually the verdict)."""
    for line in reversed(out.strip().splitlines()):
        s = line.strip()
        if s and not set(s) <= set("=-_ "):
            return s[:110]
    return ""


def check_dependencies():
    """Verify required packages are importable. We CHECK rather than auto-install: silently running
    `pip install` would modify the user's environment without consent. If anything is missing, point
    the user to requirements.txt and stop cleanly."""
    missing = []
    for mod in ("numpy", "scipy"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    try:
        __import__("sklearn")
    except ImportError:
        print("note: scikit-learn not found — a few early stages need it (pip install scikit-learn).")
    if missing:
        print("Missing required packages: " + ", ".join(missing))
        print("Install dependencies first:  pip install -r requirements.txt")
        return False
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    if not check_dependencies():
        return 1
    stages = find_stages(args)
    if not stages:
        print("No stage scripts found. Place stageN_*.py in ./scripts/ or next to reproduce.py.")
        return 1

    print(f"Beating Substrate Framework — reproducing {len(stages)} stage(s)\n" + "=" * 64)
    passed, failed = 0, []
    for path in stages:
        name = os.path.basename(path)
        try:
            r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=TIMEOUT)
            ok = (r.returncode == 0)
        except subprocess.TimeoutExpired:
            ok, r = False, None
        if ok:
            passed += 1
            tag = "PASS"
            digest = "" if quiet else "  | " + first_signal_line(r.stdout)
        else:
            failed.append(name)
            tag = "FAIL"
            if r is None:
                digest = "  | timeout"
            else:
                err = (r.stderr.strip().splitlines() or [""])[-1]
                digest = "  | " + err[:110]
        print(f"[{tag}] {name}{digest}")

    print("=" * 64)
    print(f"{passed}/{len(stages)} stages ran cleanly.")
    if failed:
        print("Did not run cleanly: " + ", ".join(failed))
        print("(Check that NumPy/SciPy are installed; note np.trapz was renamed np.trapezoid in recent NumPy.)")
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
