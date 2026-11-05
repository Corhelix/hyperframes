# corhelix/video-edit

The tool home for the ALC Group / Andrew Cockburn video edit SOP. The SOP itself is in alc-group, at `andrew-cockburn/content/video-edit-sop/`.

Everything outside `corhelix/` in this repo is upstream Hyperframes (heygen-com/hyperframes). It is kept as the canonical base and is never edited here. Our work lives only in this folder and in `compositions/brand-kit/`.

## current/

The scripts the SOP runs.

| Script | Does | Status |
|---|---|---|
| `compose.py` | Composites slides, the speaker panel, Hyperframes callouts and the subtitle text layer over the cut. All paths are parameters; reads layers.json | Used on the 4 Nov 2026 Gravitate Loom (Draft v2) |
| `cut_align.py` | The v0.1 cut builder. Its pause rule (1.5 s, trimmed to about 0.7 s) is superseded by the SOP rule: up to about 2 to 2.5 s is natural, and no dead air of around 5 s. It is kept only for its frame slicing. Still holds the 3 Nov paths. | Superseded rule |
| `render_exact.py` | Runs video-use render.py unchanged but caps each segment at its exact frame count, so the output matches the EDL sum (V6). Use frame-aligned EDL ranges | Used on the 4 Nov take |
| `build_layers.py` | Stage 11: turns a layer plan, the EDL and the Scribe words into layers.json, landing each layer on its spoken word and checking the SOP copy and hold rules | Used on the 4 Nov take |
| `gap_sheets.py` | Builds gridded every-frame contact sheets for long gaps, read by eye | Built (PR 20) |
| `script_lock.py` | The cut gate. Every span the EDL removes must be a repeated redo, join padding under 0.3 s, or covered by one of Andrew's own words in `authorisations.json`. Also fails a cut inside a word and reordered ranges. Tests: `python3 -m unittest test_script_lock` from `current/` | Built (PR 1 of 3 for /video-edit) |
| `twentyfirst_lookup.py` | The 21st.dev lookup for HTML callouts that are not Hyperframes templates. `search`, `video-blocks`, `get`, and `record`, which writes `design_ref` onto the layer row only for a slug or id a logged lookup returned. Key from the vault, never printed. Tests: `python3 -m unittest test_twentyfirst_lookup` | Built; API verified 5 Nov 2026 |
| `layers_to_xml.py` | Turns edl.json, layers.json and subtitles.json into FCPXML, xmeml and EDL, with text kept as text | To build |
| `check_layers.py` | Verifies the composited draft, V1 to V7: every join, layer and subtitle. Head position on a join stays a human read; the script flags it | Built, used on the 4 Nov take |
| `grade_match.py` | Sample, measure, correct, test slices, recheck | To build |
| `compose_916.py` | The 9:16 layout | To build |

Both existing scripts still hold the Gravitate run's paths. Make the paths parameters before reuse.

## callouts/ and subtitles/

Hyperframes compositions for the text layers (SOP stage 12). `callouts/DESIGN.md` is the visual identity, written before any HTML; `callouts/template.html` plus `build_callouts.py` render each callout in layers.json as a transparent WebM. `subtitles/build_subtitles.py` builds subtitles.json and captions.srt and renders the text layer in chunks. Both lint clean with `hyperframes@0.9.10` and render with `--format webm`, which carries alpha. The run on the 4 Nov take used Montserrat and Inter, the SOP look, which the Hyperframes typography guide warns against; the deviation is logged in DESIGN.md.

## References (used where they live, not copied)

| Script | Source | Does |
|---|---|---|
| transcribe.py, pack_transcripts.py, render.py, grade.py, timeline_view.py | browser-use/video-use, `helpers/` (local `~/Documents/video-use`) | Scribe transcript, segment render with fades and loudnorm, grade presets |
| detect_cuts.py, build_composition.py, au_spelling.py, export_package.py, decide_cuts.py | Corhelix/N8n-projects `projects/long-form-shorts-engine/services/talking-head/` | Retakes and fillers, subtitle cues, AU spelling, FCPXML 1.9 with lanes. These are plain Python and do not need n8n. decide_cuts.py calls a paid API, so run it with `--no-model`. |
| make_captions.py, social_reframe.py, social_enhance.py | Corhelix/N8n-projects `projects/long-form-shorts-engine/tools/` | Subtitle cues, 9:16 crop, 9:16 template |
| export_xml.py, render_cut.py, match_audio.py, check_a7.py | Corhelix/alc-group `andrew-cockburn/content/tasks/2026-10-10-pascoe-long-form-video-experiment/harness/` | FCPXML 1.8, xmeml v4 and CMX3600; conform; audio sync; join check |
| produce.py, compose.py, brand_gate.py | Corhelix/Agent-and-Config-Files `projects/hyperframes/pipeline/` | Applies a brand kit from tokens.css and gates the render against it |
| Brand-kit compositions and callouts | This repo, `compositions/brand-kit/` | stat, quote and keyterm callouts, lower-third, section-title, intro, outro |
