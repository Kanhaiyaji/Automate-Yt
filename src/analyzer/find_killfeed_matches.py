#!/usr/bin/env python3
"""find_killfeed_matches.py - Detects JhajiOG killfeed banners and counts consecutive kills (2-3+)."""
import cv2, os, glob, numpy as np

TEMPLATE_PATH = r"C:/Users/JHAJI/.gemini/antigravity/brain/dfd3a2b0-7189-4660-8846-f67a475ee071/.user_uploaded/media_1792394931337_1c3b7421.png"
tmpl = cv2.imread(TEMPLATE_PATH)
th, tw, _ = tmpl.shape
print(f"User Template size: {tw}x{th}")

# Extract just the 'OCN | JhajiOG*' name part for cleaner template matching
# In 282x37, 'OCN | JhajiOG*' is roughly x: 10 to 115
name_tmpl = tmpl[:, 10:115]
cv2.imwrite("shorts/name_tmpl.jpg", name_tmpl)

# The video frames in shorts/frames/ are 640x288
# If the original video was 1280x576 or 1920x1080, the template was cropped from original resolution
# Let's extract full-resolution frames at 1 fps into a high-res cache or scan video directly with OpenCV VideoCapture
video_path = "shorts/source_full_sd3.mp4.webm"
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
vw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Source video: {vw}x{vh} @ {fps:.1f} fps, {total_frames} frames ({total_frames/fps:.1f}s)")

# We search in the killfeed region: left side (x: 0 to 0.4*vw, y: 0.15*vh to 0.45*vh)
# Cyan text color range in HSV:
# Hue for cyan/teal: ~80 to ~100 in OpenCV HSV (where 0-180 is hue)
lower_cyan = np.array([75, 80, 80])
upper_cyan = np.array([105, 255, 255])

kill_seconds = []
sec = 0

# Check 1 frame every 0.5s
step = int(fps * 0.5)
for frame_idx in range(0, total_frames, step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret: break
    
    t_sec = frame_idx / fps
    # Killfeed region
    # Look at y from 100 to 250, x from 20 to 450
    kf_crop = frame[int(0.18*vh):int(0.42*vh), int(0.02*vw):int(0.38*vw)]
    
    # Check for cyan pixels (the distinctive color of 'OCN | JhajiOG*')
    hsv = cv2.cvtColor(kf_crop, cv2.COLOR_BGR2HSV)
    cyan_mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
    cyan_count = cv2.countNonZero(cyan_mask)
    
    # If cyan pixels indicate killfeed entry
    if cyan_count > 150: # Sufficient cyan text pixels for name
        kill_seconds.append((round(t_sec, 1), cyan_count))

cap.release()
print(f"Detected {len(kill_seconds)} timestamps with JhajiOG killfeed activity.")

# Cluster into kill events (group timestamps within 1.5s as one kill banner)
distinct_kills = []
curr_cluster = []
for t, c in kill_seconds:
    if not curr_cluster:
        curr_cluster.append((t, c))
    else:
        if t - curr_cluster[-1][0] <= 2.0:
            curr_cluster.append((t, c))
        else:
            # Pick timestamp with max cyan
            best_t = max(curr_cluster, key=lambda x: x[1])[0]
            distinct_kills.append(best_t)
            curr_cluster = [(t, c)]
if curr_cluster:
    best_t = max(curr_cluster, key=lambda x: x[1])[0]
    distinct_kills.append(best_t)

print(f"\nDistinct Killfeed Events ({len(distinct_kills)}):")
for i, t in enumerate(distinct_kills):
    m, s = divmod(int(t), 60)
    print(f"  Kill {i+1}: {m:02d}:{s:02d} ({t:.1f}s)")

# Find clusters where count is 2-3 (within 10-15s window)
multi_kill_clips = []
window = 16.0 # seconds

i = 0
while i < len(distinct_kills):
    t_start = distinct_kills[i]
    cluster = [t_start]
    j = i + 1
    while j < len(distinct_kills) and (distinct_kills[j] - t_start) <= window:
        cluster.append(distinct_kills[j])
        j += 1
    
    count = len(cluster)
    if count >= 2:
        clip_start = max(0.0, cluster[0] - 3.5) # 3.5s lead-in to see enemy & aim
        clip_end = cluster[-1] + 3.0           # 3.0s follow-through to celebrate kill
        multi_kill_clips.append({
            "count": count,
            "kills": cluster,
            "clip_start": clip_start,
            "clip_end": clip_end,
            "duration": clip_end - clip_start
        })
        i = j
    else:
        i += 1

print(f"\nMulti-Kill Sequences with count 2-3+ ({len(multi_kill_clips)}):")
for idx, clip in enumerate(multi_kill_clips):
    st_m, st_s = divmod(int(clip['clip_start']), 60)
    en_m, en_s = divmod(int(clip['clip_end']), 60)
    print(f"  --> CLIP {idx+1}: Count = {clip['count']} KILLS!")
    print(f"      Range: {st_m:02d}:{st_s:02d} -> {en_m:02d}:{en_s:02d} ({clip['duration']:.1f}s)")
    print(f"      Kill timestamps: {[f'{int(k//60):02d}:{int(k%60):02d}' for k in clip['kills']]}")
