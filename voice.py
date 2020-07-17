import os
import webbrowser
import subprocess
import json
# http used for error exception
import http
import Timer
import weather
import toggle
import game
import speech_recognition as sr
import pyttsx3 as pytexttospeech
from itertools import chain
from difflib import get_close_matches

# Constants
try:
    with open("websites.json") as websites_json:
        WEBSITES = json.load(websites_json)
except FileNotFoundError:
    with open('websites.json','w') as websites_json:
        websites_json.write('{"google":"!g"}')
        WEBSITES = {"google":"!g"}
STANDARD_CUTOFF = 0.4
# Set some options for text to speech
engine = pytexttospeech.init()
engine.setProperty('rate',125)

# current_files, current_dirs and current_paths are defined at the bottom of the file.
# They are the current files, dirs, and paths in the directory.

def find_path(file):
    for path, dirs, files in os.walk(os.getcwd()):
        if any(i == file for i in chain(dirs, files)):
            return os.path.join(path, file)
    
    print("Could not find path!")
    
    

def file_search(file):
    return get_close_matches(file, current_files, cutoff=STANDARD_CUTOFF)[0]

def dir_search(directory):
    try:
        requested_dir = get_close_matches(directory, current_dirs, cutoff=STANDARD_CUTOFF)[0]
        dir_list = [requested_dir]
        # Iterating through the directory that was declared before.
        for dirs in os.listdir(find_path(requested_dir)):
            if os.path.isdir(find_path(dirs)):
                dir_list.append("{}/{}".format(requested_dir, dirs))       
        if len(get_close_matches(directory, dir_list, cutoff=STANDARD_CUTOFF)) == 0:
            return find_path(requested_dir)
        else:
            return get_close_matches(directory, dir_list, cutoff=STANDARD_CUTOFF)[0]
    # Index Error because get_close_matches returns a list
    # And if the list is emty there is no index 0 
    except IndexError:
        print('Could not find directory "{}"!'.format(directory))
        return ""
    
# commands

def search(command):
    duckurl = "https://www.duckduckgo.com/?q="
    website = command.split()[0]

    # if command.split()[0] in websites.json then it will search the website
    # instead of googling it.
    if website in WEBSITES:
        url = f"{duckurl}{WEBSITES[website]} {command[command.index(command.split()[1]):]}"
        
    else:
        url = duckurl + command

    webbrowser.open(url)
    return True

search.help = '''searches duckduckgo: "search (what you want to search for)". if you want to search a specific website:
"search (specific website)(what you want to search for)"'''  

def play_directory(command):    
    # Directory the user wants to play
    wanted_dir=  dir_search(command)
    # Get entire directory tree 
    for sub_dir, dirs, files in os.walk(os.getcwd()):
        if wanted_dir in sub_dir:
            engine.say(f"Playing {wanted_dir}")
            engine.runAndWait()
            os.system("vlc {}".format(sub_dir))                
            return True
play_directory.help = """Turns a directory into a vlc playlist: "playlist (directory)" """

def play(command):
    #this will play one file
    file = file_search(command[command.index(command.split()[1]):])
    engine.say(f"Playing {command}")
    engine.runAndWait()
    subprocess.call(["xdg-open",find_path(file)])
    return True

play.help = """Plays a file: "play (file)" """

def run(command):
    subprocess.run(command, shell=True)

run.help = """Runs command on the teminal: "run (command)" """

def add(command): 
    # The first letter will be the webbsite second will be the bang
    WEBSITES[command.split()[0]] = "!{}".format(command.split()[1])
    with open("websites.json", "w") as websites_json:
        json.dump(WEBSITES, websites_json)   

    print(WEBSITES)
    return True

add.help = """Adds a searchable website to the json: "add (website name) (duckduckgo bang)" """

def lst(directory=None):
    if directory:
        print(os.listdir(find_path(dir_search(directory))))
    else:
        print(os.listdir(os.getcwd()))
lst.help = """lists the contents of a directory:
list (directory)"""
       
        
def refresh():
    """ Order is: files, directories,then paths."""
    print("Refreshing files...")
    current_files = []
    current_dirs = []
    current_paths = []
    for paths, dirs, files in os.walk(os.getcwd()):
        current_files.extend(files)
        current_dirs.extend(dirs)
        current_paths.extend(paths)
    print("Done!")
    return current_files, current_dirs, current_paths

refresh.help = "Looks through the files and directories and saves any changes."

def note(command):
    # THis is what a command will look like
    # (Title) (Mode) (Junk to write down)
    modes = {"overwrite":"w", "append":"a", "read":"r"}
    title = ""
    # iterating through title until the it reaches mode
    for i in command.split():
        if i not in modes:
            title += i + " "
        else:
            break
    title = title.strip()
    # Seperating the title from everything else
    command = command[command.index(title[-1])+2:]
    mode = command.split()[0]
    try:
        with open(title, modes[mode]) as file:
            if mode == "read":
                print(file.read())
            else:
                file.write(command[command.index(command.split()[1]):])
    except KeyError:
        print("(NOTE) Could not find a mode in your command!")

note.help = """Write/append/read a txt file: (title) (mode) [if mode not read (what you want to write down)]"""

def timer(command):
    print("Me (The timer function has been called!")
    try:
        if len(command.split()) == 2 and command.split()[1] == "forever":
            subprocess.run(["python3", "Timer.py", str(command.split()[0]), "True"])
    # An index error will ocur if command.split[1] does not exist
    except IndexError:
        print("The actual timer is about to start!")

        Timer.timer(str(command.split()[0]))
        

timer.help = """Create a permint or temporary timer:
permamint: "timer (time in 24h time) forever"
temporary: "timer (time in 24h time)" """

def _help_(specific_command=None):
    if not specific_command:
        for k,v in exe.commands.items():
            print(" ")
            print("FUNCTION {}: {}".format(k.upper(), v.help))
    else:
        try:
            print(exe.commands[specific_command].help)
        except KeyError:
            print('"{}" is not a command!'.format(specific_command))

_help_.help = "Prints the help attribute of every command" 
def weather_speaker():
    forcast = weather.forecast()
    engine.say(forcast)
    engine.runAndWait()

def toggle_runner(audio_card):
    toggle.switch_audio_device(audio_card)

def exe(command):
    exe.commands = {"search":search, "playlist":play_directory, "play":play,
                "add":add, "run":run, "refresh":refresh, "list":lst,
                "help":_help_, "note":note, "timer":timer, "weather":weather_speaker, 'toggle':toggle.switch_audio_device, "game",game.rps}   
    
    command = command.lower()
    order = command.split()[0]
    if order in exe.commands:
        # The dictionary returns the function name which is then called in this line of code
        try:
            return exe.commands[order](command[command.index(command.split()[1]):])

        except IndexError:
            try:
                return exe.commands[order]()
            except:
                print("I misunderstood you and an error ocurred!")
                print(f"I thought you said {command}!")
                return 0
        
    else:
        print('Could not recognize command "{}"!'.format(command))
        return False

# speech recognition
recognizer = sr.Recognizer()
def recognize_speech(wait_length=5):
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=wait_length)
        except sr.WaitTimeoutError:
            print("You ran out of time!")
            return False
    print("Recognizing...")
    try:
        command = recognizer.recognize_google(audio)
        return command
    except(sr.RequestError, http.client.RemoteDisconnected):
        print("Something went wrong with the conection. Trying sphinx...")
        command = recognizer.recognize_sphinx(audio)
        return command 
    except sr.UnknownValueError:
        print("Could not hear what you were saying!")
        return False
    



current_files, current_dirs, current_subs = refresh()
if __name__ == "__main__":
    while True:
        exe(recognize_speech())
