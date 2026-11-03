# corhelix/video-edit

The tool home for the ALC Group / Andrew Cockburn video edit SOP. The SOP itself is in alc-group, at `andrew-cockburn/content/video-edit-sop/`.

Everything outside `corhelix/` in this repo is upstream Hyperframes (heygen-com/hyperframes). It is kept as the canonical base and is never edited here. Our work lives only in this folder and in `compositions/brand-kit/`.

## current/

The scripts the SOP runs.

| Script | Does | Status |
|---|---|---|
| `compose.py` | Builds the 16:9 image canvases (PIL) and composites them over the cut with ffmpeg | Used on the 3 Nov 2026 Gravitate Loom |
| `cut_align.py` | The v0.1 cut builder. Its pause rule (1.5 s, trimmed to about 0.7 s) is superseded by the SOP rule: up to about 2 to 2.5 s is natural, and no dead air of around 5 s. It is kept only for its frame slicing. | Superseded rule |
| `gap_sheets.py` | Builds gridded every-frame contact sheets for long gaps, read by eye | To build |
| `layers_to_xml.py` | Turns edl.json, layers.json and subtitles.json into FCPXML, xmeml and EDL, with text kept as text | To build |
| `check_layers.py` | Checks every layer's position, timing and content (V2 to V5) | To build |
| `grade_match.py` | Sample, measure, correct, test slices, recheck | To build |
| `compose_916.py` | The 9:16 layout | To build |

Both existing scripts still hold the Gravitate run's paths. Make the paths parameters before reuse.

## References (used where they live, not copied)

| Script | Source | Does |
|---|---|---|
| transcribe.py, pack_transcripts.py, render.py, grade.py, timeline_view.py | browser-use/video-use, `helpers/` (local `~/Documents/video-use`) | Scribe transcript, segment render with fades and loudnorm, grade presets |
| detect_cuts.py, build_composition.py, au_spelling.py, export_package.py, decide_cuts.py | Corhelix/N8n-projects `projects/long-form-shorts-engine/services/talking-head/` | Retakes and fillers, subtitle cues, AU spelling, FCPXML 1.9 with lanes. These are plain Python and do not need n8n. decide_cuts.py calls a paid API, so run it with `--no-model`. |
| make_captions.py, social_reframe.py, social_enhance.py | Corhelix/N8n-projects `projects/long-form-shorts-engine/tools/` | Subtitle cues, 9:16 crop, 9:16 template |
| export_xml.py, render_cut.py, match_audio.py, check_a7.py | Corhelix/alc-group `andrew-cockburn/content/tasks/2026-10-10-pascoe-long-form-video-experiment/harness/` | FCPXML 1.8, xmeml v4 and CMX3600; conform; audio sync; join check |
| produce.py, compose.py, brand_gate.py | Corhelix/Agent-and-Config-Files `projects/hyperframes/pipeline/` | Applies a brand kit from tokens.css and gates the render against it |
| Brand-kit compositions and callouts | This repo, `compositions/brand-kit/` | stat, quote and keyterm callouts, lower-third, section-title, intro, outro |
