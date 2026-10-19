#!/usr/bin/env python3
"""map_kills.py - Scans frames for JhajiOG in the killfeed and red kill announcements."""
import cv2, os, glob, numpy as np

frames = sorted(glob.glob("shorts/frames/frame_*.jpg"))
print(f"Scanning {len(frames)} frames for JhajiOG kills and hitmarkers...")

kill_events = []
os.makedirs("shorts/kill_events", exist_ok=True)

for i, f in enumerate(frames):
    sec = i + 1
    img = cv2.imread(f)
    if img is None: continue
    
    # 1. Killfeed region (y: 60 to 140, x: 20 to 180)
    kf_crop = img[60:140, 20:200]
    
    # 2. Center combat / kill banner (y: 100 to 200, x: 200 to 440)
    center_crop = img[100:200, 200:440]
    
    # Check for red color (hitmarker or kill text in HSV)
    hsv = cv2.cvtColor(center_crop, cv2.COLOR_BGR2HSV)
    # Red mask in HSV
    lower_red1 = np.array([0, 120, 120])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 120])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_pixels = cv2.countNonZero(mask1 | mask2)
    
    # Yellow / Gold hit text (e.g. headshot or finish notification)
    lower_yellow = np.array([20, 120, 120])
    upper_yellow = np.array([35, 255, 255])
    yellow_pixels = cv2.countNonZero(cv2.inRange(hsv, lower_yellow, upper_yellow))
    
    if red_pixels > 80 or yellow_pixels > 120:
        m, s = divmod(sec, 60)
        kill_events.append((sec, f"{m:02d}:{s:02d}", red_pixels, yellow_pixels))
        cv2.imwrite(f"shorts/kill_events/event_{sec:03d}s.jpg", img)

print(f"Detected {len(kill_events)} combat hit/kill events!")
# Group consecutive seconds
grouped = []
curr = []
for ev in kill_events:
    sec = ev[0]
    if not curr:
        curr.append(ev)
    else:
        if sec - curr[-1][0] <= 3:
            curr.append(ev)
        else:
            grouped.append(curr)
            curr = [ev]
if curr:
    grouped.append(curr)

print(f"\nDistinct combat/kill sequences ({len(grouped)}):")
for idx, grp in enumerate(grouped):
    st_sec = grp[0][0]
    en_sec = grp[-1][0]
    m1, s1 = divmod(st_sec, 60)
    m2, s2 = divmod(en_sec, 60)
    dur = en_sec - st_sec + 1
    print(f"  Engagement {idx+1}: {m1:02d}:{s1:02d} -> {m2:02d}:{s2:02d} ({dur}s) [Frames: {len(grp)}]")
