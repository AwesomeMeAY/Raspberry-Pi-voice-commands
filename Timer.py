import sys 
import os
import subprocess
import datetime
from time import sleep
class Timer():
    def __init__(self, time, forever=False):
        # Time = an int (950) 50 is the minute (time[-2:]) and the hour is 9 (time[:-2])
        self.time = datetime.timedelta(hours=int(time[:-2]), minutes=int(time[-2:]))

        requested_minute = self.time.seconds // 60 % 60

        requested_hour = self.time.seconds // 3600

        present_time = datetime.datetime.now().time()
        # Will continue until the time matches
        if forever:
            while True:
                while not(present_time.hour == requested_hour and present_time.minute == requested_minute):
                    present_time = datetime.datetime.now().time()
                subprocess.call(["xdg-open", os.path.join(os.getcwd(), "alarm.mp3")])
                sleep(60)
        else:
            while not(present_time.hour == requested_hour and present_time.minute == requested_minute):
                    present_time = datetime.datetime.now().time()
            subprocess.call(["xdg-open", os.path.join(os.getcwd(), "alarm.mp3")])
            return None
            

if __name__ == "__main__":
    try:
        if len(sys.argv)-1 == 2:            
            Timer(sys.argv[1], bool(sys.argv[2]))
        else:
            Timer(sys.argv[1])
    # Exception incase no arguments are given on terminal
    except IndexError:
        pass
