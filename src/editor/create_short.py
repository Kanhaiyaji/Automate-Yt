#!/usr/bin/env python3
"""create_short.py - High-Quality 9:16 YouTube Shorts generator for Jhaji OG (@jhajiog).

Extracts active combat/fight moments against opponents from a YouTube video or local gameplay file,
cuts out all filler/running/looting pauses between fights, crops/formats into crisp 9:16 vertical
Short (CRF 17, Split-Blur or Center-Crop), adds high-contrast hook header, and generates viral metadata.

Usage:
    # Single continuous fight:
    python tools/create_short.py --url "https://www.youtube.com/watch?v=Sd3RSY0nH50" \\
                                 --start 00:00:30 --end 00:01:02 \\
                                 --title "Clean 1v3 Clutch in ScarFall 2.0" \\
                                 --header "1v3 CLUTCH GOD 🔥" \\
                                 --out shorts/clutch_short_1.mp4

    # Multi-fight combat cuts (cuts out intermediate dead time):
    python tools/create_short.py --url "https://www.youtube.com/watch?v=Sd3RSY0nH50" \\
                                 --segments "00:00:32-00:00:44, 00:01:15-00:01:28" \\
                                 --title "Back-to-Back Squad Wipes in ScarFall 2.0" \\
                                 --header "BACK TO BACK WIPES 🔥" \\
                                 --out shorts/clutch_short_2.mp4
"""
import os, sys, re, json, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, ".."))

def check_dependencies():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except Exception:
        print("Error: FFmpeg is not installed or not in PATH.")
        sys.exit(1)

def to_secs(s):
    s = str(s).strip()
    parts = s.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(s)

def parse_segments(segments_str, start_str=None, end_str=None):
    """Parses segment string or start/end into list of (start_sec, end_sec) tuples."""
    segs = []
    if segments_str:
        raw_items = segments_str.split(",")
        for item in raw_items:
            item = item.strip()
            if not item:
                continue
            if "-" in item:
                st, en = item.split("-", 1)
                segs.append((to_secs(st), to_secs(en)))
            else:
                st = to_secs(item)
                segs.append((st, st + 15.0))
    elif start_str and end_str:
        segs.append((to_secs(start_str), to_secs(end_str)))
    return segs

def download_video_sections(url, segments, temp_raw):
    print(f"\n[1/3] Downloading highest quality fight sections from YouTube...")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--force-keyframes-at-cuts",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
        "-o", temp_raw,
        "--no-playlist"
    ]
    for st, en in segments:
        cmd.extend(["--download-sections", f"*{st}-{en}"])
    cmd.append(url)

    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("Section download fallback: downloading full clip for precise trimming...")
        cmd_fallback = [
            sys.executable, "-m", "yt_dlp",
            "-f", "bestvideo[height<=1080]+bestaudio/best",
            "-o", temp_raw,
            "--no-playlist",
            url
        ]
        res2 = subprocess.run(cmd_fallback)
        if res2.returncode != 0:
            print("Failed to download video with yt-dlp.")
            sys.exit(1)

def render_vertical_short(input_file, segments, output_file, header_text=None, style="split_blur"):
    print(f"\n[2/3] Rendering 9:16 vertical Short (Fight-Only Pacing, {len(segments)} segment(s), CRF 17)...")
    
    # Filter graph construction
    filter_parts = []
    v_streams = []
    a_streams = []

    # If only 1 segment and already section-downloaded or simple range
    if len(segments) == 1:
        st, en = segments[0]
        duration = max(3.0, en - st)
        ss_opts = ["-ss", str(st), "-t", str(duration)]
        v_in = "[0:v]"
        a_in = "0:a?"
    else:
        # Multi-segment trim & concat to cut out all intermediate dead air
        max_end = max(en for _, en in segments)
        ss_opts = ["-to", str(max_end + 1.0)]
        for i, (st, en) in enumerate(segments):
            dur = max(1.0, en - st)
            filter_parts.append(f"[0:v]trim=start={st}:end={en},setpts=PTS-STARTPTS[v{i}]")
            filter_parts.append(f"[0:a]atrim=start={st}:end={en},asetpts=PTS-STARTPTS[a{i}]")
            v_streams.append(f"[v{i}]")
            a_streams.append(f"[a{i}]")
        
        concat_inputs = "".join(f"{v_streams[i]}{a_streams[i]}" for i in range(len(segments)))
        filter_parts.append(f"{concat_inputs}concat=n={len(segments)}:v=1:a=1[vraw][araw]")
        v_in = "[vraw]"
        a_in = "[araw]"

    # 9:16 vertical formatting
    if style == "split_blur":
        filter_parts.append(f"{v_in}split=2[v_bg_in][v_fg_in]")
        filter_parts.append(
            "[v_bg_in]scale=270:480,boxblur=8:2,scale=1080:1920:flags=bilinear[bg]; "
            "[v_fg_in]scale=1080:-1[fg]; "
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[base]"
        )
        last_v = "[base]"
    else:
        filter_parts.append(f"{v_in}crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920[base]")
        last_v = "[base]"

    # Header hook banner
    if header_text:
        clean_text = re.sub(r'[^\w\s\-\|\.\,\!\?\/]', '', header_text).strip()
        font_opt = "fontsize=44:fontcolor=yellow:box=1:boxcolor=black@0.75:boxborderw=18:x=(w-text_w)/2:y=240"
        filter_parts.append(f"{last_v}drawtext=text='{clean_text}':{font_opt}[vfinal]")
        final_v = "[vfinal]"
    else:
        final_v = last_v

    full_filter = "; ".join(filter_parts)

    cmd = ["ffmpeg", "-y"]
    if ss_opts:
        cmd.extend(ss_opts)
    cmd.extend(["-i", input_file])
    cmd.extend([
        "-filter_complex", full_filter,
        "-map", final_v,
        "-map", a_in,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "17",               # Visually lossless high quality
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-movflags", "+faststart",
        output_file
    ])

    res = subprocess.run(cmd)
    if res.returncode != 0:
        print("FFmpeg rendering failed.")
        sys.exit(1)
    print(f"Rendered successfully: {output_file}")

def generate_metadata(title, header_text, output_mp4):
    clean_title = f"{title.strip()} #shorts #scarfall2 #gaming"
    meta = {
        "title": clean_title[:100],
        "video_path": os.path.abspath(output_mp4),
        "header": header_text,
        "description": (
            f"{title}\n\n"
            "🔥 Subscribe to Jhaji OG for more intense ScarFall 2.0 & BGMI esports frags, clutches & funny moments!\n"
            "Follow on Kick: https://kick.com/jhajiog\n"
            "Join Discord: https://discord.gg/uVebERX\n"
            "ODDSOCEAN Esports Instagram: https://instagram.com/oddsocean.in\n\n"
            "#shorts #scarfall2 #gaming #clutch #esportsindia #battleroyale #bgmi #oddsocean #jhajiog"
        ),
        "tags": [
            "scarfall 2.0", "scarfall 2.0 clutch", "1v3 clutch", "1v4 clutch", 
            "jhaji og", "oddsocean", "scarfall gameplay", "esports india",
            "mobile battle royale", "bgmi clutch", "shorts", "gaming shorts"
        ],
        "visibility": "unlisted"
    }
    json_path = os.path.splitext(output_mp4)[0] + "_metadata.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"[3/3] Generated staging metadata: {json_path}")
    return meta

def main():
    check_dependencies()
    parser = argparse.ArgumentParser(description="Create 9:16 Shorts for Jhaji OG with Fight-Only Pacing")
    parser.add_argument("--url", required=True, help="YouTube video URL or path to local MP4")
    parser.add_argument("--start", default="00:00:30", help="Start timestamp if single segment")
    parser.add_argument("--end", default="00:01:00", help="End timestamp if single segment")
    parser.add_argument("--segments", default=None, help="Comma-separated fight timestamps: '00:30-00:42, 01:10-01:25'")
    parser.add_argument("--title", default="Insane Fight Clutch in ScarFall 2.0", help="Video Title")
    parser.add_argument("--header", default="CLUTCH MOMENTS 🔥", help="Banner text on short")
    parser.add_argument("--style", choices=["split_blur", "crop"], default="split_blur", help="Layout style")
    parser.add_argument("--out", default="shorts/jhajiog_fight_short.mp4", help="Output MP4 path")

    args = parser.parse_args()
    segments = parse_segments(args.segments, args.start, args.end)

    if not segments:
        print("Error: No valid fight segments provided.")
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    temp_raw = os.path.join(os.path.dirname(os.path.abspath(args.out)), "temp_raw_source.mp4")

    if os.path.exists(args.url):
        source_file = args.url
    else:
        download_video_sections(args.url, segments, temp_raw)
        source_file = temp_raw

    render_vertical_short(source_file, segments, args.out, args.header, args.style)

    if os.path.exists(temp_raw):
        try: os.remove(temp_raw)
        except Exception: pass

    meta = generate_metadata(args.title, args.header, args.out)
    print("\n" + "="*60)
    print("READY TO STAGE IN YOUTUBE STUDIO:")
    print(f"  Title      : {meta['title']}")
    print(f"  File       : {meta['video_path']}")
    print(f"  Segments   : {segments}")
    print(f"  Visibility : {meta['visibility']}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
