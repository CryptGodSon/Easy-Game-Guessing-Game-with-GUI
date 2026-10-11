"""Tkinter GUI for the number guessing game."""

import tkinter as tk
from tkinter import messagebox, ttk

from game import (
    DIFFICULTIES,
    GuessError,
    GuessingGame,
    GuessResult,
    __version__,
    parse_guess,
)
from i18n import LANGUAGES, default_language, tr
from stats import Stats

COLOR_INFO = "#1f4e79"
COLOR_WARNING = "#b26a00"
COLOR_ERROR = "#b00020"
COLOR_SUCCESS = "#2e7d32"
WRAP = 340


class GuessingGameApp:  # pylint: disable=too-many-instance-attributes
    """Main application window."""

    def __init__(self, root, stats=None):
        self.root = root
        self.root.resizable(False, False)

        self.stats = stats if stats is not None else Stats()
        self.language = self.stats.language or default_language()
        self.game = None
        # Feedback is kept as translation keys so it can be re-rendered
        # when the language changes: ([(key, kwargs), ...], color).
        self.feedback = ([], COLOR_INFO)
        self.language_var = tk.StringVar(value=self.language)

        frame = ttk.Frame(root, padding=16)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)

        self.difficulty_label = ttk.Label(frame)
        self.difficulty_label.grid(row=0, column=0, sticky="w")
        self.difficulty_box = ttk.Combobox(frame, state="readonly", width=12)
        self.difficulty_box.grid(row=0, column=1, sticky="ew", pady=(0, 8))
        self.difficulty_box.bind("<<ComboboxSelected>>", lambda _event: self.new_game())

        self.prompt_label = ttk.Label(frame)
        self.prompt_label.grid(row=1, column=0, sticky="w", padx=(0, 8))
        self.guess_entry = ttk.Entry(frame, width=12, justify="center")
        self.guess_entry.grid(row=1, column=1, sticky="ew")

        self.feedback_label = tk.Label(frame, wraplength=WRAP, justify="center")
        self.feedback_label.grid(row=2, column=0, columnspan=2, pady=8)

        self.attempts_label = ttk.Label(frame)
        self.attempts_label.grid(row=3, column=0, columnspan=2)
        self.attempts_bar = ttk.Progressbar(frame, mode="determinate")
        self.attempts_bar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(2, 6))

        self.range_label = ttk.Label(frame)
        self.range_label.grid(row=5, column=0, columnspan=2)
        self.history_label = ttk.Label(frame, wraplength=WRAP, foreground="gray")
        self.history_label.grid(row=6, column=0, columnspan=2, pady=(4, 8))

        self.check_button = ttk.Button(frame, command=self.check_guess)
        self.check_button.grid(row=7, column=0, sticky="ew", padx=(0, 4))
        self.new_game_button = ttk.Button(frame, command=self.new_game)
        self.new_game_button.grid(row=7, column=1, sticky="ew", padx=(4, 0))

        ttk.Separator(frame).grid(row=8, column=0, columnspan=2, sticky="ew", pady=8)
        self.stats_label = ttk.Label(frame, foreground="gray")
        self.stats_label.grid(row=9, column=0, columnspan=2)

        self.root.bind("<Return>", lambda _event: self.check_guess())
        self.root.bind("<KP_Enter>", lambda _event: self.check_guess())
        self.root.bind("<Control-n>", lambda _event: self.new_game())
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.build_menu()
        self.difficulty_box.config(values=[self.t(d.key) for d in DIFFICULTIES])
        self.difficulty_box.current(0)
        self.new_game()
        center_window(self.root)

    # ----------------------------------------------------------- helpers
    def t(self, key, **kwargs):
        """Translate a text into the current language."""
        return tr(self.language, key, **kwargs)

    def selected_difficulty(self):
        """Return the Difficulty chosen in the combobox."""
        return DIFFICULTIES[max(self.difficulty_box.current(), 0)]

    # -------------------------------------------------------------- menu
    def build_menu(self):
        """Create (or re-create after a language change) the menu bar."""
        menubar = tk.Menu(self.root)

        game_menu = tk.Menu(menubar, tearoff=False)
        game_menu.add_command(
            label=self.t("menu_new"), accelerator="Ctrl+N", command=self.new_game
        )
        game_menu.add_command(label=self.t("menu_reset"), command=self.reset_stats)
        game_menu.add_separator()
        game_menu.add_command(
            label=self.t("menu_quit"), accelerator="Esc", command=self.root.destroy
        )
        menubar.add_cascade(label=self.t("menu_game"), menu=game_menu)

        language_menu = tk.Menu(menubar, tearoff=False)
        for code, name in LANGUAGES.items():
            language_menu.add_radiobutton(
                label=name,
                value=code,
                variable=self.language_var,
                command=lambda c=code: self.set_language(c),
            )
        menubar.add_cascade(label=self.t("menu_language"), menu=language_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(
            label=self.t("menu_how_to"),
            command=lambda: messagebox.showinfo(
                self.t("menu_how_to"), self.t("how_to_text"), parent=self.root
            ),
        )
        help_menu.add_command(
            label=self.t("menu_about"),
            command=lambda: messagebox.showinfo(
                self.t("menu_about"),
                self.t("about_text", version=__version__),
                parent=self.root,
            ),
        )
        menubar.add_cascade(label=self.t("menu_help"), menu=help_menu)

        self.root.config(menu=menubar)

    def set_language(self, code):
        """Switch the interface language and remember the choice."""
        self.language = code
        self.language_var.set(code)
        self.stats.language = code
        self.stats.save()
        self.build_menu()
        self.refresh()

    def reset_stats(self):
        """Ask for confirmation and clear the statistics."""
        if messagebox.askyesno(self.t("menu_reset"), self.t("reset_confirm"), parent=self.root):
            self.stats.reset()
            self.refresh()

    # -------------------------------------------------------------- game
    def new_game(self):
        """Start a new round with the selected difficulty."""
        self.game = GuessingGame(self.selected_difficulty())
        self.guess_entry.config(state="normal")
        self.check_button.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()
        self.feedback = ([("good_luck", {})], COLOR_INFO)
        self.refresh()

    def check_guess(self):
        """Validate the input and evaluate the player's guess."""
        if self.game.is_over:
            return
        difficulty = self.game.difficulty
        try:
            value = parse_guess(self.guess_entry.get(), difficulty.low, difficulty.high)
        except GuessError as error:
            self.feedback = (
                [(error.reason, {"low": error.low, "high": error.high})],
                COLOR_ERROR,
            )
            self.select_entry()
            self.refresh()
            return

        if value in self.game.guesses:
            self.feedback = ([("already_guessed", {"value": value})], COLOR_WARNING)
            self.select_entry()
            self.refresh()
            return

        result = self.game.guess(value)
        if result is GuessResult.CORRECT:
            self.finish_game(won=True)
        elif self.game.is_over:
            self.feedback = ([("lose", {"secret": self.game.secret})], COLOR_ERROR)
            self.finish_game(won=False)
        else:
            parts = [(result.value, {})]
            if self.game.is_close(value):
                parts.append(("close", {}))
            self.feedback = (parts, COLOR_INFO)
            self.select_entry()
        self.refresh()

    def finish_game(self, won):
        """Save the result and disable input until a new game is started."""
        attempts = self.game.attempts
        new_record = self.stats.record_game(self.game.difficulty.key, won, attempts)
        if won:
            word = "attempt_one" if attempts == 1 else "attempt_many"
            parts = [("win", {"secret": self.game.secret, "attempts": attempts, "word": word})]
            if new_record:
                parts.append(("new_record", {}))
            self.feedback = (parts, COLOR_SUCCESS)
        self.guess_entry.config(state="disabled")
        self.check_button.config(state="disabled")

    def select_entry(self):
        """Select the entry text so the next guess overwrites it."""
        self.guess_entry.select_range(0, tk.END)
        self.guess_entry.focus_set()

    # ----------------------------------------------------------- display
    def render_feedback(self):
        """Turn stored feedback keys into text in the current language."""
        parts, color = self.feedback
        texts = []
        for key, kwargs in parts:
            kwargs = dict(kwargs)
            if "word" in kwargs:
                kwargs["attempt_word"] = self.t(kwargs.pop("word"))
            texts.append(self.t(key, **kwargs))
        self.feedback_label.config(text=" ".join(texts), fg=color)

    def refresh(self):
        """Update every text and indicator in the window."""
        game = self.game
        difficulty = game.difficulty
        self.root.title(self.t("title"))
        self.difficulty_label.config(text=self.t("difficulty"))
        self.difficulty_box.config(values=[self.t(d.key) for d in DIFFICULTIES])
        self.difficulty_box.set(self.t(difficulty.key))
        self.prompt_label.config(
            text=self.t("prompt", low=difficulty.low, high=difficulty.high)
        )
        self.check_button.config(text=self.t("check"))
        self.new_game_button.config(text=self.t("new_game"))
        self.render_feedback()

        self.attempts_label.config(
            text=self.t("attempts_left", count=game.attempts_left)
        )
        self.attempts_bar.config(maximum=difficulty.max_attempts, value=game.attempts_left)
        self.range_label.config(
            text=self.t("possible_range", low=game.lower_bound, high=game.upper_bound)
        )
        history = ", ".join(str(g) for g in game.guesses)
        self.history_label.config(text=self.t("history", history=history) if history else "")

        best = self.stats.best.get(difficulty.key)
        self.stats_label.config(
            text=self.t(
                "stats",
                played=self.stats.played,
                won=self.stats.won,
                rate=self.stats.win_rate,
                best=best if best is not None else self.t("no_best"),
            )
        )


def center_window(window):
    """Place the window in the middle of the screen."""
    window.update_idletasks()
    width, height = window.winfo_reqwidth(), window.winfo_reqheight()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 3
    window.geometry(f"+{x}+{y}")


def main():
    """Create the window and run the Tkinter event loop."""
    root = tk.Tk()
    GuessingGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
