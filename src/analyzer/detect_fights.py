#!/usr/bin/env python3
"""detect_fights.py - Detect high-intensity combat / fight moments using audio RMS volume spikes."""
import subprocess, re, sys, os

def get_volume_profile(video_path):
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
        "-f", "null", "-"
    ]
    # Or simpler: run ebur128 or silencedetect
    cmd2 = [
        "ffmpeg", "-i", video_path,
        "-filter_complex", "ebur128=metadata=1,ametadata=print:key=lavfi.r128.M:file=volume_log.txt",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "volume_log.txt"

def parse_volume_log(log_path):
    # Extracts timestamps where loudness M (momentary loudness in LUFS) is high (e.g. > -18 LUFS)
    fights = []
    current_fight = None
    if not os.path.exists(log_path):
        return []
    
    with open(log_path, "r", encoding="utf-8") as f:
        pts = None
        for line in f:
            if "pts_time:" in line:
                m = re.search(r"pts_time:([\d\.]+)", line)
                if m:
                    pts = float(m.group(1))
            elif "lavfi.r128.M=" in line:
                m = re.search(r"lavfi\.r128\.M=(-?[\d\.]+)", line)
                if m and pts is not None:
                    loudness = float(m.group(1))
                    # Loudness threshold for gunshots/fighting: usually > -20.0 LUFS
                    is_active = loudness > -19.0
                    if is_active:
                        if current_fight is None:
                            current_fight = [pts, pts]
                        else:
                            current_fight[1] = pts
                    else:
                        if current_fight is not None:
                            # If gap is small, keep merging; if big, close fight
                            if pts - current_fight[1] > 2.5:
                                dur = current_fight[1] - current_fight[0]
                                if dur >= 4.0:
                                    fights.append((current_fight[0], current_fight[1]))
                                current_fight = None
    if current_fight and (current_fight[1] - current_fight[0]) >= 4.0:
        fights.append((current_fight[0], current_fight[1]))
    return fights

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "shorts/source_full_sd3.mp4.webm"
    log = get_volume_profile(vid)
    fights = parse_volume_log(log)
    print(f"\nDetected {len(fights)} intense fight moments in {vid}:")
    for i, (st, en) in enumerate(fights):
        m1, s1 = divmod(int(st), 60)
        m2, s2 = divmod(int(en), 60)
        print(f"  Fight {i+1}: {m1:02d}:{s1:02d} - {m2:02d}:{s2:02d} ({en-st:.1f}s)")
    if os.path.exists("volume_log.txt"):
        try: os.remove("volume_log.txt")
        except: pass
