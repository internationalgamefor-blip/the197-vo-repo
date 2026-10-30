#!/usr/bin/env python3
"""Generate all 60 ElevenLabs VO lines (George) with mood-matched settings.
Reads VO lines verbatim from russia-10min-script.md, in order.
Mood map by shot (stability, style):
 1-3 intro calm, 4-9 warm story, 10-13 reverent, 14-19 tense invasion,
 20-24 hopeful rise, 25-28 proud, 29 dark, 30 somber troubles,
 31-37 reform energy, 38-43 tense/war, 44-49 strained revolution,
 50-53 heavy then triumphant, 54-56 awe/tense, 57-60 closing reflective.
"""
import re, subprocess, sys, os
VOICE = "JBFqnCBsd6RMkjVDRZzb"
OUT = os.path.expanduser("~/workspace/the197/vo-elevenlabs")
os.makedirs(OUT, exist_ok=True)
script = open(os.path.expanduser("~/workspace/the197/russia-10min-script.md")).read()
lines = re.findall(r"^\s+VO: (.+)$", script, re.M)
assert len(lines) == 60, f"found {len(lines)} VO lines, expected 60"

def mood(n):
    if n <= 3: return (0.60, 0.20)
    if n <= 9: return (0.55, 0.30)
    if n <= 13: return (0.60, 0.25)
    if n <= 19: return (0.35, 0.65)
    if n <= 24: return (0.50, 0.40)
    if n <= 28: return (0.50, 0.45)
    if n == 29: return (0.40, 0.50)
    if n == 30: return (0.45, 0.40)
    if n <= 37: return (0.50, 0.45)
    if n <= 43: return (0.35, 0.60)
    if n <= 49: return (0.40, 0.50)
    if n <= 52: return (0.40, 0.55)
    if n == 53: return (0.55, 0.45)
    if n == 54: return (0.55, 0.40)
    if n <= 56: return (0.40, 0.55)
    return (0.55, 0.35)

helper = os.path.expanduser("~/workspace/custom-connectors/custom.elevenlabs/bin/elevenlabs.py")
for i, text in enumerate(lines, 1):
    out = f"{OUT}/vo-{i:02d}.mp3"
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"skip {i:02d} (exists)")
        continue
    st, sty = mood(i)
    r = subprocess.run(["python3", helper, "tts", "--voice-id", VOICE,
                        "--text", text, "--out", out,
                        "--stability", str(st), "--style", str(sty)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL {i:02d}: {r.stderr[-500:]}"); sys.exit(1)
    print(f"{i:02d} ok ({st}/{sty}) {text[:60]}")
print("ALL DONE")
