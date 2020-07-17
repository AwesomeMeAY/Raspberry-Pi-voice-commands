from time import sleep
from random import choice
from voice import recognize_speech
import pyttsx3 as textspeech

# rock paper scissors
def rps():
    engine = textspeech.init()
    moves = ["rock", "paper", "scissors"]
    cheat_sheet = {"rock":"scissors", "paper":"rock","scissors":"paper"}
    bot_choice = choice(moves)
    engine.say("Choose your move")
    engine.runAndWait()
    player_choice = recognize_speech(1).lower()
    for i in moves:
        engine.say(i)
        sleep(0.5)
    engine.say("Shoot")
    engine.say(f"I chose {bot_choice}")
    # If player wins
    if cheat_sheet[player_choice] == bot_choice:
        engine.say("You win, congratulations")
    # If bot wins
    elif cheat_sheet[bot_choice] == player_choice:
        engine.say("I win. You stink at this game loser haha")
    # If draw
    else:
        engine.say("Draw")
    engine.runAndWait()
rps()
