"""Tests for twentyfirst_lookup.py. No network: the client takes a fake transport.
Run from current/: python3 -m unittest test_twentyfirst_lookup"""
import json
import unittest

import twentyfirst_lookup as t

SEARCH = {"result": {"structuredContent": {"results": [
    {"type": "component", "id": 1844, "name": "Animated Counter", "author": "preetsuthar17",
     "url": "https://21st.dev/@preetsuthar17/components/animated-counter", "previewUrl": "https://x/p.png"}]}}}
BLOCKS = {"result": {"content": [{"type": "text", "text": json.dumps({"blocks": [
    {"ref": "mg-realty-agent", "name": "Meet Your Agent", "kind": "scene", "sizes": ["16:9"]}]})}]}}


def fake(replies):
    seen = []
    def post(sid, body):
        seen.append(body)
        if body["method"] == "initialize":
            return json.dumps({"jsonrpc": "2.0", "id": body["id"], "result": {}}), "sess-1"
        if body["method"] == "notifications/initialized":
            return "", None
        return "event: message\ndata: " + json.dumps(dict(replies[body["params"]["name"]], jsonrpc="2.0", id=body["id"])) + "\n\n", None
    return post, seen


class Lookup(unittest.TestCase):
    def test_slug_comes_from_author_and_url(self):
        self.assertEqual(t.slug_of(SEARCH["result"]["structuredContent"]["results"][0]), "preetsuthar17/animated-counter")
        self.assertEqual(t.slug_of({"ref": "mg-x"}), "mg-x")
        self.assertEqual(t.slug_of({"id": 9}), "9")

    def test_search_and_block_parsing(self):
        self.assertEqual(t.parse_search(SEARCH["result"])[0]["id"], 1844)
        self.assertEqual(t.parse_video_blocks(BLOCKS["result"])[0]["slug"], "mg-realty-agent")
        self.assertEqual(t.parse_video_blocks({"content": [{"type": "text", "text": "not json"}]}), [])

    def test_client_initialises_once_and_keeps_the_session(self):
        post, seen = fake({"search": SEARCH})
        c = t.Client("k", post)
        c.call("search", {"query": "x"}); c.call("search", {"query": "y"})
        self.assertEqual([b["method"] for b in seen], ["initialize", "notifications/initialized", "tools/call", "tools/call"])
        self.assertEqual(c.sid, "sess-1")

    def test_record_needs_a_real_lookup(self):
        log = [{"query": "counter", "results": t.parse_search(SEARCH["result"])}]
        self.assertIsNone(t.find_in_log(log, slug="made/up"))
        hit = t.find_in_log(log, slug="preetsuthar17/animated-counter")
        self.assertEqual(hit["query"], "counter")
        self.assertEqual(t.find_in_log(log, cid="1844")["id"], 1844)

    def test_record_writes_design_ref_on_a_callout_row(self):
        layers = {"slides": [], "callouts": [{"id": "C2", "type": "custom"}]}
        row = t.apply_record(layers, "C2", {"slug": "a/b", "id": 7, "query": "q"}, "2026-11-05T10:00:00")
        self.assertEqual(layers["callouts"][0]["design_ref"]["source"], "21st.dev")
        self.assertEqual(row["design_ref"]["slug"], "a/b")
        with self.assertRaises(SystemExit):
            t.apply_record(layers, "C9", {"slug": "a/b"}, "now")


if __name__ == "__main__":
    unittest.main()
