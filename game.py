"""Core logic of the number guessing game, independent of any user interface."""

import random
from dataclasses import dataclass
from enum import Enum

__version__ = "2.0.0"


class GuessResult(Enum):
    """Possible outcomes of a single guess."""

    TOO_LOW = "too_low"
    TOO_HIGH = "too_high"
    CORRECT = "correct"


@dataclass(frozen=True)
class Difficulty:
    """Range of numbers and attempt limit for a game."""

    key: str
    low: int
    high: int
    max_attempts: int

    @property
    def size(self):
        """How many numbers can be drawn."""
        return self.high - self.low + 1


DIFFICULTIES = (
    Difficulty("easy", 1, 10, 5),
    Difficulty("medium", 1, 50, 7),
    Difficulty("hard", 1, 100, 8),
    Difficulty("expert", 1, 1000, 10),
)


class GuessError(ValueError):
    """Raised when the user's input is not a valid guess.

    ``reason`` is either ``"not_number"`` or ``"out_of_range"`` so that the
    user interface can show a message in its own language.
    """

    def __init__(self, reason, low, high):
        super().__init__(f"{reason}: expected a whole number between {low} and {high}")
        self.reason = reason
        self.low = low
        self.high = high


def parse_guess(text, low, high):
    """Convert user input to an int within [low, high] or raise GuessError."""
    try:
        value = int(text.strip())
    except ValueError:
        raise GuessError("not_number", low, high) from None
    if not low <= value <= high:
        raise GuessError("out_of_range", low, high)
    return value


class GuessingGame:
    """A single round of the guessing game."""

    def __init__(self, difficulty=DIFFICULTIES[0], rng=None):
        self.difficulty = difficulty
        self._rng = rng or random.Random()
        self.secret = self._rng.randint(difficulty.low, difficulty.high)
        self.guesses = []
        self.won = False
        self.lower_bound = difficulty.low
        self.upper_bound = difficulty.high

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

    def is_close(self, value):
        """True when a wrong guess is within 5% of the range from the secret."""
        return abs(value - self.secret) <= max(1, self.difficulty.size // 20)

    def guess(self, value):
        """Register a guess and return how it compares to the secret number."""
        if self.is_over:
            raise RuntimeError("The game is already over.")
        self.guesses.append(value)
        if value < self.secret:
            self.lower_bound = max(self.lower_bound, value + 1)
            return GuessResult.TOO_LOW
        if value > self.secret:
            self.upper_bound = min(self.upper_bound, value - 1)
            return GuessResult.TOO_HIGH
        self.won = True
        self.lower_bound = self.upper_bound = value
        return GuessResult.CORRECT
