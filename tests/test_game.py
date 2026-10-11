"""Unit tests for the game logic."""

import random
import unittest

from game import DIFFICULTIES, Difficulty, GuessingGame, GuessResult, parse_guess


class ParseGuessTest(unittest.TestCase):
    """Tests for parse_guess."""

    def test_valid_number(self):
        self.assertEqual(parse_guess(" 7 ", 1, 10), 7)

    def test_bounds_are_inclusive(self):
        self.assertEqual(parse_guess("1", 1, 10), 1)
        self.assertEqual(parse_guess("10", 1, 10), 10)

    def test_not_a_number(self):
        for text in ("", "abc", "3.5"):
            with self.assertRaisesRegex(ValueError, "whole number"):
                parse_guess(text, 1, 10)

    def test_out_of_range(self):
        for text in ("0", "11", "-5"):
            with self.assertRaisesRegex(ValueError, "between 1 and 10"):
                parse_guess(text, 1, 10)


class GuessingGameTest(unittest.TestCase):
    """Tests for GuessingGame."""

    def make_game(self, difficulty=Difficulty("Test", 1, 10, 3)):
        """Create a game with a known secret number (5)."""
        game = GuessingGame(difficulty, rng=random.Random(0))
        game.secret = 5
        return game

    def test_secret_within_range(self):
        for difficulty in DIFFICULTIES:
            for seed in range(50):
                game = GuessingGame(difficulty, rng=random.Random(seed))
                self.assertTrue(difficulty.low <= game.secret <= difficulty.high)

    def test_hints(self):
        game = self.make_game()
        self.assertIs(game.guess(2), GuessResult.TOO_LOW)
        self.assertIs(game.guess(8), GuessResult.TOO_HIGH)
        self.assertIs(game.guess(5), GuessResult.CORRECT)
        self.assertTrue(game.won)
        self.assertTrue(game.is_over)
        self.assertEqual(game.guesses, [2, 8, 5])

    def test_attempt_counting(self):
        game = self.make_game()
        self.assertEqual(game.attempts_left, 3)
        game.guess(1)
        self.assertEqual(game.attempts, 1)
        self.assertEqual(game.attempts_left, 2)

    def test_lose_after_max_attempts(self):
        game = self.make_game()
        for _ in range(3):
            game.guess(1)
        self.assertTrue(game.is_over)
        self.assertFalse(game.won)

    def test_no_guesses_after_game_over(self):
        game = self.make_game()
        game.guess(5)
        with self.assertRaises(RuntimeError):
            game.guess(5)

    def test_attempt_limit_allows_binary_search(self):
        for difficulty in DIFFICULTIES:
            size = difficulty.high - difficulty.low + 1
            self.assertGreaterEqual(2 ** difficulty.max_attempts, size + 1)


if __name__ == "__main__":
    unittest.main()
