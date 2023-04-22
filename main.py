import random
import tkinter as tk

# generate a random number between 1 and 10
number = random.randint(1, 10)

# create a Tkinter window
window = tk.Tk()
window.title("Guessing Game")

# create a label and entry widget for the user's guess
tk.Label(window, text="Guess a number between 1 and 10:").grid(row=0, column=0)
guess_entry = tk.Entry(window)
guess_entry.grid(row=0, column=1)

# create a label widget to display the feedback
feedback_label = tk.Label(window, text="")
feedback_label.grid(row=1, column=0, columnspan=2)


# create a function to check the user's guess
def check_guess():
    # get the user's guess from the entry widget
    guess = int(guess_entry.get())

    # check if the guess is correct
    if guess == number:
        feedback_label.config(text="Congratulations! You guessed the number.")
    elif guess < number:
        feedback_label.config(text="Too low. Try again.")
    else:
        feedback_label.config(text="Too high. Try again.")


# create a button widget to check the user's guess
check_button = tk.Button(window, text="Check", command=check_guess)
check_button.grid(row=2, column=0, columnspan=2)

# bind the Enter key to the "Check" button
window.bind('<Return>', lambda event: check_button.invoke())

# start the Tkinter event loop
window.mainloop()
