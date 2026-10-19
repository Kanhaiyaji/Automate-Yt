---
name: yt-learn
description: >-
  Master and practice YouTube channel engineering: the 21 hook formulas,
  packaging laws (title + thumbnail as one unit), retention leak diagnostics
  (hook leak, cliffs, slide), transcript EDL cutting, and outlier virality.
  Use for "teach me YouTube skills", "how do hooks work", "explain the 21
  formulas", "quiz me on retention", "drill my ideas", or a walkthrough of the
  YouTube Agent tools.
---

# yt-learn

Interactive coach and engineering reference for running a YouTube channel with code and deterministic tools.

```bash
python learn.py --list                         # List all 21 hook formulas
python learn.py --formula the-statistic        # Inspect a formula's shape, example, failure mode
python learn.py --packaging                    # Mobile (40) vs Desktop (60) & 3-word thumb rules
python learn.py --retention                    # Diagnose Hook Leak (<25%), Cliffs (>0.8%), and Slide
python learn.py --editing                      # Dead-air trimming from the middle & restart detection
python learn.py --chapters                     # Mandatory 00:00, 3+ count, 10s min rendering rules
python learn.py --viral                        # Outlier multiplier over own channel's median
python learn.py --topic "Your Topic"           # Auto-generate & score 5 formula hooks for a topic
python learn.py --quiz                         # Interactive mastery quiz
```

## The Core Doctrines

### 1. The Hook Doctrine (The First 15 Seconds)
The first 15 seconds is the whole job. A hook must do THREE things or it leaks:
1. **Confirm the Click**: Reassure the viewer that the title they clicked is real in sentence one.
2. **Open an Unclosed Loop**: Raise a question they cannot answer on their own.
3. **Prove the Payoff Exists**: Show the artifact or promise early.

**The Golden Rule**: Never open with who you are or a subscribe pitch. The first 15 seconds is for the viewer, not the creator.

### 2. The Packaging Doctrine (Title + Thumbnail = One Unit)
- **Shared Click Surface**: If the thumbnail text repeats the title, half the click surface is wasted.
- **The 3-Word Limit**: On mobile feeds, a 4th word on a thumbnail becomes an illegible blur.
- **Truncation Bands**:
  - Mobile home feed cuts around **40 characters** (subject must survive).
  - Desktop search cuts around **60 characters** (tail is lost).
- **Concrete Details Win**: Specific numbers, dates, and names outperform empty hype words ("insane", "massive", "secret"). Maximum 2 all-caps words.

### 3. The Retention Diagnostic Order
When reviewing retention exports (`/yt-retention`):
1. **Hook Leak (0:00 - 0:30)**: Under 25% lost is healthy. If leaking >25%, fix the script's first 15s.
2. **Cliffs (>0.8% instant drop)**: Single moments where viewers leave. Cross-reference transcript at that second. Usually a sudden sponsor read, unannounced topic switch, or slow setup.
3. **Slide**: Steady loss across the middle. This is a PACING issue. Cut the middle; do not rewrite.

### 4. Transcript EDL Principles
- **Middle Trimming**: Gaps > 0.45s must be cut from the middle (`floor / 2` preserved on each side). Cutting flush against words makes speech sound gasping.
- **Restart Detection**: Compare restarted sentences against the last *speech* cue, ignoring filler words like "um" in between.

### 5. Outlier Virality (Median Multiplier)
Raw view counts measure channel size, not idea quality. An outlier is a video that beats its channel's own median views by 2x or more (requiring at least 4 videos to establish a valid baseline).

## Learning Workflows

When the user asks to learn or improve:
1. **Diagnose**: Run `python learn.py --topic "<user idea>"` to brainstorm and score initial angles.
2. **Drill**: Guide the user through selecting a formula, refining the weakest link from `hookscore.py`, and linting the title/thumb pairing via `title.py`.
3. **Test**: Run the interactive quiz or analyze a real retention CSV/transcript to cement the concepts.

## The Gate

Nothing here publishes. This skill educates, drafts, and lints. The human creator always retains editorial control.
Every recommendation ends with: **ship it, or change it?**
