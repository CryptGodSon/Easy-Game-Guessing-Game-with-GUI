"""Tkinter GUI for the number guessing game."""

import tkinter as tk
from tkinter import ttk

from game import DIFFICULTIES, GuessingGame, GuessResult, parse_guess

COLOR_INFO = "#1f4e79"
COLOR_ERROR = "#b00020"
COLOR_SUCCESS = "#2e7d32"


class GuessingGameApp:  # pylint: disable=too-many-instance-attributes
    """Main application window."""

    def __init__(self, root):
        self.root = root
        self.root.title("Guessing Game")
        self.root.resizable(False, False)

        self.game = None
        self.best_scores = {}
        self.difficulty_var = tk.StringVar(value=DIFFICULTIES[0].name)

        frame = ttk.Frame(root, padding=16)
        frame.grid(sticky="nsew")

        ttk.Label(frame, text="Difficulty:").grid(row=0, column=0, sticky="w")
        difficulty_box = ttk.Combobox(
            frame,
            textvariable=self.difficulty_var,
            values=[d.name for d in DIFFICULTIES],
            state="readonly",
            width=10,
        )
        difficulty_box.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        difficulty_box.bind("<<ComboboxSelected>>", lambda _event: self.new_game())

        self.prompt_label = ttk.Label(frame)
        self.prompt_label.grid(row=1, column=0, sticky="w")
        self.guess_entry = ttk.Entry(frame, width=12)
        self.guess_entry.grid(row=1, column=1, sticky="ew")

        self.feedback_label = tk.Label(frame, wraplength=320, justify="center")
        self.feedback_label.grid(row=2, column=0, columnspan=2, pady=8)

        self.status_label = ttk.Label(frame)
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.history_label = ttk.Label(frame, wraplength=320, foreground="gray")
        self.history_label.grid(row=4, column=0, columnspan=2, pady=(4, 8))

        self.check_button = ttk.Button(frame, text="Check", command=self.check_guess)
        self.check_button.grid(row=5, column=0, sticky="ew", padx=(0, 4))
        ttk.Button(frame, text="New game", command=self.new_game).grid(
            row=5, column=1, sticky="ew", padx=(4, 0)
        )

        self.root.bind("<Return>", lambda _event: self.check_guess())
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.new_game()

    def selected_difficulty(self):
        """Return the Difficulty chosen in the combobox."""
        name = self.difficulty_var.get()
        return next(d for d in DIFFICULTIES if d.name == name)

    def new_game(self):
        """Start a new round with the selected difficulty."""
        difficulty = self.selected_difficulty()
        self.game = GuessingGame(difficulty)
        self.prompt_label.config(
            text=f"Guess a number between {difficulty.low} and {difficulty.high}:"
        )
        self.guess_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()
        self.show_feedback("Good luck!", COLOR_INFO)
        self.update_status()

    def check_guess(self):
        """Validate the input and evaluate the player's guess."""
        if self.game.is_over:
            return
        difficulty = self.game.difficulty
        try:
            value = parse_guess(self.guess_entry.get(), difficulty.low, difficulty.high)
        except ValueError as error:
            self.show_feedback(str(error), COLOR_ERROR)
            self.select_entry()
            return

        result = self.game.guess(value)
        if result is GuessResult.CORRECT:
            self.handle_win()
        elif self.game.is_over:
            self.show_feedback(
                f"Out of attempts! The number was {self.game.secret}.", COLOR_ERROR
            )
            self.end_round()
        else:
            hint = "Too low" if result is GuessResult.TOO_LOW else "Too high"
            self.show_feedback(f"{hint}. Try again.", COLOR_INFO)
            self.select_entry()
        self.update_status()

    def handle_win(self):
        """Show the victory message and remember the best score."""
        name = self.game.difficulty.name
        attempts = self.game.attempts
        message = (
            f"Congratulations! You guessed {self.game.secret} "
            f"in {attempts} {'attempt' if attempts == 1 else 'attempts'}."
        )
        best = self.best_scores.get(name)
        if best is None or attempts < best:
            self.best_scores[name] = attempts
            if best is not None:
                message += " New record!"
        self.show_feedback(message, COLOR_SUCCESS)
        self.end_round()

    def end_round(self):
        """Disable input until a new game is started."""
        self.guess_entry.config(state="disabled")
        self.check_button.config(state="disabled")

    def select_entry(self):
        """Select the entry text so the next guess overwrites it."""
        self.guess_entry.select_range(0, tk.END)
        self.guess_entry.focus_set()

    def show_feedback(self, text, color):
        """Display a message under the input field."""
        self.feedback_label.config(text=text, fg=color)

    def update_status(self):
        """Refresh attempts counter, best score and guess history."""
        best = self.best_scores.get(self.game.difficulty.name)
        status = f"Attempts left: {self.game.attempts_left}"
        if best is not None:
            status += f"   |   Best: {best}"
        self.status_label.config(text=status)
        history = ", ".join(str(g) for g in self.game.guesses)
        self.history_label.config(text=f"Your guesses: {history}" if history else "")


def main():
    """Create the window and run the Tkinter event loop."""
    root = tk.Tk()
    GuessingGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
