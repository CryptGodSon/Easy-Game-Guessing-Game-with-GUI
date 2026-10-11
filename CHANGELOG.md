# Changelog

## 2.0.0

- Polish and English user interface (Language menu, remembered between runs;
  Polish is chosen automatically on Polish systems)
- New **Expert** difficulty (1–1000, 10 attempts)
- Statistics saved between runs: games played, games won, win rate and best
  score per difficulty (`~/.guessing_game.json`), with a "Reset statistics" option
- "You are very close!" hint and the possible range shrinking after every guess
- Repeating a number already tried no longer costs an attempt
- Attempts progress bar, menu bar (Game / Language / Help), `Ctrl+N` shortcut,
  window centred on screen
- Can be installed with `pip install .` and started with `guessing-game`
- More unit tests (statistics, translations); CI on Python 3.9–3.13, Dependabot
  for GitHub Actions

## 1.1.0

- Game logic moved to `game.py` and covered by unit tests
- Input validation (letters and out-of-range numbers no longer crash the game)
- Easy / Medium / Hard difficulty with attempt limits, guess history,
  best score and a "New game" button
- README fixes and a screenshot; CI runs pylint and the tests

## 1.0.0

- First version: guess a number between 1 and 10 in a Tkinter window
