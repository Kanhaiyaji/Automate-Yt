#!/usr/bin/env python3
"""explore_channel.py - Fetches and categorizes videos from @jhajiog."""
import subprocess, json, sys, os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def get_channel_videos(tab="videos"):
    url = f"https://www.youtube.com/@jhajiog/{tab}"
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-json",
        url
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    videos = []
    for line in res.stdout.splitlines():
        if line.strip():
            try:
                videos.append(json.loads(line))
            except Exception:
                pass
    return videos

if __name__ == "__main__":
    tab = sys.argv[1] if len(sys.argv) > 1 else "videos"
    vids = get_channel_videos(tab)
    print(f"=== Channel @jhajiog / {tab.upper()} ({len(vids)} items) ===")
    out_list = []
    for v in vids:
        vid_id = v.get("id")
        title = v.get("title")
        dur = v.get("duration")
        views = v.get("view_count")
        url = v.get("url") or f"https://www.youtube.com/watch?v={vid_id}"
        out_list.append({
            "id": vid_id,
            "title": title,
            "duration": dur,
            "view_count": views,
            "url": url
        })
    with open(f"channel_{tab}.json", "w", encoding="utf-8") as f:
        json.dump(out_list, f, indent=2)
    
    # Print top 15
    for i, item in enumerate(out_list[:15]):
        dur_str = f"{int(item['duration']//60)}m {int(item['duration']%60)}s" if item['duration'] else "N/A"
        print(f"{i+1:2d}. [{item['id']}] ({dur_str}) {item['title']}")
