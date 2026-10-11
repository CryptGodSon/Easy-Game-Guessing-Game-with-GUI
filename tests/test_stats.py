"""Unit tests for persistent statistics."""

import json
import tempfile
import unittest
from pathlib import Path

from stats import Stats


class StatsTest(unittest.TestCase):
    """Tests for Stats."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.path = Path(self._tmp.name) / "stats.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_when_file_missing(self):
        stats = Stats(self.path)
        self.assertEqual((stats.played, stats.won, stats.best), (0, 0, {}))
        self.assertEqual(stats.win_rate, 0)

    def test_record_and_reload(self):
        stats = Stats(self.path)
        stats.record_game("easy", won=True, attempts=4)
        stats.record_game("easy", won=False, attempts=5)
        stats.language = "pl"
        stats.save()

        loaded = Stats(self.path)
        self.assertEqual((loaded.played, loaded.won), (2, 1))
        self.assertEqual(loaded.best, {"easy": 4})
        self.assertEqual(loaded.win_rate, 50)
        self.assertEqual(loaded.language, "pl")

    def test_new_record_only_when_beating_previous_best(self):
        stats = Stats(self.path)
        self.assertFalse(stats.record_game("hard", won=True, attempts=6))
        self.assertFalse(stats.record_game("hard", won=True, attempts=7))
        self.assertTrue(stats.record_game("hard", won=True, attempts=3))
        self.assertEqual(stats.best["hard"], 3)

    def test_lost_game_does_not_set_best(self):
        stats = Stats(self.path)
        stats.record_game("easy", won=False, attempts=5)
        self.assertEqual(stats.best, {})

    def test_reset_keeps_language(self):
        stats = Stats(self.path)
        stats.language = "pl"
        stats.record_game("easy", won=True, attempts=2)
        stats.reset()
        loaded = Stats(self.path)
        self.assertEqual((loaded.played, loaded.won, loaded.best), (0, 0, {}))
        self.assertEqual(loaded.language, "pl")

    def test_damaged_file_is_ignored(self):
        for content in ("not json", "[1, 2]", json.dumps({"played": "x"})):
            self.path.write_text(content, encoding="utf-8")
            stats = Stats(self.path)
            self.assertEqual(stats.played, 0)

    def test_unwritable_location_does_not_crash(self):
        stats = Stats(Path(self._tmp.name) / "missing_dir" / "stats.json")
        stats.record_game("easy", won=True, attempts=1)
        self.assertEqual(stats.played, 1)


if __name__ == "__main__":
    unittest.main()
