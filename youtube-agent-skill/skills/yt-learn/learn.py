#!/usr/bin/env python3
"""learn.py - Interactive learning coach and reference guide for YouTube Agent skills.

Usage:
    python learn.py --list                         # List all 21 hook formulas
    python learn.py --formula <id-or-name>         # Deep-dive into a specific formula
    python learn.py --packaging                    # Master the title & thumbnail packaging doctrine
    python learn.py --retention                    # Learn the 3 retention problems & remedies
    python learn.py --editing                      # Learn the transcript EDL cutting principles
    python learn.py --chapters                     # Learn YouTube chapter rendering rules
    python learn.py --viral                        # Learn the outlier virality median multiplier
    python learn.py --topic "Your Topic"           # Generate and score 5 formula hooks for a topic
    python learn.py --quiz                         # Test your YouTube engineering knowledge
    python learn.py --all                          # Complete reference overview
"""
import json, os, re, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS_JSON = os.path.join(HERE, "..", "yt-script", "hooks.json")
if not os.path.exists(HOOKS_JSON):
    HOOKS_JSON = os.path.join(HERE, "hooks.json")

def load_formulas():
    if os.path.exists(HOOKS_JSON):
        with open(HOOKS_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {"rules": [], "hooks": []}

DATA = load_formulas()
FORMULAS = DATA.get("hooks", [])
CORE_RULES = DATA.get("rules", [])

def print_header(title):
    print(f"\n{'=' * 72}\n  {title}\n{'=' * 72}")

def show_overview():
    print_header("YouTube Agent Skills & Production Doctrine")
    print("""
The YouTube Agent suite is built on eleven specialized skills and six zero-dependency
deterministic Python tools. Together they enforce retention engineering, packaging
laws, and edit precision.

THE 11 AGENT SKILLS:
  1. /yt-script    : First 15s hook options (scored off 21 formulas) + spoken retention beats.
  2. /yt-package   : Title and thumbnail linted as ONE unit for truncation, duplication, and vagueness.
  3. /yt-edit      : Timestamped transcript -> Edit Decision List (dead air, filler, retakes).
  4. /yt-comment   : Triage comments into Questions, Corrections, Praise, Bait + authentic replies.
  5. /yt-plan      : Capacity-based weekly calendar: 1 anchor, 1 cheap video, 3 Shorts.
  6. /yt-viral     : Niche outlier analysis ranked by multiple over channel's own median.
  7. /yt-retention : Studio retention CSV analysis: Hook Leak (<25%), Cliffs (>0.8%), and Slide.
  8. /yt-shorts    : Find self-contained 20-55s clips with brand new standalone hooks.
  9. /yt-seo       : First 2-line above-the-fold descriptions, 15 disambiguation tags, 3 queries.
  10. /yt-chapters : Chapters from transcript validated against YouTube's rendering criteria.
  11. /yt-audit    : Whole channel audit ending in ONE high-leverage fix rather than 20 complaints.

THE NEW 12th SKILL:
  12. /yt-learn    : Interactive learning coach, formula browser, packaging/retention drills.
""")

def list_formulas():
    print_header("The 21 YouTube Hook Formulas")
    print("A hook does 3 things: confirm title click, open an unresolved question, prove payoff.\n")
    for i, f in enumerate(FORMULAS, 1):
        print(f"  {i:2d}. [{f['id']}] {f['name']}")
        print(f"      Shape : {f['shape']}")
        print(f"      Example: \"{f['example']}\"\n")

def inspect_formula(query):
    query_norm = query.lower().strip()
    match = None
    for f in FORMULAS:
        if query_norm in (f["id"].lower(), f["name"].lower()) or query_norm in f["id"] or query_norm in f["name"].lower():
            match = f
            break
    if not match:
        print(f"Formula '{query}' not found. Run --list to see all available formulas.")
        return

    print_header(f"Formula: {match['name']} ({match['id']})")
    print(f"  Shape       : {match['shape']}")
    print(f"  Worked Hook : \"{match['example']}\"")
    print(f"  Fails When  : {match['fails_when']}")
    print("  Match Patterns:")
    for p in match["match"]:
        print(f"    - regex: {p}")
    print("\n  Tip: The first sentence must confirm the title click. Never introduce yourself first.")

def show_packaging():
    print_header("Packaging Doctrine: Title + Thumbnail as ONE Unit")
    print("""
1. THE 60 / 40 TRUNCATION RULE:
   - Desktop Search truncates titles around 60 characters. A cut loses the tail.
   - Mobile Home Feed truncates titles around 40 characters. A cut can lose the subject!
   - Always front-load the key subject and promise within the first 40 characters.

2. ANTI-DUPLICATION LAW:
   - The thumbnail and title share 100% of the click surface.
   - If the thumbnail repeats the title's words (e.g. Title: "Best AI Video Editors",
     Thumb: "BEST AI EDITORS"), you waste half your real estate.
   - Thumbnail should show or state what the title CANNOT (e.g. emotion, contrast, proof).

3. THE 3-WORD THUMBNAIL CEILING:
   - At mobile feed thumbnail size, a 4th word becomes an unreadable grey smear.
   - Keep thumbnail text to 1 to 3 bold, high-contrast words.

4. CONCRETE VS VAGUE:
   - Concrete figures, dates, and names ("400 to 200,000", "7 months", "$1,400")
     beat empty hype words ("insane", "massive", "ultimate", "secret").
   - Max two all-caps words in titles before it reads as spam.
""")

def show_retention():
    print_header("Retention Engineering: Diagnosing the 3 Core Leaks")
    print("""
The retention curve is the only honest feedback YouTube gives. Diagnose in this order:

1. HOOK LEAK (0:00 - 0:30):
   - Measure: Percentage of viewers lost in the first 30 seconds.
   - Benchmark: Under 25% lost is healthy. Over 40% is severe leak.
   - Cause: Title promise mismatch, channel intro, fluff, asking to subscribe.
   - Fix: Fix the first 15 seconds of the SCRIPT. Never open with who you are.

2. CLIFFS (Instant drops > 0.8%):
   - Measure: Single moments where the line drops sharply.
   - Cause: Abrupt topic change without signposting, sudden sponsor read, long silent setup.
   - Fix: Check the transcript at that second. Bridge the transition with a clear payoff signpost.

3. SLIDE (The steady middle bleed):
   - Measure: Gentle downward angle across minutes 1:00 to the end.
   - Cause: Pacing dragged out, repetitive points, lack of pattern interrupts.
   - Fix: Cut the middle! Trimming 20% of dead space fixes slide. Do not rewrite.
""")

def show_editing():
    print_header("Edit Decision List (EDL) Cutting Principles")
    print("""
1. TRIM DEAD AIR FROM THE MIDDLE:
   - Gaps longer than 0.45s (or custom floor) should be trimmed from the MIDDLE.
   - Leaving floor / 2 on both sides preserves natural breathing.
   - Cutting flush against speech makes the speaker sound gasping and robotic.

2. CATCH SENTENCE RESTARTS (RETAKES):
   - A restart happens when a creator stumbles and begins the sentence again.
   - Retakes often have an "um" or silence between them.
   - Compare new speech cues against the last actual speech cue (skipping filler).

3. PURGE FILLER-ONLY CUES:
   - Drop cues that are exclusively filler ("um", "uh", "so yeah", "basically").
""")

def show_chapters():
    print_header("YouTube Chapters: The Mandatory Rendering Rules")
    print("""
If a description block breaks ANY of these 3 rules, YouTube silently refuses to render chapters:
  Rule 1: The very first timestamp MUST be 00:00 (or 0:00).
  Rule 2: There MUST be at least 3 chapters listed.
  Rule 3: Every chapter MUST be at least 10 seconds long.

RETITLING ADVICE:
  The algorithm flags vocabulary shifts and pauses to identify chapter cuts.
  The detected keywords are draft topic tags (e.g. "Script Hook Formulas").
  Always rewrite each chapter title as an outcome promise in your voice (3-5 words).
""")

def show_viral():
    print_header("Outlier Virality: The Median Multiplier Method")
    print("""
1. RAW VIEWS LIE:
   - 500,000 views on a 5M subscriber channel is an underperformance.
   - 500,000 views on a 20k subscriber channel whose median is 10k is a 50x outlier!
   - Study the OUTLIERS relative to each channel's own median.

2. DATA INTEGRITY:
   - Minimum 4 recent videos per channel are required to establish a reliable median.
   - Use public listings (e.g. via `yt-dlp --flat-playlist -J <channel_url>`).
   - Filter for videos with multiplier >= 2.0x.

3. FORMULA EXTRACTION:
   - Map the outlier titles against the 21 hook formulas.
   - Identify which structural pattern (The Statistic, Someone Else's Result, etc.)
     caused the click spike.
""")

def run_quiz():
    print_header("YouTube Engineering Mastery Quiz")
    questions = [
        {
            "q": "What is the maximum healthy percentage drop in the first 30 seconds (Hook Leak)?",
            "choices": ["A) 10%", "B) 25%", "C) 50%", "D) 65%"],
            "ans": "B",
            "explain": "Under 25% lost in the first 30 seconds is healthy. Anything over 40% is severe leak."
        },
        {
            "q": "Around how many characters does a mobile home feed truncate video titles?",
            "choices": ["A) 20 characters", "B) 40 characters", "C) 60 characters", "D) 100 characters"],
            "ans": "B",
            "explain": "Mobile home feeds cut off around 40 characters, while desktop search cuts around 60."
        },
        {
            "q": "Why should dead air be cut from the middle of a pause rather than flush against words?",
            "choices": [
                "A) To save disk space",
                "B) To keep a natural breath on both sides so the speaker doesn't sound gasping",
                "C) Because YouTube filters silence",
                "D) To make the video exactly 8 minutes"
            ],
            "ans": "B",
            "explain": "Trimming from the middle keeps a natural breath cushion before and after words."
        },
        {
            "q": "Which of the following breaks YouTube's chapter rendering rules?",
            "choices": [
                "A) Having 5 chapters",
                "B) First chapter starting at 00:00",
                "C) First chapter starting at 00:05",
                "D) Each chapter being 30 seconds long"
            ],
            "ans": "C",
            "explain": "The first chapter MUST begin at 00:00 or YouTube will not render the chapter bar."
        },
        {
            "q": "What is the ceiling for words on a thumbnail at feed size?",
            "choices": ["A) 3 words", "B) 8 words", "C) 12 words", "D) As many as fit"],
            "ans": "A",
            "explain": "At mobile feed size, a 4th word becomes an illegible grey smear. 3 words max."
        }
    ]

    score = 0
    for i, item in enumerate(questions, 1):
        print(f"\nQuestion {i}: {item['q']}")
        for c in item["choices"]:
            print(f"  {c}")
        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans == item["ans"]:
            print("  [CORRECT!] " + item["explain"])
            score += 1
        else:
            print(f"  [INCORRECT] The correct answer is {item['ans']}. {item['explain']}")

    print(f"\nYour Final Score: {score} / {len(questions)}")
    if score == len(questions):
        print("Mastery Level: Lead YouTube Strategist!")
    elif score >= 3:
        print("Mastery Level: Solid Practitioner. Review the guidelines to master all details.")
    else:
        print("Mastery Level: Apprentice. Run `python learn.py --all` to level up!")

def generate_topic_hooks(topic):
    print_header(f"Generated Hook Options for: \"{topic}\"")
    templates = [
        ("The Statistic", f"94% of people trying {topic} fail in the first week. Here is what the other 6% do."),
        ("The Mistake", f"Your approach to {topic} is why you are not seeing results. It is not the algorithm."),
        ("Contrarian Flip", f"Everyone tells you to do {topic} every day. I tested it for 30 days and found the opposite."),
        ("The Reveal", f"I am going to show you the exact 3-step blueprint for {topic} on screen right now."),
        ("The Clock", f"In the next 6 minutes, you will master {topic} without wasting another dollar.")
    ]
    print("Drafting 5 formula-aligned hooks and scoring them:\n")
    script_dir = os.path.join(HERE, "..", "yt-script")
    sys.path.insert(0, script_dir)
    try:
        import hookscore
        for name, hook in templates:
            parts, verdict, fname, hits = hookscore.score(hook)
            band_str = hookscore.band(verdict)
            print(f"  [{name}] (Verdict: {verdict}/100 - {band_str})")
            print(f"  \"{hook}\"")
            print(f"  Weakest link: {min(parts, key=parts.get)} -> {hookscore.FIX[min(parts, key=parts.get)]}\n")
    except Exception as e:
        for name, hook in templates:
            print(f"  [{name}] \"{hook}\"")

def main():
    args = sys.argv[1:]
    if not args or "--all" in args:
        show_overview()
        show_packaging()
        show_retention()
        show_editing()
        show_chapters()
        show_viral()
        list_formulas()
        return

    if "--list" in args:
        list_formulas()
    elif "--formula" in args:
        idx = args.index("--formula")
        if idx + 1 < len(args):
            inspect_formula(args[idx + 1])
        else:
            print("Please specify a formula name or id, e.g. `python learn.py --formula the-statistic`")
    elif "--packaging" in args:
        show_packaging()
    elif "--retention" in args:
        show_retention()
    elif "--editing" in args:
        show_editing()
    elif "--chapters" in args:
        show_chapters()
    elif "--viral" in args:
        show_viral()
    elif "--topic" in args:
        idx = args.index("--topic")
        if idx + 1 < len(args):
            generate_topic_hooks(args[idx + 1])
        else:
            print("Please specify a topic string.")
    elif "--quiz" in args:
        run_quiz()
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
