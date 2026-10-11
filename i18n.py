"""User interface texts in English and Polish."""

import locale

LANGUAGES = {"en": "English", "pl": "Polski"}

TEXTS = {
    "en": {
        "title": "Guessing Game",
        "menu_game": "Game",
        "menu_new": "New game",
        "menu_reset": "Reset statistics",
        "menu_quit": "Quit",
        "menu_language": "Language",
        "menu_help": "Help",
        "menu_how_to": "How to play",
        "menu_about": "About",
        "difficulty": "Difficulty:",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "expert": "Expert",
        "prompt": "Guess a number between {low} and {high}:",
        "check": "Check",
        "new_game": "New game",
        "good_luck": "Good luck!",
        "not_number": "Please enter a whole number.",
        "out_of_range": "The number must be between {low} and {high}.",
        "too_low": "Too low. Try again.",
        "too_high": "Too high. Try again.",
        "close": "You are very close!",
        "already_guessed": "You already tried {value}.",
        "win": "Congratulations! You guessed {secret} in {attempts} {attempt_word}.",
        "attempt_one": "attempt",
        "attempt_many": "attempts",
        "new_record": "New record!",
        "lose": "Out of attempts! The number was {secret}.",
        "attempts_left": "Attempts left: {count}",
        "possible_range": "Possible range: {low} – {high}",
        "history": "Your guesses: {history}",
        "stats": "Played: {played}   Won: {won} ({rate}%)   Best: {best}",
        "no_best": "–",
        "reset_confirm": "Reset all statistics?",
        "how_to_text": (
            "The computer picks a secret number from the chosen range.\n\n"
            "Type your guess and press Enter (or click Check). After each guess "
            "you get a hint whether the secret number is higher or lower.\n\n"
            "Guess it before you run out of attempts!\n\n"
            "Shortcuts: Enter – check, Ctrl+N – new game, Esc – quit."
        ),
        "about_text": "Guessing Game {version}\n\nA simple number guessing game "
        "written in Python and Tkinter.\n\nMIT License",
    },
    "pl": {
        "title": "Zgadnij liczbę",
        "menu_game": "Gra",
        "menu_new": "Nowa gra",
        "menu_reset": "Wyzeruj statystyki",
        "menu_quit": "Zakończ",
        "menu_language": "Język",
        "menu_help": "Pomoc",
        "menu_how_to": "Jak grać",
        "menu_about": "O programie",
        "difficulty": "Poziom:",
        "easy": "Łatwy",
        "medium": "Średni",
        "hard": "Trudny",
        "expert": "Ekspert",
        "prompt": "Zgadnij liczbę od {low} do {high}:",
        "check": "Sprawdź",
        "new_game": "Nowa gra",
        "good_luck": "Powodzenia!",
        "not_number": "Wpisz liczbę całkowitą.",
        "out_of_range": "Liczba musi być z zakresu od {low} do {high}.",
        "too_low": "Za mało. Spróbuj jeszcze raz.",
        "too_high": "Za dużo. Spróbuj jeszcze raz.",
        "close": "Jesteś bardzo blisko!",
        "already_guessed": "Liczba {value} była już sprawdzana.",
        "win": "Brawo! Liczba {secret} odgadnięta w {attempts} {attempt_word}.",
        "attempt_one": "próbie",
        "attempt_many": "próbach",
        "new_record": "Nowy rekord!",
        "lose": "Koniec prób! Szukana liczba to {secret}.",
        "attempts_left": "Pozostałe próby: {count}",
        "possible_range": "Możliwy zakres: {low} – {high}",
        "history": "Twoje strzały: {history}",
        "stats": "Gry: {played}   Wygrane: {won} ({rate}%)   Rekord: {best}",
        "no_best": "–",
        "reset_confirm": "Wyzerować wszystkie statystyki?",
        "how_to_text": (
            "Komputer losuje liczbę z wybranego zakresu.\n\n"
            "Wpisz swój strzał i naciśnij Enter (albo kliknij Sprawdź). Po każdym "
            "strzale dostaniesz podpowiedź, czy szukana liczba jest większa, czy "
            "mniejsza.\n\n"
            "Zgadnij ją, zanim skończą Ci się próby!\n\n"
            "Skróty: Enter – sprawdź, Ctrl+N – nowa gra, Esc – zakończ."
        ),
        "about_text": "Zgadnij liczbę {version}\n\nProsta gra w zgadywanie liczb "
        "napisana w Pythonie i Tkinterze.\n\nLicencja MIT",
    },
}


def default_language():
    """Pick Polish for Polish system locales, English otherwise."""
    try:
        code = locale.getlocale()[0] or ""
    except ValueError:
        code = ""
    return "pl" if code.lower().startswith("pl") else "en"


def tr(language, key, **kwargs):
    """Translate ``key`` into ``language`` (English is the fallback)."""
    text = TEXTS.get(language, TEXTS["en"]).get(key) or TEXTS["en"][key]
    return text.format(**kwargs) if kwargs else text
