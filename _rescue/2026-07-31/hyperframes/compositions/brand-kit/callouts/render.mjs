// Render a Hyperframes composition via the producer and save the output.
// usage: node render.mjs <composition.html> <out.file> [format=mp4|webm|mov]
import { readFileSync, writeFileSync } from 'node:fs';

const [, , inPath, outPath, format = 'mp4'] = process.argv;
const html = readFileSync(inPath, 'utf8');

const res = await fetch('http://localhost:9847/render', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ html, format }),
});
const j = await res.json();
if (!j.success) { console.error('render failed', JSON.stringify(j).slice(0, 400)); process.exit(1); }
const dl = await fetch(`http://localhost:9847/outputs/${j.outputToken}`);
const buf = Buffer.from(await dl.arrayBuffer());
writeFileSync(outPath, buf);
console.log(`${format} ${buf.length} bytes -> ${outPath} (${j.videoDurationSeconds}s, ${j.durationMs}ms render)`);
