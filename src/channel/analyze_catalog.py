#!/usr/bin/env python3
"""analyze_catalog.py - Inspects top candidate videos from @jhajiog for clutch moments."""
import subprocess, json, sys, os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CANDIDATES = [
    {"id": "09ugnAq0Vz4", "name": "WINNER OF 3 TOURNAMENT IN ONE DAY"},
    {"id": "Tw3NtuIuZxU", "name": "HACKER........? JHAJIOG !"},
    {"id": "qI4nr1emrYs", "name": "SCARFALL THE END GAME | TOURNAMENTS CLIPS"},
    {"id": "Q0Xvf-3Rwyw", "name": "FRAGS | DROP CLASH | RUNNER UP | ODDSOCEAN"},
    {"id": "bbUuD0yIEhg", "name": "KIROK CLIP | PDA THA DAAL DIYA"},
    {"id": "9uDbOT-WQZo", "name": "Storage Clear kr rha hu | Part 2"}
]

def inspect_video(vid_id):
    url = f"https://www.youtube.com/watch?v={vid_id}"
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json",
        "--skip-download",
        url
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    if res.returncode == 0 and res.stdout.strip():
        data = json.loads(res.stdout)
        return {
            "id": vid_id,
            "title": data.get("title"),
            "duration": data.get("duration"),
            "view_count": data.get("view_count"),
            "like_count": data.get("like_count"),
            "comment_count": data.get("comment_count"),
            "description": data.get("description", "")[:250],
            "tags": data.get("tags", [])[:8]
        }
    return None

if __name__ == "__main__":
    results = []
    print("Analyzing top candidate videos...")
    for c in CANDIDATES:
        info = inspect_video(c["id"])
        if info:
            results.append(info)
            dur_m, dur_s = divmod(info["duration"], 60)
            print(f"- [{info['id']}] {info['title']}")
            print(f"  Duration: {dur_m}m {dur_s}s | Views: {info['view_count']} | Likes: {info['like_count']}")
            print(f"  Tags: {', '.join(info['tags'])}")
            print()
    with open("top_candidates_analysis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
