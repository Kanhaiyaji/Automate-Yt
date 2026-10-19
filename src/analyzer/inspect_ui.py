#!/usr/bin/env python3
"""inspect_ui.py - Checks HUD coordinates for Alive / Finish counter and Kill Feed."""
import cv2, os

img = cv2.imread("shorts/frames/frame_0040.jpg")
h, w, _ = img.shape
print(f"Image shape: {w}x{h}")

# The top-left HUD (Alive / Finish) is roughly x: 0 to 0.25*w, y: 0 to 0.25*h
# Let's save a crop of top-left and middle
hud_crop = img[0:int(0.25*h), 0:int(0.35*w)]
cv2.imwrite("shorts/hud_sample.jpg", hud_crop)

# Middle kill announcement (usually center or top-center)
center_crop = img[int(0.2*h):int(0.6*h), int(0.2*w):int(0.8*w)]
cv2.imwrite("shorts/center_sample.jpg", center_crop)
print("Saved hud_sample.jpg and center_sample.jpg")
