#!/usr/bin/env python3
"""fast_killfeed_detect.py - Scans the 267 extracted frames in shorts/frames/ for Jhaji's killfeed knocks/kills."""
import cv2, os, glob, numpy as np

frames = sorted(glob.glob("shorts/frames/frame_*.jpg"))
print(f"Loaded {len(frames)} frames from shorts/frames/")

# In HSV: Cyan / Teal color for OCN | JhajiOG*
# Hue: 75 to 105, Sat: 80 to 255, Val: 80 to 255
lower_cyan = np.array([75, 80, 80])
upper_cyan = np.array([105, 255, 255])

kill_hits = []
for i, f in enumerate(frames):
    sec = i + 1
    img = cv2.imread(f)
    h, w, _ = img.shape
    
    # Killfeed is on the left side
    kf_crop = img[int(0.20*h):int(0.52*h), int(0.02*w):int(0.40*w)]
    hsv = cv2.cvtColor(kf_crop, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
    cyan_count = cv2.countNonZero(mask)
    
    if cyan_count > 60: # Threshold for cyan text pixels in 640x288
        kill_hits.append((sec, cyan_count))

print(f"Detected cyan killfeed on {len(kill_hits)} seconds.")

# Group consecutive seconds into discrete kill/knock notifications
distinct_events = []
current = []
for sec, cnt in kill_hits:
    if not current:
        current.append((sec, cnt))
    else:
        if sec - current[-1][0] <= 2:
            current.append((sec, cnt))
        else:
            best_sec = max(current, key=lambda x: x[1])[0]
            distinct_events.append(best_sec)
            current = [(sec, cnt)]
if current:
    best_sec = max(current, key=lambda x: x[1])[0]
    distinct_events.append(best_sec)

print(f"\nDistinct Killfeed Events ({len(distinct_events)}):")
for idx, s in enumerate(distinct_events):
    m, sec_rem = divmod(s, 60)
    print(f"  Event {idx+1}: {m:02d}:{sec_rem:02d} ({s}s)")

# Find clusters where count is 2-3 (within a 15-20 second engagement window)
multi_kill_clusters = []
i = 0
while i < len(distinct_events):
    cluster = [distinct_events[i]]
    j = i + 1
    while j < len(distinct_events) and (distinct_events[j] - distinct_events[i]) <= 18:
        cluster.append(distinct_events[j])
        j += 1
    
    if len(cluster) >= 2:
        st_sec = max(0, cluster[0] - 4)  # 4s before the first knock/kill (to see aim/approach)
        en_sec = min(len(frames), cluster[-1] + 3) # 3s after last kill
        multi_kill_clusters.append({
            "count": len(cluster),
            "kills": cluster,
            "start": st_sec,
            "end": en_sec,
            "duration": en_sec - st_sec
        })
        i = j
    else:
        i += 1

print(f"\n=======================================================")
print(f"FOUND {len(multi_kill_clusters)} MULTI-KILL CLUSTERS (Count = 2-3+):")
for idx, cl in enumerate(multi_kill_clusters):
    st_m, st_s = divmod(cl['start'], 60)
    en_m, en_s = divmod(cl['end'], 60)
    k_strs = [f"{int(k//60):02d}:{int(k%60):02d}" for k in cl['kills']]
    print(f"\n[CLIP OPTION {idx+1}] => {cl['count']} KILLS IN KILLFEED!")
    print(f"  Time Window : {st_m:02d}:{st_s:02d} - {en_m:02d}:{en_s:02d} ({cl['duration']} seconds)")
    print(f"  Exact Kills : {', '.join(k_strs)}")
print("=======================================================\n")
