import pyautogui
import pyttsx3
from time import sleep
from subprocess import call
def switch_audio_device(audio_device):
    # Click the audio menu
    pyautogui.click(x=1275, y=15, button='right')
    # It takes a while on a raspberry pi
    sleep(1)
    # Click audio drop down
    pyautogui.click(1285, 45)
    # Click audio device
    pyautogui.click(1085 , 115) if audio_device == "bluetooth" else pyautogui.click(1045, 75)
    # Wait while it switches
    sleep(3)
    print(f"Switched audio device to {audio_device}")
    engine = pyttsx3.init()
    engine.say(f"Switched audio device to {audio_device}")
    engine.runAndWait()
    return 1


