# The YouTube agent skill

Eleven Claude skills that run a YouTube channel. Free, MIT, no signup, no API key, nothing to
connect.

One of them writes your script off 21 hook formulas and scores the hook before you waste a take on
it. One lints the title and the thumbnail as a single pairing, because writing them separately is
why half of your click surface says the same thing twice. One reads your audience-retention export
and tells you the exact second people left and what you were saying when they did. One turns a
transcript into an edit decision list. One finds the Shorts already hiding inside a long video. One
goes and finds what is working in your niche and ranks it by how far each video beat its own
channel, not by how big the channel is.

**Nothing gets published until you do it.** These skills write. You upload.

## Install

### In Antigravity / Gemini CLI:

As a global plugin (available in all workspaces):
```bash
# Copy into Antigravity global plugin directory:
cp -r youtube-agent-skill ~/.gemini/config/plugins/youtube-agent
```

Project-local in your current repository:
```bash
# Copy into project workspace customizations:
mkdir -p .agents/skills
cp -r youtube-agent-skill/skills/yt-* .agents/skills/
```

### In Claude Code:

```bash
cp -r youtube-agent-skill/skills/yt-* ~/.claude/skills/
```

Or as a plugin:
```
/plugin marketplace add Jakeschincariol/youtube-agent-skill
/plugin install youtube-agent
```

Then spend ten minutes on [`templates/voice.md`](templates/voice.md). Copy it to
`./youtube/voice.md` or `~/.gemini/youtube/voice.md` (or `~/.claude/youtube/voice.md`) and fill it in, or send the agent three of your own videos and say "write my voice.md from these". Every skill reads that file. It matters more here than anywhere else, because you have to say the words out loud.

## The twelve skills

| command | what it does |
| --- | --- |
| `/yt-learn` | **NEW**: Interactive coach & doctrine reference: explore 21 hook formulas, run quizzes, practice packaging, retention drills, and topic brainstorming. |
| `/yt-script` | One idea into a script. Five hooks off [21 formulas](skills/yt-script/hooks.json), scored, then the spoken script with the retention beats marked. |
| `/yt-package` | Title and thumbnail as one pairing, linted for truncation, duplication and vagueness. |
| `/yt-edit` | A transcript into an edit decision list: dead air, filler cues, retakes, with timecodes. |
| `/yt-comment` | The comment section triaged into four piles, then replies in your voice. Says which one to pin. |
| `/yt-plan` | A week that fits the hours you actually have. One anchor, one cheap one, three Shorts. |
| `/yt-viral` | What is working in your niche, ranked by multiple over each channel's own median. |
| `/yt-retention` | Your retention export read properly: hook leak, the cliffs, the slide, and what to change. |
| `/yt-shorts` | The Shorts already inside a long video, with a new first line written for each. |
| `/yt-seo` | The description, the tags that are worth having, and the three queries this should win. |
| `/yt-chapters` | Chapters from a transcript, validated against YouTube's own rules so they render. |
| `/yt-audit` | The whole channel, ending in ONE fix rather than twenty. |

## The deterministic Python tools

Every one of these runs on a clean Python 3 with zero external dependencies. They are the reason the skills are not just prompts.

```bash
# Unified runner:
python yt_tools.py hook --hook "one line"
python yt_tools.py title --title "..." --thumb "..."
python yt_tools.py deadair transcript.srt
python yt_tools.py chapters transcript.srt
python yt_tools.py retention retention.csv
python yt_tools.py swipe collected.json --min 2.0
python yt_tools.py learn --formula the-statistic

# Or invoke directly:
python skills/yt-script/hookscore.py --hook "one line"        # 5-property hook panel
python skills/yt-package/title.py --title "..." --thumb "..." # title + thumbnail linter
python skills/yt-edit/deadair.py transcript.srt               # edit decision list
python skills/yt-chapters/chapters.py transcript.srt          # validated chapters
python skills/yt-retention/retention.py retention.csv         # where they left, and why
python skills/yt-viral/swipe.py collected.json --min 2.0      # outliers by own-channel multiple
python skills/yt-learn/learn.py --topic "AI Coding"           # interactive learning & hook drill
```

## The fine print

The part most packs leave out.

**It does not publish.** YouTube's Data API would allow it with your own OAuth, which makes this
pack different from the LinkedIn and Instagram ones, where posting is not available at all. It is
still not built here: every skill ends in a block you copy and a question — ship it, or change it?
Anything that claims to run your channel unattended should be read with that distinction in mind.

**`hookscore.py` is a heuristic, not a predictor.** The panel was built and calibrated against 74
real short-form hooks (the first 15 seconds of auto-captions, top-8 and bottom-8 by views across
five channels). It separates deliberately bad hooks from real ones well. It separates a given
creator's hits from their own misses barely at all. A low score is a reason to look again; a high
score is not a promise.

**The formula classifier is about the words, not the result.** When `/yt-viral` says a title used
The Statistic, that is a judgement about the title you can see, not a claim about why the video got
its views.

**`/yt-viral` reads, it does not scrape.** Public listings only. It never logs in as you and never
touches your credentials.

**Tags barely matter** and this pack says so instead of selling you a tag generator.

**Nothing invents a number.** If a skill wants a figure it does not have, it asks you for it or
writes the line without it.

## Licence

MIT. Use it, change it, ship it.
