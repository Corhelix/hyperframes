// Overlay generator, Gravitate Loom take 2 (video edit SOP v0.4, stage 12 overlays).
// Writes one standalone Hyperframes composition per scene and per callout into scenes/<id>/,
// copies only the assets each one needs, and writes scenes.json for the render and Resolve placement steps.
// Times are OUTPUT seconds on the cut (timeline 01:00:00:00 = 0 s, 24 fps).
// Usage: node gen.mjs <layer-plan.json>
import fs from "node:fs";
import path from "node:path";

const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1"));
const SRC = path.join(HERE, "assets-src");
const LOOKUP = "C:/Users/hello/Downloads/PORTFOLIO-GENERAL-WEB-SET-LOT1-2026-11-06/images";
const META = JSON.parse(fs.readFileSync(path.join(SRC, "meta.json"), "utf8").replace(/^\uFEFF/, ""));
const LAYER_PLAN = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const OUTDIR = path.join(HERE, "scenes");
const FPS = 24;

// ---------- geometry (build_layers.py: SLIDE_BOX 40,40 1280x720; PANEL 1360,455 520x585) ----------
// Cards use x 40..1320 and y 40..840 so nothing reaches the speaker panel and there is no dead space under them.
const AX = 40, AY = 40, AW = 1280, AH = 800, CX = AX + AW / 2, CY = AY + AH / 2;

// ---------- the scene plan ----------
const V = (id, poster, mediaStart = 0) => ({ vid: id, poster, mediaStart });
const SCENES = [
  // B2 News Corp
  { id: "s01", type: "blowout", end: 50.56, items: [{ img: "G01", t: 38.56, focus: "22% 26%", z0: 1.9 }] },
  { id: "s02", type: "thumbs", end: 73.86, items: [{ img: "G04", t: 56.58 }, { img: "E17", t: 62.24 }, { img: "008", t: 66.66 }, { img: "009", t: 70.66 }] },
  { id: "s03", type: "deck", end: 81.36, items: [{ img: "063", t: 73.96 }, { img: "060", t: 76.36 }] },
  { id: "s04", type: "stack", end: 109.94, items: [{ img: "E63", t: 85.74 }, { img: "065", t: 93.76 }, { img: "007", t: 103.94 }] },
  { id: "s05", type: "full", end: 119, items: [{ img: "062", t: 113 }] },
  { id: "s06", type: "blowout", end: 137.79, items: [{ img: "012", t: 131.79, focus: "50% 35%", z0: 1.8 }] },
  { id: "s07", type: "full", end: 148, items: [{ img: "064", t: 142 }] },
  { id: "s08", type: "full", end: 160.5, items: [{ img: "G19", t: 152.5 }] },
  // B3 Wolf & Eagle
  { id: "s09", type: "deck", end: 170.79, items: [{ img: "047", t: 162.79 }, { img: "061", t: 165.79 }] },
  { id: "s10", type: "quote", start: 183.36, end: 191.36, quote: "His ability to identify growth opportunities and provide clarity on both immediate wins and long-term direction was outstanding.", source: "Michelle B, Zinus Australia", hl: ["growth", "opportunities", "long-term", "direction"] },
  { id: "s12", type: "quote", start: 203.3, end: 211.3, quote: "His ability to step into complex environments, audit underperforming agencies, and provide a clear, actionable roadmap has been invaluable.", source: "M. Bianchi, Business with 26 Locations Across Australia", hl: ["audit", "underperforming", "agencies,", "clear,", "actionable", "roadmap"] },
  { id: "s13", type: "pan", end: 234.16, items: [{ img: "010", t: 226.16 }] },
  { id: "s14", type: "blowout", end: 248.42, items: [{ img: "116", t: 242.42, focus: "50% 50%", z0: 1.7 }] },
  { id: "s15", type: "full", end: 266.5, items: [{ img: "067", t: 258.5 }] },
  // B4 Panasonic
  { id: "s16", type: "feature", end: 301.97, cards: ["165", "049", "122", "094"], items: [{ card: 0, t: 271.29 }, { card: 1, t: 275.89 }, { card: 2, t: 289.77 }, { card: 3, t: 296.47 }] },
  { id: "s17", type: "cylinder", start: 302.3, end: 310.39, faces: ["053", "051", "047", "049", "094", "046", "067", "165", "082", "061"], picks: [{ face: 0, t: 304.39 }] },
  { id: "s17b", type: "cylinder", start: 324.9, end: 334.07, faces: ["051", "047", "049", "094", "046", "067", "165", "082", "061", "053"], picks: [{ face: 0, t: 327.07 }] },
  { id: "s18", type: "pan", end: 357.93, items: [{ img: "082", t: 351.93 }] },
  { id: "s19", type: "blowout", end: 370.1, items: [{ img: "046", t: 364.1, focus: "50% 45%", z0: 1.7 }] },
  // B5 MGM
  { id: "s20", type: "feature", end: 426.24, cards: ["056", "122", "026"], items: [{ card: 0, t: 386.7 }, { card: 1, t: 397.46 }, { card: 2, t: 410.82 }, { card: 0, t: 421.24 }] },
  { id: "s21", type: "stack", end: 456.24, items: [{ img: "026", t: 437.34 }, { img: "056", t: 451.24 }] },
  { id: "s22", type: "pan", end: 477.84, items: [{ img: "043", t: 468.79 }, { ...V("v042", "v042-poster.jpg"), t: 473.84 }] },
  { id: "s23", type: "full", end: 487.5, items: [{ img: "043", t: 481.5 }] },
  // B6 Education
  { id: "s24", type: "deck", end: 511.4, items: [{ img: "034", t: 500.82 }, { img: "184", t: 506.4 }] },
  { id: "s25", type: "stack", end: 531.4, items: [{ img: "151", t: 518.16, focus: "50% 30%" }, { img: "147", t: 523.4 }] },
  { id: "s26", type: "thumbs", end: 546, items: [{ img: "002", t: 533.26 }, { img: "001", t: 541 }] },
  { id: "s27", type: "pan", end: 562.5, items: [{ img: "189", t: 553.82 }, { img: "E60", t: 558 }] },
  { id: "s28", type: "stack", end: 577.1, items: [{ img: "130", t: 565.4, focus: "73% 79%", z0: 2.2 }, { img: "129", t: 572.1, focus: "50% 9%", z0: 2.0 }] },
  { id: "s29", type: "blowout", end: 592.54, items: [{ img: "123", t: 588.84, focus: "30% 30%", z0: 1.6 }] },
  // B7 AI and systems
  { id: "s30", type: "feature", end: 613.5, cards: ["G22", "120", "153"], items: [{ card: 0, t: 596.68 }, { card: 1, t: 602.3 }, { card: 2, t: 607.5 }] },
  { id: "s31", type: "stack", end: 671.7, items: [{ img: "172", t: 653.92 }, { ...V("v161", "v161-poster.jpg", 2), t: 658.73 }, { ...V("v162", "v162-poster.jpg"), t: 665.7 }] },
  { id: "s32", type: "blowout", end: 689.31, items: [{ img: "G23", t: 681.31, focus: "50% 30%", z0: 1.7 }] },
  { id: "s33", type: "feature", end: 712.6, cards: [V("v160", "v160-poster.jpg"), V("v163", "v163-poster.jpg")], items: [{ card: 0, t: 699.03 }, { card: 1, t: 705.6 }] },
  // B8 Close
  { id: "s34", type: "cylinder", start: 721.2, end: 745.38, faces: ["057", "072", "171", "E21", "068", "070", "074", "081", "167", "175", "069", "076"], picks: [{ face: 0, t: 723.39 }, { face: 1, t: 727.4 }, { face: 2, t: 731.37 }, { face: 3, t: 738.38 }] },
  { id: "s35", type: "thumbs", end: 765.41, items: ["G01", "147", "G22", "056", "043", "171"].map((img, k) => ({ img, t: 757.41 + k * 1.15 })) },
];

// Callouts: layer-plan.json C01..C18 (source time) mapped to output time through the EDL, plus the Connex line.
const CALLOUT_OUT = { C01: 37.77, C02: 55.53, C03: 61.29, C04: 65.83, C05: 115.66, C06: 150.58, C07: 203.31, C08: 286.36, C09: 335.22, C10: 368.32, C11: 382.13, C12: 394.99, C13: 467.85, C14: 486.21, C15: 522.35, C16: 533.29, C17: 618.11, C18: 729.07 };
const CALLOUTS = LAYER_PLAN.callouts.map((c) => ({ id: c.id, t: CALLOUT_OUT[c.id], type: c.type, head: c.head, label: c.label || "", tag: c.type === "quote" ? "Recommendation" : "" }));
CALLOUTS.push({ id: "X01", t: 565.9, type: "keyterm", head: "Implemented college software such as Connex", label: "", tag: "Hillcrest Christian College" });
CALLOUTS.sort((a, b) => a.t - b.t);

// ---------- helpers ----------
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const r2 = (n) => Math.round(n * 1000) / 1000;
function imgInfo(id) {
  const m = META[id];
  if (!m) throw new Error(`no image ${id} in lookup`);
  return { file: m.file, uniform: m.uniform, bg: m.uniform ? m.bg : "#0b1220" };
}
// A media element. Slides (flat edges) fit whole on a matched backdrop; photos fill by cropping.
function media(item, idAttr, start, dur, assets, forceCover = false) {
  if (item.vid) {
    assets.add(`vid/${item.vid}.mp4`); assets.add(`vid/${item.poster}`);
    return `<img class="m" src="assets/${item.poster}" style="object-fit:cover" alt="" /><video id="${idAttr}" class="m" src="assets/${item.vid}.mp4" muted playsinline data-start="${r2(start)}" data-duration="${r2(dur)}" data-media-start="${item.mediaStart || 0}" style="object-fit:cover"></video>`;
  }
  const i = imgInfo(item.img || item);
  assets.add(`img/${i.file}`);
  const fit = !forceCover && i.uniform ? "contain" : "cover";
  return `<img id="${idAttr}" class="m" src="assets/${i.file}" style="object-fit:${fit};object-position:${item.focus || "50% 50%"}" alt="" />`;
}
const bgOf = (item) => (item.vid ? "#0b1220" : imgInfo(item.img || item).bg);

// ---------- scene builders: each returns { html, js } with times relative to scene start ----------
const B = {};

B.blowout = (s, A) => {
  const it = s.items[0], D = s.dur;
  const html = `<div id="c" class="card" style="left:${AX}px;top:${AY}px;width:${AW}px;height:${AH}px;background:${bgOf(it)}"><div id="z" class="zoom">${media(it, "m0", 0, D, A)}</div></div>`;
  const push = D - 0.35 - 1.85;
  const js = `gsap.set("#z",{transformOrigin:"${it.focus || "50% 50%"}"});
tl.fromTo("#c",{opacity:0,scale:0.96},{opacity:1,scale:1,duration:0.5,ease:"power3.out"},0);
tl.fromTo("#z",{scale:${it.z0 || 1.8}},{scale:1,duration:1.5,ease:"power3.inOut"},0.35);
${push > 0.2 ? `tl.to("#z",{scale:1.035,duration:${r2(push)},ease:"none"},1.85);` : ""}
tl.to("#c",{opacity:0,duration:0.35,ease:"power2.in"},${r2(D - 0.35)});`;
  return { html, js };
};

B.full = (s, A) => {
  const it = s.items[0], D = s.dur;
  const html = `<div id="f" style="position:absolute;inset:0;overflow:hidden;background:${bgOf(it)}"><div id="z" class="zoom">${media(it, "m0", 0, D, A)}</div></div>`;
  const js = `gsap.set("#z",{transformOrigin:"${it.focus || "50% 50%"}"});
tl.fromTo("#f",{opacity:0},{opacity:1,duration:0.45,ease:"power2.out"},0);
tl.fromTo("#z",{scale:1},{scale:1.06,duration:${r2(D)},ease:"none"},0);
tl.to("#f",{opacity:0,duration:0.4,ease:"power2.in"},${r2(D - 0.4)});`;
  return { html, js };
};

B.pan = (s, A) => {
  const D = s.dur, n = s.items.length;
  let layers = "", js = `tl.fromTo("#c",{clipPath:"inset(0% 100% 0% 0% round 22px)"},{clipPath:"inset(0% 0% 0% 0% round 22px)",duration:0.75,ease:"power3.inOut"},0);\n`;
  s.items.forEach((it, i) => {
    const t = it.rel, tEnd = i < n - 1 ? s.items[i + 1].rel + 0.6 : D;
    const vidDur = it.vid ? Math.min(D - t, 2.0) : 0; // the 042 preview is 2 s long; the image under it carries on
    layers += `<div id="p${i}" class="zoom" style="background:${bgOf(it)}">${media(it, "m" + i, t, it.vid ? vidDur : D, A, true)}</div>`;
    js += `tl.fromTo("#p${i}",{scale:1.14,xPercent:4},{scale:1.14,xPercent:-4,duration:${r2(tEnd - t)},ease:"none"},${r2(t)});\n`;
    if (i > 0) js += `tl.fromTo("#p${i}",{opacity:0},{opacity:1,duration:0.6,ease:"power2.inOut"},${r2(t)});\n`;
    if (it.vid && i > 0) js += `tl.to("#p${i}",{opacity:0,duration:0.5,ease:"power2.inOut"},${r2(t + vidDur - 0.25)});\n`;
  });
  const html = `<div id="c" class="card" style="left:${AX}px;top:${AY}px;width:${AW}px;height:${AH}px">${layers}</div>`;
  js += `tl.to("#c",{opacity:0,duration:0.35,ease:"power2.in"},${r2(D - 0.35)});`;
  return { html, js };
};

B.thumbs = (s, A) => {
  const D = s.dur, n = s.items.length, TW = 132, TH = 88, G = 14;
  const sw = n * TW + (n - 1) * G, sx = AX + (AW - sw) / 2, MT = AY + TH + 16, MH = AY + AH - MT;
  let thumbs = "", slides = "", js = "";
  s.items.forEach((it, i) => {
    const ii = imgInfo(it.img); A.add(`img/${ii.file}`);
    thumbs += `<div id="t${i}" class="thumb" style="left:${sx + i * (TW + G)}px;top:${AY}px;width:${TW}px;height:${TH}px;background:#0b1220 url('assets/${ii.file}') center/cover no-repeat"></div>`;
    slides += `<div style="position:absolute;left:${i * AW}px;top:0;width:${AW}px;height:${MH}px;overflow:hidden;background:${bgOf(it)}"><div id="z${i}" class="zoom">${media(it, "m" + i, 0, D, A)}</div></div>`;
  });
  js += `gsap.set(".thumb",{boxShadow:"0 0 0 0px #0066ff, 0 2px 6px rgba(17,17,17,0.18)"});
tl.fromTo("#c",{opacity:0,y:40},{opacity:1,y:0,duration:0.55,ease:"power3.out"},0);
tl.fromTo(".thumb",{opacity:0,y:-24},{opacity:0.5,y:0,duration:0.45,ease:"power3.out",stagger:0.06},0.15);\n`;
  s.items.forEach((it, i) => {
    const t = Math.max(it.rel, i === 0 ? 0.6 : it.rel), segEnd = i < n - 1 ? s.items[i + 1].rel : D;
    if (i > 0) js += `tl.to("#trk",{x:${-i * AW},duration:0.8,ease:"power3.inOut"},${r2(it.rel)});\ntl.to("#t${i - 1}",{opacity:0.5,scale:1,boxShadow:"0 0 0 0px #0066ff, 0 2px 6px rgba(17,17,17,0.18)",duration:0.4},${r2(it.rel)});\n`;
    js += `tl.to("#t${i}",{opacity:1,scale:1.12,boxShadow:"0 0 0 3px #0066ff, 0 6px 16px rgba(17,17,17,0.28)",duration:0.4},${r2(t)});\n`;
    js += `tl.fromTo("#z${i}",{scale:1},{scale:1.05,duration:${r2(segEnd - it.rel + 0.8)},ease:"none"},${r2(it.rel)});\n`;
  });
  const last = s.items[n - 1].rel;
  if (D - last > 3) js += `tl.to(".thumb",{opacity:0,y:-16,duration:0.4,stagger:0.03,ease:"power2.in"},${r2(last + 1.4)});\n`;
  js += `tl.to("#c",{opacity:0,duration:0.35,ease:"power2.in"},${r2(D - 0.35)});`;
  const html = `${thumbs}<div id="c" class="card" style="left:${AX}px;top:${MT}px;width:${AW}px;height:${MH}px"><div id="trk" style="position:absolute;left:0;top:0;width:${n * AW}px;height:${MH}px">${slides}</div></div>`;
  return { html, js };
};

B.deck = (s, A) => {
  const D = s.dur, W = 1040, H = 693, P = 14, L = CX - (W + 2 * P) / 2, T = CY - (H + 2 * P) / 2;
  const rot = [-4, 3.5, -2, 5, -3], off = [[-26, 8], [22, -12], [-8, 6], [18, -6], [-14, 10]];
  let html = "", js = "";
  s.items.forEach((it, i) => {
    html += `<div id="d${i}" class="pol" style="left:${L}px;top:${T}px;width:${W + 2 * P}px;height:${H + 2 * P}px;padding:${P}px"><div class="polin" style="width:${W}px;height:${H}px"><div id="z${i}" class="zoom">${media(it, "m" + i, 0, D, A, true)}</div></div></div>`;
    js += `tl.fromTo("#d${i}",{y:-1150,x:${off[i][0]},rotation:${rot[i] - 16}},{y:${off[i][1]},rotation:${rot[i]},duration:0.9,ease:"back.out(1.25)"},${r2(it.rel)});\n`;
    if (i > 0) js += `tl.to("#d${i - 1}",{x:${off[i - 1][0] - 34},rotation:${rot[i - 1] - 3},duration:0.6,ease:"power2.out"},${r2(it.rel + 0.35)});\n`;
    js += `tl.fromTo("#z${i}",{scale:1},{scale:1.05,duration:${r2(D - it.rel)},ease:"none"},${r2(it.rel)});\n`;
  });
  js += `tl.to(".pol",{opacity:0,duration:0.4,ease:"power2.in"},${r2(D - 0.4)});`;
  return { html, js };
};

B.stack = (s, A) => {
  const D = s.dur, n = s.items.length;
  let cards = "", js = "";
  s.items.forEach((it, i) => {
    const next = i < n - 1 ? s.items[i + 1].rel : D;
    cards += `<div id="k${i}" class="card" style="left:0;top:${AY}px;width:${AW}px;height:${AH}px;background:${bgOf(it)}"><div id="z${i}" class="zoom">${media(it, "m" + i, it.rel, (it.vid ? Math.min(next - it.rel + 0.8, D - it.rel) : D), A)}</div><div id="h${i}" class="shade"></div></div>`;
    js += `gsap.set("#k${i}",{transformOrigin:"50% 0%"});\n`;
    js += `tl.fromTo("#k${i}",{y:820},{y:0,duration:0.7,ease:"power3.out"},${r2(it.rel)});\n`;
    for (let j = Math.max(0, i - 2); j < i; j++) {
      const d = i - j;
      js += `tl.to("#k${j}",{scale:${r2(1 - 0.06 * d)},y:${-22 * d},duration:0.7,ease:"power3.out"},${r2(it.rel)});\n`;
      js += `tl.to("#h${j}",{opacity:${r2(Math.min(0.35 * d, 0.6))},duration:0.7,ease:"power2.out"},${r2(it.rel)});\n`;
    }
    if (!it.vid) {
      js += `gsap.set("#z${i}",{transformOrigin:"${it.focus || "50% 50%"}"});\n`;
      js += `tl.fromTo("#z${i}",{scale:${it.z0 || 1.6}},{scale:1,duration:1.4,ease:"power3.inOut"},${r2(it.rel + 0.75)});\n`;
      const pushT = it.rel + 2.15, pushD = next - pushT;
      if (pushD > 0.5) js += `tl.to("#z${i}",{scale:1.035,duration:${r2(pushD)},ease:"none"},${r2(pushT)});\n`;
    }
  });
  js += `tl.to("#stage",{opacity:0,duration:0.35,ease:"power2.in"},${r2(D - 0.35)});`;
  const html = `<div id="stage" style="position:absolute;left:${AX}px;top:0;width:${AW}px;height:${AY + AH + 20}px;overflow:hidden">${cards}</div>`;
  return { html, js };
};

B.feature = (s, A) => {
  const D = s.dur, cards = s.cards, n = cards.length, W = 1040, H = 693, L = AW / 2 - W / 2, T = AY + AH / 2 - H / 2;
  const pos = (k) => ({ x: k * 620, scale: k === 0 ? 1 : 0.74, rotationY: -k * 24, opacity: k === 0 ? 1 : Math.abs(k) === 1 ? 0.55 : 0, filter: `blur(${k === 0 ? 0 : 4}px)`, zIndex: k === 0 ? 3 : Math.abs(k) === 1 ? 2 : 1 });
  const kOf = (i, a) => { let k = (((i - a) % n) + n) % n; if (k > n / 2) k -= n; return k; };
  // each card's video (if any) plays while that card is in front
  let html = "", js = "";
  cards.forEach((c, i) => {
    const item = typeof c === "string" ? { img: c } : c;
    const turns = s.items.filter((x) => x.card === i);
    let inner = "";
    if (item.vid) {
      A.add(`vid/${item.vid}.mp4`); A.add(`vid/${item.poster}`);
      inner = `<img class="m" src="assets/${item.poster}" style="object-fit:cover" alt="" />`;
      turns.forEach((tn, q) => {
        const idx = s.items.indexOf(tn), next = idx < s.items.length - 1 ? s.items[idx + 1].rel : D;
        inner += `<video id="v${i}_${q}" class="m" src="assets/${item.vid}.mp4" muted playsinline data-start="${r2(tn.rel)}" data-duration="${r2(Math.min(next - tn.rel + 0.4, D - tn.rel))}" data-media-start="${item.mediaStart || 0}" style="object-fit:cover"></video>`;
      });
    } else inner = media(item, "m" + i, 0, D, A);
    html += `<div id="f${i}" class="card" style="left:${L}px;top:${T}px;width:${W}px;height:${H}px;background:${bgOf(item)}">${inner}</div>`;
    const p = pos(kOf(i, s.items[0].card));
    js += `gsap.set("#f${i}",${JSON.stringify(p)});\n`;
  });
  js += `tl.fromTo("#fc",{opacity:0,scale:0.96},{opacity:1,scale:1,duration:0.5,ease:"power3.out"},0);\n`;
  s.items.forEach((it, q) => {
    if (q === 0) return;
    cards.forEach((_, i) => { js += `tl.to("#f${i}",{...${JSON.stringify(pos(kOf(i, it.card)))},duration:0.8,ease:"power3.inOut"},${r2(Math.max(0, it.rel - 0.3))});\n`; });
  });
  js += `tl.to("#fc",{opacity:0,duration:0.4,ease:"power2.in"},${r2(D - 0.4)});`;
  return { html: `<div id="fc" style="position:absolute;left:${AX}px;top:0;width:${AW}px;height:${AY + AH + 20}px;overflow:hidden;perspective:1800px">${html}</div>`, js };
};

B.cylinder = (s, A) => {
  const D = s.dur, N = s.faces.length, TH = 360 / N, FW = 250, FH = 167, R = Math.round((N * 270) / (2 * Math.PI)), PW = 1100, PH = 733;
  let faces = "", pops = "";
  s.faces.forEach((f, i) => {
    const ii = imgInfo(f); A.add(`img/${ii.file}`);
    faces += `<div class="face" style="left:${-FW / 2}px;top:${-FH / 2}px;width:${FW}px;height:${FH}px;transform:rotateY(${r2(i * TH)}deg) translateZ(${R}px);background:#0b1220 url('assets/${ii.file}') center/cover no-repeat"></div>`;
  });
  s.picks.forEach((p, j) => { pops += `<div id="pp${j}" class="zoom" style="background:${bgOf({ img: s.faces[p.face] })}">${media({ img: s.faces[p.face] }, "pm" + j, 0, D, A, true)}</div>`; });
  const W_ = -20; // degrees per second, constant spin
  let js = `gsap.set("#cy",{filter:"blur(0px)"});gsap.set("[id^=pp]",{opacity:0});
tl.fromTo("#cy",{opacity:0},{opacity:1,duration:0.6,ease:"power2.out"},0);\n`;
  let r = 0, tc = 0;
  s.picks.forEach((p, j) => {
    const settle = p.rel - 1.1;
    if (settle > tc + 0.05) { const r1 = r + W_ * (settle - tc); js += `tl.to("#ring",{rotationY:${r2(r1)},duration:${r2(settle - tc)},ease:"none"},${r2(tc)});\n`; r = r1; tc = settle; }
    const m = ((((r - 25 + p.face * TH) % 360) + 360) % 360), target = r - 25 - m;
    js += `tl.to("#ring",{rotationY:${r2(target)},duration:1.1,ease:"power3.out"},${r2(tc)});\n`;
    r = target; tc = p.rel;
    js += `tl.set("#pp${j}",{opacity:1},${r2(p.rel)});\n`;
    js += `tl.fromTo("#pop",{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.55,ease:"back.out(1.2)",immediateRender:${j === 0}},${r2(p.rel)});\n`;
    js += `tl.to("#cy",{opacity:0.28,filter:"blur(3px)",duration:0.5,ease:"power2.out"},${r2(p.rel)});\n`;
    const nx = s.picks[j + 1];
    if (nx) {
      const rel = Math.max(p.rel + 1.2, nx.rel - 2.0);
      js += `tl.to("#pop",{opacity:0,scale:0.5,duration:0.4,ease:"power2.in"},${r2(rel)});\n`;
      js += `tl.set("#pp${j}",{opacity:0},${r2(rel + 0.4)});\n`;
      js += `tl.to("#cy",{opacity:1,filter:"blur(0px)",duration:0.4,ease:"power2.out"},${r2(rel)});\n`;
      tc = rel + 0.4;
    }
  });
  js += `tl.to("#pop",{opacity:0,duration:0.4,ease:"power2.in"},${r2(D - 0.4)});\ntl.to("#cy",{opacity:0,duration:0.4,ease:"power2.in"},${r2(D - 0.4)});`;
  const html = `<div id="cy" style="position:absolute;left:${AX}px;top:0;width:${AW}px;height:${AY + AH + 20}px;overflow:hidden;perspective:1400px"><div id="ring" style="position:absolute;left:${AW / 2}px;top:${AY + AH / 2}px;width:0;height:0;transform-style:preserve-3d">${faces}</div></div>
<div id="pop" class="card" style="left:${CX - PW / 2}px;top:${CY - PH / 2}px;width:${PW}px;height:${PH}px">${pops}</div>`;
  return { html, js };
};

B.quote = (s) => {
  const D = s.dur, words = s.quote.split(" ");
  const hl = new Set(s.hl || []);
  const wHtml = words.map((w, i) => `<span class="wm"><span class="w${hl.has(w) ? " hl" : ""}">${esc(w)}</span></span>`).join(" ");
  const html = `<div style="position:absolute;left:${AX}px;top:${AY}px;width:${AW}px;height:${AH}px;display:flex;align-items:center;justify-content:center"><div id="q" class="qcard"><div class="qm">&ldquo;</div><div id="qt" class="qt">${wHtml}</div><div id="qs" class="qs">${esc(s.source)}</div></div></div>`;
  const wordsEnd = 0.35 + words.length * 0.035 + 0.5;
  const js = `tl.fromTo("#q",{opacity:0,y:24},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0);
tl.fromTo("#qt .w",{yPercent:110},{yPercent:0,duration:0.5,ease:"power3.out",stagger:0.035},0.35);
tl.to("#qt .hl",{color:"#0066ff",duration:0.5,ease:"power2.out",stagger:0.08},${r2(wordsEnd + 0.3)});
tl.fromTo("#qs",{opacity:0,y:10},{opacity:1,y:0,duration:0.4,ease:"power3.out"},${r2(wordsEnd)});
tl.to("#q",{opacity:0,duration:0.35,ease:"power2.in"},${r2(D - 0.35)});`;
  return { html, js };
};

B.callout = (c) => {
  const D = c.dur, words = c.head.split(" ");
  const px = c.head.length <= 12 ? 80 : c.head.length <= 24 ? 64 : c.head.length <= 40 ? 54 : 46;
  const cls = c.type === "stat" ? "stat" : c.type === "quote" ? "quote" : "";
  const wHtml = words.map((w) => `<span class="wm"><span class="w">${esc(w)}</span></span>`).join(" ");
  const html = `<div style="position:absolute;left:40px;top:790px;width:1060px;height:260px;display:flex;align-items:flex-end;padding-bottom:18px"><div id="co" class="cocard">${c.tag ? `<div class="cotag">${esc(c.tag)}</div>` : ""}<div id="coh" class="coh ${cls}" style="font-size:${px}px">${wHtml}</div>${c.label ? `<div id="col" class="col">${esc(c.label)}</div>` : ""}</div></div>`;
  const js = `tl.fromTo("#co",{opacity:0,y:14},{opacity:1,y:0,duration:0.35,ease:"power3.out"},0);
tl.fromTo("#coh .w",{yPercent:110},{yPercent:0,duration:0.45,ease:"power3.out",stagger:0.06},0.1);
${c.label ? `tl.fromTo("#col",{opacity:0,y:8},{opacity:1,y:0,duration:0.35,ease:"power3.out"},${r2(0.3 + words.length * 0.06)});` : ""}
tl.to("#co",{opacity:0,duration:0.3,ease:"power2.in"},${r2(D - 0.3)});`;
  return { html, js };
};

// ---------- page shell ----------
const CSS = `@font-face{font-family:"Montserrat";font-weight:400;src:url("assets/fonts/Montserrat-Regular.ttf")}
@font-face{font-family:"Montserrat";font-weight:600;src:url("assets/fonts/Montserrat-SemiBold.ttf")}
@font-face{font-family:"Montserrat";font-weight:700;src:url("assets/fonts/Montserrat-Bold.ttf")}
@font-face{font-family:"Montserrat";font-weight:900;src:url("assets/fonts/Montserrat-Black.ttf")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:transparent}
#root{position:relative;width:100%;height:100%;overflow:hidden}
.card{position:absolute;border-radius:22px;overflow:hidden;border:1px solid #d9e1ee;box-shadow:0 10px 32px rgba(17,17,17,0.16);background:#0b1220}
.m{position:absolute;left:0;top:0;width:100%;height:100%;display:block}
.zoom{position:absolute;left:0;top:0;width:100%;height:100%;overflow:hidden}
.shade{position:absolute;left:0;top:0;width:100%;height:100%;background:#0b1220;opacity:0}
.thumb{position:absolute;border-radius:10px;overflow:hidden;border:2px solid #ffffff;background:#0b1220}
.pol{position:absolute;background:#ffffff;border-radius:8px;box-shadow:0 14px 36px rgba(17,17,17,0.22)}
.polin{position:relative;overflow:hidden;border-radius:4px}
.face{position:absolute;border-radius:12px;overflow:hidden;box-shadow:0 8px 22px rgba(17,17,17,0.2);background:#0b1220}
.wm{display:inline-block;overflow:hidden;vertical-align:bottom;padding-bottom:0.08em}
.w{display:inline-block}
.qt .wm,.coh.quote .wm{padding-right:0.14em;margin-right:-0.14em}
.qcard{width:1180px;padding:54px 64px 50px 64px;background:#ffffff;border:1px solid #d9e1ee;border-radius:22px;box-shadow:0 10px 32px rgba(17,17,17,0.14)}
.qm{font-family:"Montserrat",sans-serif;font-weight:900;font-size:140px;line-height:0.7;color:#0066ff;height:62px}
.qt{font-family:"Montserrat",sans-serif;font-weight:600;font-style:italic;font-size:48px;line-height:1.22;letter-spacing:-0.02em;color:#111111;margin-top:18px}
.qs{font-family:"Montserrat",sans-serif;font-weight:700;font-size:28px;letter-spacing:0.06em;text-transform:uppercase;color:#3b4252;margin-top:28px}
.cocard{max-width:1000px;padding:26px 36px 28px 36px;background:#ffffff;border:1px solid #d9e1ee;border-radius:22px;box-shadow:0 8px 28px rgba(17,17,17,0.12)}
.cotag{font-family:"Montserrat",sans-serif;font-weight:700;font-size:28px;letter-spacing:0.1em;text-transform:uppercase;color:#0066ff;margin-bottom:10px}
.coh{font-family:"Montserrat",sans-serif;font-weight:700;letter-spacing:-0.03em;line-height:1.1;color:#111111}
.coh.stat{color:#0066ff;font-weight:900}
.coh.quote{font-weight:600;font-style:italic}
.col{font-family:"Montserrat",sans-serif;font-weight:400;font-size:30px;line-height:1.25;color:#3b4252;margin-top:12px}`;

const page = (id, title, body, js, dur) => `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>${esc(title)}</title>
    <!-- Generated by gen.mjs. Do not hand-edit: change the plan in gen.mjs and regenerate. -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>${CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="${id}" data-start="0" data-width="1920" data-height="1080" data-duration="${dur}">
${body}
    </div>
    <script>
const tl = gsap.timeline({ paused: true });
${js}
window.__timelines["${id}"] = tl;
    </script>
  </body>
</html>
`;

// ---------- write everything ----------
fs.rmSync(OUTDIR, { recursive: true, force: true });
fs.mkdirSync(OUTDIR, { recursive: true });
const manifest = [];
function emit(id, title, start, dur, built, assets, track) {
  const dir = path.join(OUTDIR, id);
  fs.mkdirSync(path.join(dir, "assets", "fonts"), { recursive: true });
  for (const f of fs.readdirSync(path.join(SRC, "fonts"))) fs.copyFileSync(path.join(SRC, "fonts", f), path.join(dir, "assets", "fonts", f));
  for (const a of assets) {
    const from = a.startsWith("img/") ? path.join(LOOKUP, a.slice(4)) : path.join(SRC, a);
    fs.copyFileSync(from, path.join(dir, "assets", path.basename(a)));
  }
  // Pad the timeline to the exact length so the render is exactly `dur` seconds.
  const js = `${built.js}\ntl.set({}, {}, ${r2(dur)});`;
  fs.writeFileSync(path.join(dir, "index.html"), page(id, title, built.html, js, r2(dur)));
  manifest.push({ id, title, start: r2(start), dur: r2(dur), frame: 86400 + Math.round(start * FPS), track });
}

for (const s of SCENES) {
  const start = s.start ?? Math.min(...(s.items || s.picks).map((x) => x.t));
  s.dur = s.end - start;
  for (const x of s.items || []) x.rel = x.t - start;
  for (const x of s.picks || []) x.rel = x.t - start;
  const A = new Set();
  const built = B[s.type](s, A);
  emit(s.id, `${s.id} ${s.type}`, start, s.dur, built, A, "scene");
}
CALLOUTS.forEach((c, i) => {
  const words = c.head.split(" ").length + (c.label ? c.label.split(" ").length : 0);
  let dur = Math.min(Math.max(3, 1 + 0.3 * words), 6);
  const next = CALLOUTS[i + 1];
  if (next) dur = Math.min(dur, next.t - c.t - 0.2);
  c.dur = r2(dur);
  emit(`co-${c.id.toLowerCase()}`, `${c.id} ${c.head}`, c.t, c.dur, B.callout(c), new Set(), "callout");
});
fs.writeFileSync(path.join(HERE, "scenes.json"), JSON.stringify(manifest, null, 1));
console.log(`scenes ${SCENES.length}, callouts ${CALLOUTS.length}, written to ${OUTDIR}`);
