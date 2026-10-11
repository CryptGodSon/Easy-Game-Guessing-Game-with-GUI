"""Unit tests for translations."""

import string
import unittest

from game import DIFFICULTIES
from i18n import LANGUAGES, TEXTS, tr


def placeholders(text):
    """Return the set of {names} used in a format string."""
    return {name for _, name, _, _ in string.Formatter().parse(text) if name}


class TranslationsTest(unittest.TestCase):
    """Every language must provide the same texts with the same placeholders."""

    def test_all_languages_have_texts(self):
        self.assertEqual(set(LANGUAGES), set(TEXTS))

    def test_same_keys_and_placeholders(self):
        english = TEXTS["en"]
        for code, texts in TEXTS.items():
            with self.subTest(language=code):
                self.assertEqual(set(texts), set(english))
                for key, text in texts.items():
                    self.assertEqual(placeholders(text), placeholders(english[key]), key)

    def test_difficulties_are_translated(self):
        for texts in TEXTS.values():
            for difficulty in DIFFICULTIES:
                self.assertIn(difficulty.key, texts)

    def test_tr_formats_and_falls_back_to_english(self):
        self.assertEqual(tr("pl", "attempts_left", count=3), "Pozostałe próby: 3")
        self.assertEqual(tr("xx", "check"), "Check")


if __name__ == "__main__":
    unittest.main()
