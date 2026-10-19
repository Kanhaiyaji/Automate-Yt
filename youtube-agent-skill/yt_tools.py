#!/usr/bin/env python3
"""yt_tools.py - Unified CLI runner for YouTube Agent tools.

Usage:
    python yt_tools.py hook --hook "one line"
    python yt_tools.py title --title "..." --thumb "..."
    python yt_tools.py deadair transcript.srt [--floor 0.35]
    python yt_tools.py chapters transcript.srt [--target 8]
    python yt_tools.py retention retention.csv [--duration 600] [--transcript transcript.srt]
    python yt_tools.py swipe collected.json [--min 2.0]
    python yt_tools.py learn [--formula the-statistic | --topic "AI" | --packaging | --retention | --quiz]
"""
import sys, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

TOOLS = {
    "hook": os.path.join(HERE, "skills", "yt-script", "hookscore.py"),
    "hookscore": os.path.join(HERE, "skills", "yt-script", "hookscore.py"),
    "title": os.path.join(HERE, "skills", "yt-package", "title.py"),
    "package": os.path.join(HERE, "skills", "yt-package", "title.py"),
    "deadair": os.path.join(HERE, "skills", "yt-edit", "deadair.py"),
    "edit": os.path.join(HERE, "skills", "yt-edit", "deadair.py"),
    "chapters": os.path.join(HERE, "skills", "yt-chapters", "chapters.py"),
    "retention": os.path.join(HERE, "skills", "yt-retention", "retention.py"),
    "swipe": os.path.join(HERE, "skills", "yt-viral", "swipe.py"),
    "viral": os.path.join(HERE, "skills", "yt-viral", "swipe.py"),
    "learn": os.path.join(HERE, "skills", "yt-learn", "learn.py"),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        print("Available tools:")
        for name in sorted(set(TOOLS.keys())):
            target = TOOLS[name]
            exists = " [ready]" if os.path.exists(target) else " [missing]"
            print(f"  - {name:<12} -> {os.path.relpath(target, HERE)}{exists}")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd not in TOOLS:
        print(f"Unknown tool '{cmd}'. Choose from: {', '.join(sorted(TOOLS.keys()))}")
        sys.exit(1)

    target_script = TOOLS[cmd]
    if not os.path.exists(target_script):
        print(f"Error: Target script not found at {target_script}")
        sys.exit(1)

    # Pass remaining args to target script
    args = [sys.executable, target_script] + sys.argv[2:]
    res = subprocess.run(args)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
