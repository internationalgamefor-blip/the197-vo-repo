import re, subprocess, sys, os
VOICE="JBFqnCBsd6RMkjVDRZzb"
OUT=os.path.expanduser("~/workspace/the197/shorts/vo"); os.makedirs(OUT, exist_ok=True)
text=open(os.path.expanduser("~/workspace/the197/shorts-vo-scripts.md")).read()
# parse segments
shorts={}
for m in re.finditer(r"## Short (\d+) —[^\n]*\n(.*?)(?=\n## Short |\Z)", text, re.S):
    segs=re.findall(r"^\d+\.\s*(.+)$", m.group(2), re.M)
    shorts[int(m.group(1))]=segs
assert len(shorts)==4 and all(len(v)==4 for v in shorts.values()), shorts.keys()
moods={1:(0.55,0.30),2:(0.35,0.65),3:(0.50,0.45),4:(0.40,0.55)}
helper=os.path.expanduser("~/workspace/custom-connectors/custom.elevenlabs/bin/elevenlabs.py")
for s,segs in shorts.items():
    st,sty=moods[s]
    for j,seg in enumerate(segs,1):
        out=f"{OUT}/s{s}seg{j}.mp3"
        if os.path.exists(out) and os.path.getsize(out)>1000: print(f"skip s{s}seg{j}"); continue
        r=subprocess.run(["python3",helper,"tts","--voice-id",VOICE,"--text",seg,"--out",out,"--stability",str(st),"--style",str(sty)],capture_output=True,text=True)
        if r.returncode!=0: print(f"FAIL s{s}seg{j}: {r.stderr[-500:]}"); sys.exit(1)
        print(f"s{s}seg{j} ok")
print("ALL DONE")
