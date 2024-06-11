import tkinter as tk
from tkinter import messagebox
import random
okno = tk.Tk()
okno.title("Wordle")
canvas_width = 800

canvas = tk.Canvas(okno, height=500, width=canvas_width)


words = []
with open('data.txt', 'r') as file:
    for line in file:
        words.extend(line.split())


word = random.choice(words).lower()
print(word)


letter_spacing = 50
total_width = len(word) * letter_spacing

start_x = (canvas_width - total_width) // 2
max_tries = 5
current_try = 0
current_guess = ""
guesses = []


def reset_game():
    global word, current_try, current_guess, guesses
    word = random.choice(words).lower()
    current_try = 0
    current_guess = ""
    guesses = []
    print(word)
    canvas.delete("all")
    draw_lines()
    draw_label("GUESS THE WORD")
    guess_label.config(text="")
    tries_label.config(text=f"Tries left: {max_tries}")
    play_again_button.place_forget()
    quit_button.place_forget()


def draw_lines():
    x = start_x
    for i in range(len(word)):
        canvas.create_line(x, 250, x + 25, 250, tag="lines")
        x += letter_spacing


def draw_label(text):
    label_font = ("arial", 25)
    text_item = canvas.create_text(0, 0, text=text, font=label_font, anchor='nw')
    label_bbox = canvas.bbox(text_item)
    label_width = label_bbox[2] - label_bbox[0]
    canvas.delete(text_item)
    label_x = start_x + (total_width - label_width) // 2
    WordleTXT = tk.Label(okno, text=text, font=label_font)
    WordleTXT.place(x=label_x, y=150)


def update_guess_display():
    canvas.delete("current_guess")
    x = start_x
    for i, char in enumerate(current_guess):
        canvas.create_text(x + 12, 240 + current_try * 30, text=char.upper(), font=("arial", 18), tag="current_guess")
        x += letter_spacing


def update_guesses_display():
    canvas.delete("guesses")
    for idx, guess in enumerate(guesses):
        x = start_x
        for i, char in enumerate(guess):
            color = "black"
            if char == word[i]:
                color = "green"
            elif char in word:
                color = "yellow"
            canvas.create_text(x + 12, 240 + idx * 30, text=char.upper(), font=("arial", 18), fill=color, tag="guesses")
            x += letter_spacing

def on_key_press(event):
    global current_guess
    if len(current_guess) < len(word) and event.char.isalpha():
        current_guess += event.char.lower()
        update_guess_display()
    elif event.keysym == 'BackSpace' and len(current_guess) > 0:
        current_guess = current_guess[:-1]
        update_guess_display()
    elif event.keysym == 'Return' and len(current_guess) == len(word):
        check_guess()


def check_guess():
    global current_try, current_guess
    if current_guess not in words:
        messagebox.showwarning("Invalid Word", "The word is not in the list. Try again.")
        current_guess = ""
        update_guess_display()
        return

    guesses.append(current_guess)
    update_guesses_display()
    if current_guess == word:
        game_over("You won!")
    else:
        current_try += 1
        tries_label.config(text=f"Tries left: {max_tries - current_try}")
        if current_try >= max_tries:
            game_over(f"You lost! The word was: {word}")
    current_guess = ""
    update_guess_display()


def game_over(message):
    messagebox.showinfo("Game Over", message)
    play_again_button.place(x=300, y=400)
    quit_button.place(x=400, y=400)


def quit_game():
    okno.destroy()

#Button/txts
play_again_button = tk.Button(okno, text="Play Again", command=reset_game)
quit_button = tk.Button(okno, text="Quit", command=quit_game)


tries_label = tk.Label(okno, text=f"Tries left: {max_tries}", font=("arial", 18))
tries_label.place(x=50, y=50)


guess_label = tk.Label(okno, text="", font=("arial", 18))
guess_label.place(x=50, y=100)

#lines
draw_lines()
draw_label("GUESS THE WORD")


okno.bind("<KeyPress>", on_key_press)


canvas.pack()
okno.mainloop()
