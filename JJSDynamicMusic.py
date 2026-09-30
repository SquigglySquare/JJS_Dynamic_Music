import time 
import pyautogui
import pygame
import keyboard
import random
from pathlib import Path
import glob

pygame.init()
pygame.mixer.init()

passiveVolume = 0
aggroVolume = 0

dynamicMusic = script_dir = Path(__file__).resolve().parent
print(dynamicMusic)
config = dynamicMusic / "Config.txt"
aggroFolder = dynamicMusic / "AggressiveMusic"
passiveFolder = dynamicMusic / "PassiveMusic"
aggroList = []
passiveList =  []
for file in aggroFolder.glob("*.mp3"):
    aggroList.append(file)
for file in passiveFolder.glob("*.mp3"):
    passiveList.append(file)
print(aggroList)
print(passiveList)
#music choices

with open(config,"r",encoding="utf-8") as file:
    lines = file.readlines()
    passiveVolume = float(lines[1])
    aggroVolume = float(lines[2])

stopMusicBind = "-"
startMusicBind = "]"
kill = "["
passiveDelay = 2

state = 0
toggle = True
global current_color
current_color = (0,0,0)
lastState = 0

check_x = 1901
check_y = 34

target = (0,0,0)    

print("Monitoring position (" , check_x,", ", check_y,") for rgb (",target,")")

def shuffle(type):
    match type:
        case 0:
            pygame.mixer.music.set_volume(passiveVolume)
            pygame.mixer.music.load(passiveList[random.randint(0,len(passiveList)-1)])

        case 1:
            pygame.mixer.music.set_volume(aggroVolume)
            pygame.mixer.music.load(aggroList[random.randint(0,len(aggroList)-1)])
        case _:
            print("INVALID SHUFFLE TYPE")

def setState(st):
    if st == 0:
        pygame.mixer.music.set_volume(0.2)
        shuffle(0)
        pygame.mixer.music.play(loops=0) #passive music here   
    else:
        pygame.mixer.music.set_volume(0.4)
        shuffle(1)
        pygame.mixer.music.play(loops=0) #Aggro music here

while toggle == True:
    current_color = pyautogui.pixel(check_x, check_y)

    if keyboard.is_pressed(stopMusicBind):  # if key '-' is pressed 
        print('music stopped')
        pygame.mixer.music.unload()

    if keyboard.is_pressed(startMusicBind):  # if key ']' is pressed 
        print('music force started')
        setState(state)

    if not pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() == -1:
        setState(state)

    if current_color == target:
        print("IN COMBAT")
        state = 1
        if state != lastState:
            setState(1)
        lastState = 1
    else:
        state = 0
        if state != lastState:
            start_time = None
            print("PASSIVE ATTEMPT")
            for i in range (20):
                current_color = pyautogui.pixel(check_x, check_y)
                if current_color != target:
                    if i == 19:
                        print("OUT OF COMBAT")
                        setState(0)
                        lastState = 0
                    else:
                        print(i)
                else:
                    break
                time.sleep(0.1)

    if keyboard.is_pressed("+"):
        print("toggle off")
        toggle = False

    time.sleep(0.1)

while toggle == False:
    if keyboard.is_pressed("+"):
        print("toggle on")
        toggle = True

    time.sleep(0.1)

