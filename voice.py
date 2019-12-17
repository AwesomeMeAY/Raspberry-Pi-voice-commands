import os
import webbrowser
import subprocess
import speech_recognition as sr
from time import sleep
from difflib import get_close_matches

# defining functions that are used 
def reload_files():
    """ Order is: files, directories,then paths."""
    found_files = []
    found_dirs = []
    found_paths = []
    for paths, dirs, files in os.walk(os.getcwd()):
        found_files += files
        found_dirs += dirs
        found_paths += paths
    return found_files, found_dirs, found_paths

def find_path(file):
    for path, dirs, files in os.walk(os.getcwd()):
            for f in files:
                if f == file:
                    return os.path.join(path, file)
            for d in dirs:
                if d == file:
                    return os.path.join(path, file)

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
        else:
            return get_close_matches(directory, dir_list)[0]                           
    except:
        print('Could not find directory "{}"!'.format(directory))

def exe(command):
    duckurl = "https://www.duckduckgo.com/?q="
    command = command.lower()
    order = command.split()[0]
    if order == "search":
        website = command.split()[1]
        # if command.split()[1] in websites then it will search the website
        # instead of googling it.
        if website in websites:
            webbrowser.open("{}{} {}".format(duckurl, websites[website], command[command.index(command.split()[2]):]))
            return True
        else:
            webbrowser.open(duckurl + command[command.index(command.split()[1]):])
            return True
    elif "open directory" in command:
        combined_dir =  dir_search(command[command.index(command.split()[2]):])
        for sub_dir, dirs, files in os.walk(os.getcwd()):
            if combined_dir in sub_dir:
                subprocess.call(["xdg-open",sub_dir])
                return True
    elif order == "play":
        #this will play movies
        file = file_search(command[command.index(command.split()[1]):])
        subprocess.call(["xdg-open",find_path(file)])
        return True
    
    elif order == "add":
        # The second letter will be the webbsite third will be the bang
        websites[command.split()[1]] = command.split()[2]
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
    command_worked = exe(r.recognize_google(audio))
    if not command_worked:
        print("Something went wrong!")
        return False
    else:
        return True
# Constants
current_files, current_dirs, current_subs = reload_files()
r = sr.Recognizer()
websites = {"youtube":"!you"}

while True:
    listening()    
    
