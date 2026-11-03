"""Choose cut points inside each pause so head and face line up best across the cut.
Reads the Scribe transcript, rebuilds the natural cut, then for every boundary samples
frames at 10 fps in the allowed pause window either side, compares the centre face region,
and keeps the out/in pair with the smallest difference. Writes edl-aligned.json and a
side-by-side PNG per cut in verify/cuts/."""
import json,re,subprocess,numpy as np
from PIL import Image
SRC="/Users/burns/Movies/2026-11-03 16-01-53.mp4"
d=json.load(open('transcripts/2026-11-03 16-01-53.json'))
W=[w for w in d['words'] if w['type']=='word']
n=lambda w:re.sub(r"[^a-z]","",w['text'].lower())
drop=set()
def win(a,b,pred=lambda w:True):
    for i,w in enumerate(W):
        if a-0.01<=w['start']<=b+0.01 and pred(w): drop.add(i)
for i,w in enumerate(W):
    if w['start']<120.0: drop.add(i)
idx=[i for i,w in enumerate(W) if 175<=w['start']<=179.3]
s=next(i for i in idx if n(W[i])=="jumping"); e=next(i for i,w in enumerate(W) if w['start']>=179.3 and n(w)=="jumping")
drop.update(range(s,e))
win(257.32,257.96); win(373.15,374.93); win(401.45,401.73)
win(402.51,403.6,lambda w:n(w) in("realistically","out")); win(446.57,447.67)
win(687.0,688.2,lambda w:n(w) in("training","s"))
K=[(i,w) for i,w in enumerate(W) if i not in drop]
segs=[];cur=[K[0][1]]
for (ia,a),(ib,b) in zip(K,K[1:]):
    if b['start']-a['end']>1.5 or ib-ia>1: segs.append(cur);cur=[b]
    else: cur.append(b)
segs.append(cur)
def frames(t0,t1):
    t0=max(0,t0); dur=max(0.1,t1-t0)
    raw=subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-ss",f"{t0:.3f}","-t",f"{dur:.3f}","-i",SRC,
        "-vf","fps=10,crop=iw*0.44:ih*0.75:iw*0.28:0,scale=96:96,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,96,96).astype(np.float32)
    return [(t0+k/10,a[k]) for k in range(len(a))]
ranges=[[segs[0][0]['start']-0.30,None]]
report=[]
for k in range(len(segs)-1):
    last=segs[k][-1]['end']; nxt=segs[k+1][0]['start']
    # all removed material between them is fair game for the out window up to 2 s, the in window up to 2 s back
    o_lo,o_hi=last+0.12,min(last+2.0,nxt-0.05)
    i_lo,i_hi=max(nxt-2.0,last+0.05),nxt-0.08
    # words that were dropped between last and nxt limit the windows so no removed speech returns
    dropped=[W[i] for i in drop if last<W[i]['start']<nxt]
    if dropped:
        o_hi=min(o_hi,min(w['start'] for w in dropped)-0.03)
        i_lo=max(i_lo,max(w['end'] for w in dropped)+0.03)
    O=frames(o_lo,max(o_hi,o_lo+0.1)); I=frames(i_lo,max(i_hi,i_lo+0.1))
    best=None
    for to,fo in O:
        for ti,fi in I:
            air=(to-last)+(nxt-ti)
            if not 0.45<=air<=1.1: continue
            sc=float(np.mean((fo-fi)**2))
            if best is None or sc<best[0]: best=(sc,to,ti,fo,fi)
    if best is None:  # fall back to the plain natural pads
        to,ti=last+0.40,nxt-0.30; sc=-1
        fo,fi=O[-1][1],I[0][1]
    else: sc,to,ti,fo,fi=best
    ranges[-1][1]=to; ranges.append([ti,None])
    # side-by-side full frames for the record
    subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-ss",f"{to:.3f}","-i",SRC,"-ss",f"{ti:.3f}","-i",SRC,
        "-filter_complex","[0:v]trim=end_frame=1,scale=640:-2[a];[1:v]trim=end_frame=1,scale=640:-2[b];[a][b]hstack","-frames:v","1",f"verify/cuts/cut{k+1:02d}.png"])
    report.append((k+1,round(last,2),round(to,2),round(ti,2),round(nxt,2),round(sc,1)))
ranges[-1][1]=segs[-1][-1]['end']+0.40
tot=sum(b-a for a,b in ranges)
json.dump({"version":1,"sources":{"A":SRC},"ranges":[{"source":"A","start":round(a,3),"end":round(b,3),"beat":"","quote":"","reason":"natural cut, cut points chosen for best head and face alignment"} for a,b in ranges],"grade":"none","total_duration_s":round(tot,2)},open('edl-aligned.json','w'),indent=1)
for r in report: print("cut%02d last-word %s out %s | in %s next-word %s  diff %s"%r)
print(len(ranges),"ranges; total",int(tot//60),"m",round(tot%60),"s")
