import time
from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

#Data frame
word_data = pandas.read_csv("data/Korean_words.csv")
try:
    learned_words = pandas.read_csv("words_learned.csv")
    #Filter learned words
    to_learn = word_data[~word_data["Korean"].isin(learned_words["Korean"])].to_dict(orient="records")
except:
    #If file with learned words doesn't exist
    to_learn = word_data.to_dict(orient= "records")
learned = {}
current_card = {}
# Window
window = Tk()
window.config(bg=BACKGROUND_COLOR, width= 800, height=600)
window.title("Flashcards")
flip_timer = None

# Images
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

# ---------------------------- Functions ----------------------------#
def pick_new_word():
    global current_card, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer) #Annuleer de oude timer
    if not to_learn:
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="You've learned all words!", fill="black")
        canvas.itemconfig(card_bg, image=card_front_img)
        return
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text = "Korean", fill="black")
    canvas.itemconfig(card_word, text= current_card["Korean"], fill="black")
    canvas.itemconfig(card_bg, image= card_front_img)
    #After 3 seconds flip the card
    flip_timer = window.after(5000,flip_card)

def flip_card():
    global flip_timer
    canvas.itemconfig(card_bg, image=card_back_img)
    canvas.itemconfig(card_title, text= "English", fill= "white")
    canvas.itemconfig(card_word, text= current_card["English"], fill= "white")
    flip_timer = None #timer is reset

def known_word():
    global to_learn
    if current_card in to_learn:
        to_learn.remove(current_card)
        #DataFrame of current card
        learned_df = pandas.DataFrame([current_card])
        #Add to csv file (or make one if csv file doesn't exist
        learned_df.to_csv("words_learned.csv", mode= "a", header=not pandas.io.common.file_exists("words_learned.csv"), index = False)
        # Update ook je to_learn file na verwijderen van het woord
        to_learn_df = pandas.DataFrame(to_learn)
        to_learn_df.to_csv("words_to_learn.csv", index=False)
        pick_new_word()

def wrong_word():
    # Word not learned so stays in to_learn
    # Just update
    to_learn_df = pandas.DataFrame(to_learn)
    to_learn_df.to_csv("words_to_learn.csv", index=False)
    pick_new_word()
# ---------------------------- UI ----------------------------#
# Canvas card
canvas = Canvas(width=800,height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_image(400,263, image= card_front_img)
card_title = canvas.create_text(400,150, text="Korean", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400,263, text="KoreanWord", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2, padx=50,pady=50)

# Buttons
right_button = Button(
    image=right_image,
    bd=0,
    relief="flat",
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR,
    command= known_word
)
right_button.grid(column=1, row=1, padx=50, pady=50)

wrong_button = Button(
    image=wrong_image,
    bd=0,
    relief="flat",
    highlightthickness=0,
    bg=BACKGROUND_COLOR,
    activebackground=BACKGROUND_COLOR,
    command=wrong_word
)
wrong_button.grid(column=0, row=1, padx=50, pady=50)

# window.mainloop
window.mainloop()



