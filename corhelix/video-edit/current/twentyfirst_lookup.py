#!/usr/bin/env python3
"""21st.dev lookup for HTML callouts that are not Hyperframes templates (SOP: Beats to callouts).

Talks to the 21st MCP server (https://21st.dev/api/mcp, Streamable HTTP, key in an x-api-key header).
Verified 5 Nov 2026 against the server's own tools/list: `search` (free metadata), `video_search_blocks`
(video blocks with props schemas), `get_component` (code, by id). `generate` is not used: it spends AI
credits.

  twentyfirst_lookup.py search "animated stat counter" [--type component|theme|template|all] [--limit 5]
  twentyfirst_lookup.py video-blocks "lower third" [--size 16:9] [--kind overlay-fx]
  twentyfirst_lookup.py get 1844 [--out component.tsx]
  twentyfirst_lookup.py record --layer-id C2 (--slug author/name | --component-id 1844)

Every search and get is appended to <project>/layers/21st-lookups.jsonl. `record` writes
design_ref {source, slug, component_id, query, checked_at} onto the layer row in layers/layers.json, and
refuses a slug or id that no lookup in the log returned. The /video-edit gate then accepts the callout.

Key: TWENTYFIRST_API_KEY if set, else decrypted in-process from the secrets vault
(secrets/internal/21st-dev.enc.env, variable 21ST_DEV_KEY; vault folder from VIDEO_EDIT_VAULT or
~/Documents/CLEAN/secrets-vault). It is never printed or written.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

URL = "https://21st.dev/api/mcp"
VAULT_FILE = "secrets/internal/21st-dev.enc.env"
VAULT_VAR = "21ST_DEV_KEY"
UA = "corhelix-video-edit/1.0"


def get_key():
    k = os.environ.get("TWENTYFIRST_API_KEY")
    if k:
        return k
    vault = pathlib.Path(os.environ.get("VIDEO_EDIT_VAULT") or pathlib.Path.home() / "Documents" / "CLEAN" / "secrets-vault")
    r = subprocess.run(["sops", "-d", "--input-type", "dotenv", "--output-type", "dotenv", str(vault / VAULT_FILE)],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("could not decrypt the 21st.dev key from the vault: %s" % r.stderr.strip()[:200])
    for line in r.stdout.splitlines():
        if line.startswith(VAULT_VAR + "="):
            return line.split("=", 1)[1]
    raise SystemExit("%s not found in %s" % (VAULT_VAR, VAULT_FILE))


def _network_post(key, sid, body):
    h = {"content-type": "application/json", "accept": "application/json, text/event-stream",
         "x-api-key": key, "user-agent": UA}
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=h, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=40)
        return r.read().decode(), r.headers.get("mcp-session-id")
    except urllib.error.HTTPError as e:
        raise SystemExit("21st.dev returned HTTP %d: %s" % (e.code, e.read().decode()[:200]))


def _body(text):
    for line in text.splitlines():
        if line.startswith("data:"):
            text = line[5:].strip()
            break
    return json.loads(text)


class Client:
    def __init__(self, key, post=None):
        self.key, self.sid, self.n = key, None, 0
        self._post = post or (lambda sid, body: _network_post(self.key, sid, body))
        self._ready = False

    def _rpc(self, method, params=None, notify=False):
        self.n += 1
        body = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            body["params"] = params
        if not notify:
            body["id"] = self.n
        text, sid = self._post(self.sid, body)
        self.sid = sid or self.sid
        return None if notify or not text.strip() else _body(text)

    def call(self, tool, args):
        if not self._ready:
            self._rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                     "clientInfo": {"name": "corhelix-video-edit", "version": "1.0"}})
            self._rpc("notifications/initialized", notify=True)
            self._ready = True
        res = self._rpc("tools/call", {"name": tool, "arguments": args})
        if res.get("error"):
            raise SystemExit("21st.dev error: %s" % str(res["error"])[:200])
        out = res["result"]
        if out.get("isError"):
            raise SystemExit("21st.dev tool error: %s" % str(out.get("content"))[:300])
        return out


def slug_of(r):
    if r.get("ref"):
        return r["ref"]
    m = re.search(r"/components/([^/?#]+)", r.get("url", "") or "")
    if m and r.get("author"):
        return "%s/%s" % (r["author"], m.group(1))
    return str(r.get("id", ""))


def brief(r):
    return {"id": r.get("id"), "slug": slug_of(r), "name": r.get("name"), "author": r.get("author"),
            "url": r.get("url"), "preview": r.get("previewUrl")}


def parse_search(out):
    return [brief(r) for r in (out.get("structuredContent") or {}).get("results", [])]


def parse_video_blocks(out):
    try:
        blocks = json.loads(out["content"][0]["text"]).get("blocks", [])
    except (KeyError, IndexError, ValueError):
        blocks = []
    return [{"id": None, "slug": b["ref"], "name": b.get("name"), "kind": b.get("kind"), "sizes": b.get("sizes")} for b in blocks]


def log_path(project):
    return pathlib.Path(project) / "layers" / "21st-lookups.jsonl"


def append_log(project, entry):
    p = log_path(project)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_log(project):
    out = []
    try:
        for line in log_path(project).read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    except OSError:
        pass
    return out


def find_in_log(entries, slug=None, cid=None):
    """The newest logged result matching the slug or id, with the query that found it."""
    for e in reversed(entries):
        for r in e.get("results", []):
            if (slug and r.get("slug") == slug) or (cid is not None and str(r.get("id")) == str(cid)):
                return dict(r, query=e.get("query"))
    return None


def callout_rows(layers):
    if isinstance(layers, dict):
        return layers.get("callouts", []) + layers.get("layers", [])
    return layers or []


def apply_record(layers, layer_id, hit, now):
    for row in callout_rows(layers):
        if row.get("id") == layer_id:
            row["design_ref"] = {"source": "21st.dev", "slug": hit["slug"], "component_id": hit.get("id"),
                                 "query": hit.get("query"), "checked_at": now}
            return row
    raise SystemExit("no layer row with id %r in layers.json" % layer_id)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--project", default=".", help="project folder (default: the current folder)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--type", default="component", choices=["component", "theme", "template", "all"]); s.add_argument("--limit", type=int, default=5)
    v = sub.add_parser("video-blocks"); v.add_argument("query"); v.add_argument("--size", choices=["16:9", "9:16", "1:1"]); v.add_argument("--kind")
    g = sub.add_parser("get"); g.add_argument("id", type=int); g.add_argument("--out")
    r = sub.add_parser("record"); r.add_argument("--layer-id", required=True); r.add_argument("--slug"); r.add_argument("--component-id"); r.add_argument("--layers")
    a = p.parse_args(argv)
    now = time.strftime("%Y-%m-%dT%H:%M:%S")

    if a.cmd == "record":
        if not (a.slug or a.component_id):
            raise SystemExit("record needs --slug or --component-id")
        hit = find_in_log(read_log(a.project), a.slug, a.component_id)
        if not hit:
            raise SystemExit("no lookup in %s returned that slug or id. Search first." % log_path(a.project))
        lp = pathlib.Path(a.layers) if a.layers else pathlib.Path(a.project) / "layers" / "layers.json"
        layers = json.loads(lp.read_text(encoding="utf-8"))
        apply_record(layers, a.layer_id, hit, now)
        lp.write_text(json.dumps(layers, indent=1), encoding="utf-8")
        print("recorded design_ref on %s: %s" % (a.layer_id, hit["slug"]))
        return 0

    c = Client(get_key())
    if a.cmd == "search":
        res = parse_search(c.call("search", {"query": a.query, "type": a.type, "limit": a.limit}))
        append_log(a.project, {"at": now, "tool": "search", "query": a.query, "results": res})
    elif a.cmd == "video-blocks":
        args = {"query": a.query}
        if a.size: args["size"] = a.size
        if a.kind: args["kind"] = a.kind
        res = parse_video_blocks(c.call("video_search_blocks", args))
        append_log(a.project, {"at": now, "tool": "video_search_blocks", "query": a.query, "results": res})
    else:
        out = c.call("get_component", {"id": a.id})
        text = "\n".join(x.get("text", "") for x in out.get("content", []) if x.get("type") == "text")
        append_log(a.project, {"at": now, "tool": "get_component", "query": "get %d" % a.id, "results": [{"id": a.id, "slug": str(a.id)}]})
        if a.out:
            pathlib.Path(a.out).write_text(text, encoding="utf-8")
            print("wrote %d characters to %s" % (len(text), a.out))
        else:
            print(text)
        return 0
    for x in res:
        print("[%s] %s | slug %s | %s" % (x.get("id") if x.get("id") is not None else "block", x.get("name"), x["slug"], x.get("url") or x.get("preview") or ""))
    if not res:
        print("no results")
    return 0


if __name__ == "__main__":
    sys.exit(main())
