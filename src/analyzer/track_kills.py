#!/usr/bin/env python3
"""track_kills.py - Track Finish count and kill notifications across frames."""
import cv2, os, glob

# In 640x288:
# The 'Finish' box is at y: 6 to 34, x: 62 to 115
frames = sorted(glob.glob("shorts/frames/frame_*.jpg"))
print(f"Total frames to check: {len(frames)}")

os.makedirs("shorts/kill_crops", exist_ok=True)

# Let's save a crop every 10 seconds to inspect progression
samples = []
for i in range(0, len(frames), 5):
    f = frames[i]
    sec = i + 1
    m, s = divmod(sec, 60)
    img = cv2.imread(f)
    crop = img[6:34, 62:115]
    cv2.imwrite(f"shorts/kill_crops/finish_{sec:03d}s.jpg", crop)
    samples.append((sec, f"{m:02d}:{s:02d}"))

print(f"Saved {len(samples)} sample crops into shorts/kill_crops/")
