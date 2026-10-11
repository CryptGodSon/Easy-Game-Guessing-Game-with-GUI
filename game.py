"""Core logic of the number guessing game, independent of any user interface."""

import random
from dataclasses import dataclass
from enum import Enum


class GuessResult(Enum):
    """Possible outcomes of a single guess."""

    TOO_LOW = "too_low"
    TOO_HIGH = "too_high"
    CORRECT = "correct"


@dataclass(frozen=True)
class Difficulty:
    """Range of numbers and attempt limit for a game."""

    name: str
    low: int
    high: int
    max_attempts: int


DIFFICULTIES = (
    Difficulty("Easy", 1, 10, 5),
    Difficulty("Medium", 1, 50, 7),
    Difficulty("Hard", 1, 100, 8),
)


def parse_guess(text, low, high):
    """Convert user input to an int within [low, high].

    Raises ValueError with a user-friendly message when the input is invalid.
    """
    try:
        value = int(text.strip())
    except ValueError:
        raise ValueError("Please enter a whole number.") from None
    if not low <= value <= high:
        raise ValueError(f"The number must be between {low} and {high}.")
    return value


class GuessingGame:
    """A single round of the guessing game."""

    def __init__(self, difficulty=DIFFICULTIES[0], rng=None):
        self.difficulty = difficulty
        self._rng = rng or random.Random()
        self.secret = self._rng.randint(difficulty.low, difficulty.high)
        self.guesses = []
        self.won = False

    @property
    def attempts(self):
        """Number of guesses made so far."""
        return len(self.guesses)

    @property
    def attempts_left(self):
        """Number of guesses the player still has."""
        return self.difficulty.max_attempts - self.attempts

    @property
    def is_over(self):
        """True when the player has won or run out of attempts."""
        return self.won or self.attempts_left <= 0

    def guess(self, value):
        """Register a guess and return how it compares to the secret number."""
        if self.is_over:
            raise RuntimeError("The game is already over.")
        self.guesses.append(value)
        if value < self.secret:
            return GuessResult.TOO_LOW
        if value > self.secret:
            return GuessResult.TOO_HIGH
        self.won = True
        return GuessResult.CORRECT
