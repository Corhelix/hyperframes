"""Draft layout: slide top-left, captions bottom-left, head panel lower right.
Reads cues.json and edl-aligned.json, renders one 1920x1080 canvas PNG per cue with PIL,
then composites over preview-aligned.mp4 with ffmpeg. Output: draft-layout.mp4."""
import json,re,subprocess
from PIL import Image,ImageDraw,ImageFont
SRC_CUE={"0:37":157,"0:46":166,"1:40":222,"1:54":236,"2:07":249,"2:47":290,"3:17":334,"5:14":470,"6:35":567,"8:04":670,
 "9:12":739,"9:20":747,"10:03":790,"10:33":820,"11:24":887,"11:32":895,"11:49":912,"12:03":926,"12:51":978,"13:03":990,"13:20":1005.7,"13:45":1030}
R=json.load(open('edl-aligned.json'))['ranges']
def out(t):
    o=0
    for r in R:
        if t<r['start']: return o
        if t<=r['end']: return o+t-r['start']
        o+=r['end']-r['start']
    return o
C=json.load(open('cues.json'))['cues']
BG={"white":(255,255,255),"blue":(30,91,255),"own":(10,26,58)}
INK={"white":(14,32,64),"blue":(255,255,255),"own":(255,255,255)}
F="/System/Library/Fonts/Helvetica.ttc"
fb=ImageFont.truetype(F,40,index=1); fr=ImageFont.truetype(F,34,index=0); fs=ImageFont.truetype(F,26,index=0)
SX,SY,SW,SH=40,40,1280,720          # slide box
HX,HY,HW,HH=1360,455,520,585        # head panel
wins=[]
for k,c in enumerate(C):
    a=out(SRC_CUE[c['t']])
    nxt=out(SRC_CUE[C[k+1]['t']]) if k+1<len(C) else a+15
    b=min(nxt,a+18) if nxt-a<=25 else a+15
    cv=Image.new("RGB",(1920,1080),BG[c['bg']])
    s=Image.open("slides/"+c['slide']).convert("RGBA")
    s.thumbnail((SW,SH),Image.LANCZOS)
    if c['bg']!="own":
        pad=Image.new("RGBA",s.size,BG[c['bg']]+(255,)); pad.alpha_composite(s); s=pad
    cv.paste(s,(SX+(SW-s.width)//2,SY+(SH-s.height)//2),s)
    d=ImageDraw.Draw(cv); y=790
    if c.get('intro_caption'):
        d.text((SX,y),c['intro_caption'].upper(),font=fs,fill=INK[c['bg']]); y+=44
    for i,line in enumerate(c.get('caption',[])):
        d.text((SX,y),line,font=fb if i==0 else fr,fill=INK[c['bg']]); y+=58
    cv.save(f"compose/cue{k+1:02d}.png")
    wins.append((round(a,2),round(b,2)))
m=Image.new("L",(HW,HH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,HW-1,HH-1),radius=28,fill=255); m.save("compose/headmask.png")
inputs=["-i","preview-aligned.mp4","-loop","1","-i","compose/headmask.png"]
for k in range(len(C)): inputs+=["-loop","1","-i",f"compose/cue{k+1:02d}.png"]
fc=["[0:v]split=2[base][hsrc]","[hsrc]crop=960:1080:480:0,scale=%d:%d,format=rgba[hs]"%(HW,HH),"[1:v]format=gray,scale=%d:%d[mk]"%(HW,HH),"[hs][mk]alphamerge[head]"]
cur="[base]"
for k,(a,b) in enumerate(wins):
    fc.append(f"{cur}[{k+2}:v]overlay=0:0:enable='between(t,{a},{b})':shortest=0[v{k}]"); cur=f"[v{k}]"
en="+".join(f"between(t,{a},{b})" for a,b in wins)
fc.append(f"{cur}[head]overlay={HX}:{HY}:enable='{en}':shortest=0,format=yuv420p[vout]")
dur=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","preview-aligned.mp4"],capture_output=True,text=True).stdout.strip()
cmd=["ffmpeg","-nostdin","-loglevel","error","-y",*inputs,"-filter_complex",";".join(fc),"-map","[vout]","-map","0:a","-t",dur,"-c:v","libx264","-preset","medium","-crf","20","-c:a","copy","draft-layout.mp4"]
json.dump(wins,open("compose/windows.json","w"))
print(len(wins),"slide windows"); print(wins)
subprocess.run(cmd,check=True); print("done")
