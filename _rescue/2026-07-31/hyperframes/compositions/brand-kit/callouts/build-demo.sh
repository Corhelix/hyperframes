#!/usr/bin/env bash
# Callout proof pipeline: render 3 brand callouts via Hyperframes, composite over a base clip.
# Requires the producer running: cd ~/Documents/hyperframes && node packages/producer/dist/public-server.js  (:9847)
set -euo pipefail
cd "$(dirname "$0")"

# 1) Render each composition to MP4 (green chroma bg — producer alpha output is broken in this build; see NOTE)
node render.mjs stat.html    stat-k.mp4    mp4
node render.mjs quote.html   quote-k.mp4   mp4
node render.mjs keyterm.html keyterm-k.mp4 mp4

# 2) Branded base clip (swap this for a real graded VO clip in production)
ffmpeg -y -f lavfi -t 16 -i "gradients=s=1920x1080:c0=0x0a0e1a:c1=0x14356e:x0=0:y0=0:x1=1920:y1=1080" \
  -r 30 -pix_fmt yuv420p base.mp4 -loglevel error

# 3) Chroma-key + despill each callout, composite at its beat time
ffmpeg -y -i base.mp4 -i stat-k.mp4 -i quote-k.mp4 -i keyterm-k.mp4 -filter_complex \
"[1:v]colorkey=0x00E000:0.40:0.15,despill=type=green:mix=0.6[k1];[k1]setpts=PTS-STARTPTS+0.5/TB[c1];\
[2:v]colorkey=0x00E000:0.40:0.15,despill=type=green:mix=0.6[k2];[k2]setpts=PTS-STARTPTS+5.5/TB[c2];\
[3:v]colorkey=0x00E000:0.40:0.15,despill=type=green:mix=0.6[k3];[k3]setpts=PTS-STARTPTS+10.5/TB[c3];\
[0:v][c1]overlay=eof_action=pass:enable='between(t,0.5,5.5)'[o1];\
[o1][c2]overlay=eof_action=pass:enable='between(t,5.5,10.5)'[o2];\
[o2][c3]overlay=eof_action=pass:enable='between(t,10.5,15.5)'[o3]" \
  -map "[o3]" -t 16 -r 30 -pix_fmt yuv420p -c:v libx264 -crf 18 callout-demo.mp4 -loglevel error

echo "built callout-demo.mp4"
