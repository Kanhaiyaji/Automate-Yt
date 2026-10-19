#!/usr/bin/env python3
"""find_all_kills.py - Scans source_full_sd3.mp4.webm for exact kill moments, finish counts, and knocks."""
import subprocess, os, sys, json, re

def extract_key_frames(video_path, out_dir="shorts/frames"):
    os.makedirs(out_dir, exist_ok=True)
    # Extract 1 frame per second at reduced resolution for quick analysis
    print(f"Extracting 1 frame per second from {video_path}...")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", "fps=1,scale=640:288",
        "-q:v", "5",
        os.path.join(out_dir, "frame_%04d.jpg")
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    frames = sorted([f for f in os.listdir(out_dir) if f.endswith(".jpg")])
    print(f"Extracted {len(frames)} frames to {out_dir}.")
    return frames

if __name__ == "__main__":
    vid = "shorts/source_full_sd3.mp4.webm"
    if not os.path.exists(vid):
        for f in os.listdir("shorts"):
            if "source_full" in f:
                vid = os.path.join("shorts", f)
                break
    extract_key_frames(vid)
