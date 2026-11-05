"""Tests for script_lock.py. Run: python3 -m unittest test_script_lock (from current/)."""
import unittest

from script_lock import check, is_redo


def mk(seq):
    return [{"text": t, "start": s, "end": e, "type": "word"} for t, s, e in seq]


def say(text, t0, step=0.4, dur=0.3):
    out, t = [], t0
    for w in text.split():
        out.append((w, round(t, 3), round(t + dur, 3)))
        t += step
    return out


def kinds(res):
    return [f["kind"] for f in res["findings"]]


class ScriptLock(unittest.TestCase):
    def test_clean_cut_passes(self):
        words = mk(say("we start here and finish there", 0))
        res = check(words, [{"start": 0, "end": 2.4}], 2.4)
        self.assertTrue(res["passed"])
        self.assertEqual(res["spans"], [])

    def test_redo_with_cue_passes_without_sign_off(self):
        words = mk(say("So the plan is redo", 0) + say("So the plan is simple", 3.0))
        res = check(words, [{"start": 2.9, "end": 5.0}], 5.0)
        self.assertTrue(res["passed"], res["findings"])
        self.assertEqual(res["spans"][0]["decision"], "redo")

    def test_repeated_redos_pass(self):
        words = mk(say("We open with a redo", 0) + say("We open with a redo", 3.0)
                   + say("We open with the ask", 6.0))
        res = check(words, [{"start": 5.9, "end": 8.1}], 8.1)
        self.assertTrue(res["passed"], res["findings"])

    def test_filler_cut_without_sign_off_fails(self):
        words = mk([("so", 0, 0.3), ("um", 0.4, 0.7), ("the", 0.8, 1.1), ("point", 1.2, 1.5)])
        rs = [{"start": 0, "end": 0.35}, {"start": 0.75, "end": 1.6}]
        res = check(words, rs, 1.6)
        self.assertFalse(res["passed"])
        self.assertIn("unauthorised_cut", kinds(res))

    def test_filler_cut_with_andrews_words_passes(self):
        words = mk([("so", 0, 0.3), ("um", 0.4, 0.7), ("the", 0.8, 1.1), ("point", 1.2, 1.5)])
        rs = [{"start": 0, "end": 0.35}, {"start": 0.75, "end": 1.6}]
        auth = [{"start": 0.35, "end": 0.75, "authorised_by": "Andrew", "quote": "drop the um"}]
        res = check(words, rs, 1.6, auth)
        self.assertTrue(res["passed"], res["findings"])
        self.assertEqual(res["spans"][0]["decision"], "authorised")

    def test_dead_air_needs_sign_off(self):
        words = mk([("first", 0, 0.3), ("point", 0.4, 0.7), ("second", 6.0, 6.3), ("point", 6.4, 6.7)])
        rs = [{"start": 0, "end": 0.8}, {"start": 5.9, "end": 6.8}]
        self.assertIn("unauthorised_cut", kinds(check(words, rs, 6.8)))
        auth = [{"start": 0.8, "end": 5.9, "authorised_by": "Andrew", "quote": "trim that gap"}]
        self.assertTrue(check(words, rs, 6.8, auth)["passed"])

    def test_short_silence_is_join_padding(self):
        words = mk([("a", 0, 0.3), ("b", 0.7, 1.0)])
        res = check(words, [{"start": 0, "end": 0.4}, {"start": 0.6, "end": 1.1}], 1.1)
        self.assertTrue(res["passed"], res["findings"])
        self.assertEqual(res["spans"][0]["decision"], "splice")

    def test_cut_inside_a_word_fails(self):
        words = mk([("hello", 0, 0.5)])
        res = check(words, [{"start": 0, "end": 0.25}], 0.5)
        self.assertIn("cut_inside_word", kinds(res))

    def test_reordered_ranges_fail(self):
        words = mk(say("one two three four five six", 0))
        res = check(words, [{"start": 1.9, "end": 2.4}, {"start": 0, "end": 1.0}], 2.4)
        self.assertIn("out_of_order", kinds(res))

    def test_authorisation_without_andrews_words_fails(self):
        words = mk([("a", 0, 0.3)])
        res = check(words, [{"start": 0, "end": 0.35}], 0.35,
                    [{"start": 0, "end": 1, "authorised_by": "Andrew", "quote": ""}])
        self.assertIn("bad_authorisation", kinds(res))

    def test_redo_rules(self):
        self.assertTrue(is_redo(["redo"], ["We", "open"])[0])
        self.assertTrue(is_redo(["We", "open", "with", "a"], ["We", "open", "with", "the"])[0])
        self.assertFalse(is_redo(["We", "open", "the"], ["We", "open", "with"])[0])
        self.assertFalse(is_redo(["um"], ["the", "point"])[0])


if __name__ == "__main__":
    unittest.main()
