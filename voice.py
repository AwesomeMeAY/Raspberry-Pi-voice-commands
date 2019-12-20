import os
import webbrowser
import subprocess
import json
import speech_recognition as sr
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

def play_directory(command):
    combined_dir =  dir_search(command)
    for sub_dir, dirs, files in os.walk(os.getcwd()):
        if combined_dir in sub_dir:
            os.system("vlc {}".format(sub_dir))                
            return True

def play(command):
    #this will play one file
    file = file_search(command[command.index(command.split()[1]):])
    subprocess.call(["xdg-open",find_path(file)])
    return True

def run(command):
    os.system(command)
    return True  

def add(command):
    # The first letter will be the webbsite second will be the bang
    WEBSITES[command.split()[0]] = "!{}".format(command.split()[1])
    with open("websites.json", "w") as websites_json:
        json.dump(WEBSITES, websites_json)   

    print(WEBSITES)
    return True

def lst(directory):
    print(os.listdir(find_path(dir_search(directory))))
        
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

def exe(command):
    commands = {"search":search, "playlist":play_directory, "play":play,
                "add":add, "run":run, "refresh":refresh, "list":lst}   
    command = command.lower()
    order = command.split()[0]

    if order in commands:
        # The dictionary returns the function name which is called in this line of code
        # did not expect that to work.
        try:
            return commands[order](command[command.index(command.split()[1]):])
        except IndexError:
            return commands[order]()
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
    except sr.RequestError:
        print("Something went wrong with the conection. Trying sphinx...")
        command_worked = exe(recognizer.recognize_sphinx(audio))
    
    except sr.UnknownValueError:
        print("Could not hear what you were saying!")
        return False
    
    if not command_worked:
        print("Something went wrong with the exe function!")
        return False
    else:
        return True


current_files, current_dirs, current_subs = refresh()

if __name__ == "__main__":
    while True:
        recognize_speech()  
