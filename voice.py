import os
import webbrowser
import subprocess
import speech_recognition as sr
from time import sleep
from difflib import get_close_matches

# defining functions that are used 
def reload_files():
    found_files = []
    found_dirs = []
    found_subs = []
    for sub_dirs, dirs, files in os.walk(os.getcwd()):
        found_files += files
        found_dirs += dirs
        found_subs += sub_dirs
    return found_files, found_dirs, found_subs

def find_path(file):
    for subdir, dirs, files in os.walk(os.getcwd()):
            for f in files:
                if f == file:
                    return os.path.join(subdir, file)
            for d in dirs:
                if d == file:
                    return os.path.join(subdir, file)

def file_search(file):
    return get_close_matches(file, current_files)[0]

def dir_search(directory):
    try:
        requested_dir = get_close_matches(directory, current_dirs)[0]
        dir_list = []
        # Iterating through the directory that was declared before.
        for dirs in os.listdir(find_path(requested_dir)):
            if os.path.isdir(find_path(dirs)):
                dir_list.append("{}\{}".format(requested_dir, dirs))       
        if len(get_close_matches(directory, dir_list)) == 0:
            return find_path(requested_dir)
        return get_close_matches(directory, dir_list)[0]                           
    except:
        print('Could not find directory "{}"!'.format(directory))

def exe(command):
    duckurl = "https://www.duckduckgo.com/?q="
    command = command.lower()
    order = command.split()[0]
    if "search youtube" in command:
        # search youtube for command
        # Starts at index 2 because "search" is index 1 and "youtube" is index 1
        webbrowser.open(duckurl+ "!you " +command[command.index(command.split()[2]):])
        return True
    elif "open directory" in command:
        # This will open the folder where a specified peice of media is stored
        combined_dir =  dir_search(command[command.index(command.split()[2]):])
        for sub_dir, dirs, files in os.walk(os.getcwd()):
            if combined_dir in sub_dir:
                subprocess.call(["xdg-open",sub_dir])
                return True

    elif order == "search":
        # search duck duck go
        duckurl = duckurl + command[command.index(command.split()[1]):]
        webbrowser.open(duckurl)
        return True
    elif order == "play":
        #this will play movies
        file = file_search(command[command.index(command.split()[1]):])
        subprocess.call(["xdg-open",find_path(file)])
        return True
    elif order == "refresh" or order == "reload":
        print("{}ing files...".format(order.capitalize()))
        global current_files, current_dirs, current_subs
        current_files, current_dirs, current_subs = reload_files()
        print("Complete!")
        return True
    else:
        print('Could not recognize command "{}"!'.format(command))
        return False
# speech recognition
def listening():
    with sr.Microphone() as sauce:
        print("Listening...")
        audio = r.listen(sauce)
    print("recognizing")
    work = exe(r.recognize_google(audio))
    if not work:
        print("Something went wrong!")
        return False
    else:
        return True
# Constants
current_files, current_dirs, current_subs = reload_files()
r = sr.Recognizer()
commands = ["open directory We need to deeper", "open directory Kirby's Epic Yarn", "open directory Classical music", "open directory sponge bob",
            "open directory Super mario odyssey ", "open directory batman animated", "search youtube ethoslab", "play the chrwistman tree",
            "search someting", "play spiderman", "reload", "refresh"]

while True:
    listening()
    
