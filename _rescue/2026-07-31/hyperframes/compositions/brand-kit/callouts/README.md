# Brand callouts — the video callout engine, library-only proof

The P2 proof for the video callout engine: on-brand callout compositions rendered by Hyperframes and composited over a video. No 21st, no n8n yet — this proves the render + composite spine.

## What's here

- `stat.html`, `quote.html`, `keyterm.html` — three callout compositions on the brand kit (Montserrat/Inter, #0066FF), each a transparent-overlay `#stage` with `data-start`/`data-duration` timing and a CSS entrance animation.
- `render.mjs` — POSTs a composition to the producer (`:9847`) and saves the output. `node render.mjs <in.html> <out> [mp4|webm|mov]`.
- `build-demo.sh` — the full pipeline: render → base clip → chroma-key composite → `callout-demo.mp4`.
- `callout-demo.mp4` — the built proof (3 callouts over a branded base clip).

## Run it

```bash
cd ~/Documents/hyperframes && node packages/producer/dist/public-server.js   # producer on :9847
cd compositions/brand-kit/callouts && ./build-demo.sh                          # -> callout-demo.mp4
```

## NOTE — why chroma-key, not alpha

This producer build does not emit usable alpha: `format:webm` returns `yuv420p` (alpha stripped) and `format:mov` (ProRes 4444) fails at faststart. So the compositions carry a green chroma background (`#00E000`) and ffmpeg keys it out with `colorkey` + `despill`. When the producer's alpha output is fixed, drop the chroma background back to `transparent` and composite the WebM/MOV overlay directly — no key needed.

## Next (the engine around this)

- Define `callout-spec.schema.json` and drive composition generation from a callout plan (the transcript beats).
- N4: source callout designs from 21st, reverse-engineer to the spec, bind to these brand tokens.
- Swap the lavfi base clip for a real graded VO clip via video-use; place callouts at real transcript timestamps.
- Wrap in n8n (`video-callout-subchain`).
