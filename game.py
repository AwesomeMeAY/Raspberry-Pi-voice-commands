from time import sleep
from random import choice
from voice import recognize_speech
import pyttsx3 as textspeech

moves = ["rock", "paper", "scissors"]
engine = textspeech.init()

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

def lazy_recognize():
    try:
        player_choice = recognize_speech().lower() 
        if not player_choice in moves:
            engine.say("You cheater, that is not a move. Try again")
            engine.runAndWait()
            return lazy_recognize()
        return player_choice
    except AttributeError:
        print("The game could not hear you! try again")
        return lazy_recognize()

# rock paper scissors
def rps():
    bot_choice = choice(moves)
    engine.say("Choose your move")
    engine.runAndWait()
    player_choice = lazy_recognize()
    for i in moves:
        engine.say(i)
        sleep(0.5)
    engine.say("Shoot")
    engine.say(f"I chose {bot_choice}")
    engine.say(get_win_condition(player_choice, bot_choice))
    engine.runAndWait()
    
if __name__ == '__main__':
    rps()
