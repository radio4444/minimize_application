import time
import ctypes
import pygetwindow as gw 

import os
import sys

# Get the absolute path of the folder where your script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to that folder
os.chdir(script_dir)

# --- CONFIG ---
# TARGET_TITLES = ["Chrome", "Notepad"]
TARGET_TITLES = ["Chrome"]
IDLE_THRESHOLD_MINUTES = 0.10
CHECK_INTERVAL = 0.5 
# --------------

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

def main():
    threshold_seconds = IDLE_THRESHOLD_MINUTES * 60
    already_minimized = False
    print(f"Monitoring Titles: {TARGET_TITLES}")

    while True:
        idle_sec = get_idle_duration()
        if idle_sec >= threshold_seconds:
            if not already_minimized:
                for title in TARGET_TITLES:
                    for window in gw.getWindowsWithTitle(title):
                        if not window.isMinimized:
                            window.minimize()
                already_minimized = True
        else:
            already_minimized = False
        time.sleep(CHECK_INTERVAL)

print("Hello", file=open("proof.txt", "a"))

