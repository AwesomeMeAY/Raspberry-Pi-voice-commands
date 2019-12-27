import os
import webbrowser
import subprocess
import json
import threading
import datetime
# http used for error exception
import http
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from itertools import chain
from difflib import get_close_matches

# Constants
with open("websites.json") as websites_json:
    WEBSITES = json.load(websites_json)

STANDARD_CUTOFF = 0.4

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
        url = "{}{} {}".format(duckurl, WEBSITES[website], command[command.index(command.split()[1]):])
        
    else:
        url = duckurl + command

    webbrowser.open(url)
    return True

search.help = '''searches duckduckgo: "search (what you want to search for)". if you want to search a specific website:
"search (specific website)(what you want to search for)"'''  

def play_directory(command):    
    combined_dir =  dir_search(command)
    for sub_dir, dirs, files in os.walk(os.getcwd()):
        if combined_dir in sub_dir:
            os.system("vlc {}".format(sub_dir))                
            return True
play_directory.help = """Turns a directory into a vlc playlist: "playlist (directory)" """

def play(command):
    #this will play one file
    file = file_search(command[command.index(command.split()[1]):])
    subprocess.call(["xdg-open",find_path(file)])
    return True

play.help = """Plays a file: "play (file)" """

def run(command):
    subprocess.call(command, shell=True)

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

refresh.help = "Looks through the files and directories again"

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
    if len(command.split())+1 == 2 and command.split()[1] == "forever":
        os.system("python3 Timer.py {} {}".format(command.split()[0], True))
    else:
        os.system("python3 Timer.py {}".format(command))

timer.help = """Create a permint or temporary timer:
permamint: "timer (time in 24h time) forever"
temporary: "timer (time in 24h time)" """

def exe(command):
    exe.commands = {"search":search, "playlist":play_directory, "play":play,
                "add":add, "run":run, "refresh":refresh, "list":lst,
                    "help":_help_, "note":note, "timer":timer}   
    
    command = command.lower()
    order = command.split()[0]
    if order in exe.commands:
        # The dictionary returns the function name which is then called in this line of code
        try:
            return exe.commands[order](command[command.index(command.split()[1]):])

        except IndexError:
            return exe.commands[order]()

        
    else:
        print('Could not recognize command "{}"!'.format(command))
        return False

# speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("You ran out of time!")
            return False
    print("Recognizing...")
    try:
        command_worked = exe(recognizer.recognize_google(audio))
        return True
    except(sr.RequestError, http.client.RemoteDisconnected):
        print("Something went wrong with the conection. Trying sphinx...")
        command_worked = exe(recognizer.recognize_sphinx(audio))
    
    except sr.UnknownValueError:
        print("Could not hear what you were saying!")
        return False
    



current_files, current_dirs, current_subs = refresh()
exe("timer 1648")
                        
if __name__ == "__main__":
    while True:
        recognize_speech()  
