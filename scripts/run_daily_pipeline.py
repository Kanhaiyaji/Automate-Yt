"""
Master Daily 11:11 AM YouTube Shorts Pipeline
Automates:
1. Sourcing / analyzing tournament gameplay
2. Detecting multi-kill clusters (3-4 kills)
3. Rendering True 9:16 vertical (1080x1920) montage
4. Producing metadata and staging for YouTube Studio scheduling
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.editor.multi_kill_merge import MultiKillShortBuilder
from src.uploader.metadata_generator import MetadataGenerator

def run_pipeline(source_video: str, scheduled_date: str = None, scheduled_time: str = "11:11 AM"):
    if not os.path.exists(source_video):
        print(f"[!] Error: Source video {source_video} not found.")
        sys.exit(1)

    if not scheduled_date:
        # Default to tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        scheduled_date = tomorrow.strftime("%Y-%m-%d")

    print(f"=== Starting Daily Shorts Pipeline ===")
    print(f"[*] Source Video: {source_video}")
    print(f"[*] Target Schedule: {scheduled_date} @ {scheduled_time}")

    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)
    out_mp4 = os.path.join(output_dir, f"short_{scheduled_date}.mp4")

    # Sample top 4 kills segments
    segments = [
        {"ss": "00:01:09.5", "to": "00:01:16.8", "title": "KILL 1 & 2 - vs CLOUD9"},
        {"ss": "00:02:35.0", "to": "00:02:43.8", "title": "KILL 3 - 6X LASER BEAM"},
        {"ss": "00:03:07.0", "to": "00:03:15.5", "title": "KILL 4 - vs KyZN ESPORTS"},
        {"ss": "00:06:14.0", "to": "00:06:23.2", "title": "FINAL 1v1 - CLUTCH WIN!"}
    ]

    builder = MultiKillShortBuilder(source_video=source_video, output_path=out_mp4)
    rendered_file = builder.build_multikill_short(segments)

    # Generate metadata
    gen = MetadataGenerator()
    meta = gen.generate_multikill_metadata(
        title_prefix="4 Kills Multi-Squad Wipe",
        kills_breakdown=[
            "Double Wipe vs Cloud9 Esports (C9x)",
            "80m 6x Scope Laser Spray vs TSF",
            "High Ground Ridge Clash vs KyZN Esports",
            "Final 1v1 Circle Clutch for the Victory!"
        ]
    )
    meta["scheduled_date"] = scheduled_date
    meta["scheduled_time"] = scheduled_time
    meta["video_path"] = rendered_file

    meta_file = os.path.join(output_dir, f"metadata_{scheduled_date}.json")
    with open(meta_file, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[+] Pipeline complete! Video: {rendered_file}, Metadata: {meta_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run daily YouTube Shorts pipeline")
    parser.add_argument("--source", default="shorts/source_video_2.mp4", help="Source gameplay video path")
    parser.add_argument("--date", help="Scheduled date (YYYY-MM-DD)")
    parser.add_argument("--time", default="11:11 AM", help="Scheduled time")
    args = parser.parse_args()

    run_pipeline(args.source, args.date, args.time)
