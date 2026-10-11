"""Unit tests for the game logic."""

import random
import unittest

from game import (
    DIFFICULTIES,
    Difficulty,
    GuessError,
    GuessingGame,
    GuessResult,
    parse_guess,
)


class ParseGuessTest(unittest.TestCase):
    """Tests for parse_guess."""

    def test_valid_number(self):
        self.assertEqual(parse_guess(" 7 ", 1, 10), 7)

    def test_bounds_are_inclusive(self):
        self.assertEqual(parse_guess("1", 1, 10), 1)
        self.assertEqual(parse_guess("10", 1, 10), 10)

    def test_not_a_number(self):
        for text in ("", "abc", "3.5"):
            with self.assertRaises(GuessError) as ctx:
                parse_guess(text, 1, 10)
            self.assertEqual(ctx.exception.reason, "not_number")

    def test_out_of_range(self):
        for text in ("0", "11", "-5"):
            with self.assertRaises(GuessError) as ctx:
                parse_guess(text, 1, 10)
            self.assertEqual(ctx.exception.reason, "out_of_range")
            self.assertEqual((ctx.exception.low, ctx.exception.high), (1, 10))

    def test_guess_error_is_value_error(self):
        with self.assertRaises(ValueError):
            parse_guess("x", 1, 10)


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

    def test_possible_range_narrows(self):
        game = self.make_game()
        self.assertEqual((game.lower_bound, game.upper_bound), (1, 10))
        game.guess(3)
        self.assertEqual((game.lower_bound, game.upper_bound), (4, 10))
        game.guess(8)
        self.assertEqual((game.lower_bound, game.upper_bound), (4, 7))
        game.guess(5)
        self.assertEqual((game.lower_bound, game.upper_bound), (5, 5))

    def test_range_never_widens(self):
        game = self.make_game(Difficulty("Test", 1, 10, 5))
        game.guess(4)
        game.guess(2)
        game.guess(7)
        game.guess(9)
        self.assertEqual((game.lower_bound, game.upper_bound), (5, 6))

    def test_is_close(self):
        game = GuessingGame(Difficulty("Test", 1, 100, 8))
        game.secret = 50
        self.assertTrue(game.is_close(45))
        self.assertTrue(game.is_close(55))
        self.assertFalse(game.is_close(44))
        small = self.make_game()
        self.assertTrue(small.is_close(6))
        self.assertFalse(small.is_close(7))

    def test_difficulty_keys_are_unique(self):
        keys = [d.key for d in DIFFICULTIES]
        self.assertEqual(len(keys), len(set(keys)))

    def test_attempt_limit_allows_binary_search(self):
        for difficulty in DIFFICULTIES:
            size = difficulty.high - difficulty.low + 1
            self.assertGreaterEqual(2 ** difficulty.max_attempts, size + 1)


if __name__ == "__main__":
    unittest.main()
