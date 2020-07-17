from time import sleep
from random import choice
from voice import recognize_speech
import pyttsx3 as textspeech

# rock paper scissors
def get_win_condition(player, bot):
    cheat_sheet = {"rock":"scissors", "paper":"rock","scissors":"paper"}
    # If player wins
    if cheat_sheet[player] == bot:
        return "You win, congratulations"
    # If bot wins
    elif cheat_sheet[bot] == player:
        return "I win. You stink at this game loser haha"
    # If draw
    else:
        return "Draw"
def rps():
    engine = textspeech.init()
    moves = ["rock", "paper", "scissors"]
    bot_choice = choice(moves)
    engine.say("Choose your move")
    engine.runAndWait()
    player_choice = recognize_speech(1).lower()
    for i in moves:
        engine.say(i)
        sleep(0.5)
    engine.say("Shoot")
    engine.say(f"I chose {bot_choice}")
    engine.say(get_win_condition(player_choice, bot_choice))
    engine.runAndWait()
if __name__ == '__main__':
    rps()
