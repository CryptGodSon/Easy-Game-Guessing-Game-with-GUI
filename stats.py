"""Persistent player statistics and settings stored in a small JSON file."""

import json
import os
from pathlib import Path

DEFAULT_PATH = Path.home() / ".guessing_game.json"


class Stats:
    """Games played/won, best score per difficulty and the chosen language."""

    def __init__(self, path=DEFAULT_PATH):
        self.path = Path(path)
        self.played = 0
        self.won = 0
        self.best = {}
        self.language = None
        self.load()

    @property
    def win_rate(self):
        """Percentage of games won (0 when nothing was played yet)."""
        return round(100 * self.won / self.played) if self.played else 0

    def record_game(self, difficulty_key, won, attempts):
        """Update statistics after a finished game.

        Returns True when the result is a new best score for the difficulty.
        """
        self.played += 1
        new_record = False
        if won:
            self.won += 1
            best = self.best.get(difficulty_key)
            if best is None or attempts < best:
                self.best[difficulty_key] = attempts
                new_record = best is not None
        self.save()
        return new_record

    def reset(self):
        """Forget all results (the language setting is kept)."""
        self.played = 0
        self.won = 0
        self.best = {}
        self.save()

    def load(self):
        """Read the stats file; a missing or damaged file means empty stats."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.played = int(data.get("played", 0))
            self.won = int(data.get("won", 0))
            self.best = {str(k): int(v) for k, v in data.get("best", {}).items()}
            language = data.get("language")
            self.language = language if isinstance(language, str) else None
        except (OSError, ValueError, TypeError, AttributeError):
            pass

    def save(self):
        """Write the stats file; failures (e.g. read-only home) are ignored."""
        data = {
            "played": self.played,
            "won": self.won,
            "best": self.best,
            "language": self.language,
        }
        tmp_path = self.path.with_suffix(".tmp")
        try:
            tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            os.replace(tmp_path, self.path)
        except OSError:
            pass
