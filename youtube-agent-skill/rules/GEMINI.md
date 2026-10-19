# YouTube Channel Operations & Production Rules

When assisting with YouTube content creation, scripting, packaging, editing, and channel strategy, strictly follow these studio rules:

## 1. Editorial Integrity & The Publication Gate
- **Human Uploads Only**: Nothing publishes automatically. The agent scripts, lints, and analyzes; the creator uploads and publishes.
- **The Decision Question**: Always end every run with a copy-ready block and the explicit question: **"ship it, or change it?"**
- **No Hallucinated Figures**: Never invent a number, view count, percentage, source, or result. If a metric would strengthen an argument or script and is not supplied, ask the creator for it or write the line without it.

## 2. Hook & Script Doctrine (The First 15 Seconds)
- **Confirm the Click**: The very first sentence must confirm the exact promise of the title. If the video ignores its title, viewers leave at 0:08.
- **No Self-Introductions**: Never open with who you are ("Hey guys, welcome back to my channel"), a subscribe pitch, or prolonged channel bumper. Those are the primary cause of the 0:30 cliff.
- **The Turn (0:15 - 0:45)**: State what the video will do in one sentence, then immediately begin doing it.
- **Visuals on Every Beat**: Scripts must explicitly specify `[ON SCREEN: ...]` for every spoken beat.

## 3. Packaging Doctrine (Title + Thumbnail as ONE Unit)
- **Zero Duplication**: The thumbnail text must NOT duplicate the words in the title. They share a single click surface; repeating words wastes half your real estate.
- **The 3-Word Ceiling**: Maximum 3 words on the thumbnail at mobile feed size. A 4th word becomes an illegible grey blur.
- **Truncation Awareness**: Desktop search cuts near 60 characters (losing the tail); mobile home feed cuts near 40 characters (must preserve the subject).
- **Concrete Over Hype**: Favor specific numbers, dates, or named entities over generic hype words ("insane", "massive", "ultimate"). Maximum 2 all-caps words.

## 4. Retention Diagnostics & Edit Principles
- **Hook Leak First**: Hook leak is what is lost in the first 30 seconds. Under 25% is healthy. Hook leak is always a script issue (first 15s), never an edit issue.
- **Cliffs vs. Slide**: Sudden drops (>0.8%) are moments (unannounced sponsor reads, topic changes, slow setups). A steady slide across the middle is pacing—fix it by trimming the middle, not by rewriting.
- **Dead Air Trimming**: When cutting pauses from transcripts, trim from the *middle* of the gap to preserve breath cushioning on both sides.

## 5. Voice Profile Precedence
- Check for `voice.md` in workspace (`./youtube/voice.md`, `.agent/youtube/voice.md`), then global `~/.gemini/youtube/voice.md` or `~/.claude/youtube/voice.md`. Respect creator cadence, banned words, and formatting guidelines.
