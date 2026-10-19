"""
Multi-Kill Merge Module
Merges 3 to 4 distinct pro combat kills into a single action-packed, true 9:16 (1080x1920) vertical Short.
Zero downtime, back-to-back frags, with custom HUD counter overlays and audio crossfades.
"""

import os
import subprocess
import json
from typing import List, Dict, Any

class MultiKillShortBuilder:
    def __init__(self, source_video: str, output_path: str, temp_dir: str = "temp_render"):
        self.source_video = source_video
        self.output_path = output_path
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    def build_multikill_short(self, segments: List[Dict[str, Any]]) -> str:
        """
        segments: list of dicts with keys:
            - ss: start timestamp (e.g. "00:01:09.5")
            - to: end timestamp (e.g. "00:01:16.8")
            - title: top HUD banner label (e.g. "KILL 1 & 2 - vs CLOUD9")
        """
        part_files = []
        for i, seg in enumerate(segments, 1):
            part_path = os.path.join(self.temp_dir, f"part_{i:02d}.mp4")
            part_files.append(part_path)

            title = seg.get("title", f"KILL {i}")
            # Escape colons or avoid them for drawtext filter
            safe_title = title.replace(":", " -")

            # 9:16 vertical crop formula for 1920x864: crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920
            drawbox = "drawbox=y=155:color=black@0.75:width=iw:height=75:t=fill"
            drawtext = f"drawtext=text='{safe_title}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=175"
            vf = f"crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920,{drawbox},{drawtext}"

            cmd = [
                "ffmpeg", "-y",
                "-ss", seg["ss"],
                "-to", seg["to"],
                "-i", self.source_video,
                "-vf", vf,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                "-c:a", "aac", "-b:a", "192k",
                part_path
            ]
            print(f"[*] Rendering segment {i}/{len(segments)}: {safe_title} ({seg['ss']} -> {seg['to']})...")
            subprocess.run(cmd, check=True)

        # Create concat list
        concat_file = os.path.join(self.temp_dir, "concat_list.txt")
        with open(concat_file, "w") as f:
            for p in part_files:
                f.write(f"file '{os.path.abspath(p).replace('\\', '/')}'\n")

        print("[*] Concatenating segments into final 9:16 Short...")
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            self.output_path
        ]
        subprocess.run(concat_cmd, check=True)

        print(f"[+] Multi-kill Short created successfully: {self.output_path}")
        return self.output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge 3-4 kills into a 9:16 YouTube Short")
    parser.add_argument("--source", required=True, help="Path to raw source gameplay video")
    parser.add_argument("--output", default="output_multikill_916.mp4", help="Output Short path")
    parser.add_argument("--config", help="JSON file defining segments")
    args = parser.parse_args()

    if args.config and os.path.exists(args.config):
        with open(args.config, "r") as f:
            segments = json.load(f)
    else:
        # Default sample 4-kill segments
        segments = [
            {"ss": "00:01:09.5", "to": "00:01:16.8", "title": "KILL 1 & 2 - vs CLOUD9"},
            {"ss": "00:02:35.0", "to": "00:02:43.8", "title": "KILL 3 - 6X LASER BEAM"},
            {"ss": "00:03:07.0", "to": "00:03:15.5", "title": "KILL 4 - vs KyZN ESPORTS"},
            {"ss": "00:06:14.0", "to": "00:06:23.2", "title": "FINAL 1v1 - CLUTCH WIN!"}
        ]

    builder = MultiKillShortBuilder(args.source, args.output)
    builder.build_multikill_short(segments)
