##### Libraries importation

import ctypes
import keyboard
import math
import os
import time
import win32api
import win32gui

##### Path to Osu! map folder

userName = "adrie" # Put your user name here
pathToSongs = fr"C:\Users\{userName}\AppData\Local\osu!\Songs"

############### From now on, please for god sake, DO NOT TOUCH

##### Screen units

screenWidth = ctypes.windll.user32.GetSystemMetrics(0)
screenHeight = ctypes.windll.user32.GetSystemMetrics(1)

osuWidth  = 512
osuHeight = 384

##### All the functions

def osuToScreen(x, y):
    screenX = int(x / osuWidth * screenWidth)
    screenY = int(y / osuHeight * screenHeight)
    return screenX, screenY

def getMapName():
    try:
        currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if not currentWindow: # If there's no window detected
            print("No active window detected")
            return -1, -1, -1
        if "osu!" not in currentWindow.lower(): # If Osu! isn't focused
            print("Focus on the osu! window")
            return -1, -1, -1
        if currentWindow == "osu!": # If we did not choose a beatmap
            print("Choose a beatmap")
            return -1, -1, -1
        
        mapNameInformations = currentWindow.split(" - ") # We get rid of the "osu!" in the window name
        mapArtist = mapNameInformations[1] # We take the artist name
        mapNameInformations = mapNameInformations[2].split("[") # We split the difficulty and beatmap name
        mapName = mapNameInformations[0][0:-1:1] # We take the map name (and remove the extra space)
        mapDifficulty = mapNameInformations[-1][0:-1:1] # We take the map difficulty (and remove the extra space)

        print(f"Beatmap found !\n"
              f"Artist : {mapArtist}\n"
              f"Title : {mapName}\n"
              f"Difficulty : {mapDifficulty}")
        return mapArtist, mapName, mapDifficulty
    except:
        print("Something went wrong. Please try again") # Please tell me that this will never appear
        return -1

def getMapFolder(artist, title):
    # Get all folders inside Songs
    folders = [f for f in os.listdir(pathToSongs) if os.path.isdir(os.path.join(pathToSongs, f))]

    for folder in folders: # We list all folders inside the Songs folder
        if (artist.lower() in folder.lower()) and (title.lower() in folder.lower()):
            folderPath = os.path.join(pathToSongs, folder)
            print(f"Beatmap folder found !")
            return folderPath

    print("Beatmap folder not found. Please check your Song folder")
    return -1

def getMapFile(folderPath, title, difficulty):
    # Get all files inside the song folder
    for file in os.listdir(folderPath): # We check all files inside the song folder
        if (title.lower() in file.lower()) and (difficulty.lower() in file.lower()):
            print("Beatmap file found !")
            return file
    print("Beatmap file not found. Please check your folders")
    return -1

def getMapInformations(folderPath, mapFile):
    with open(os.path.join(folderPath, mapFile), encoding="utf-8") as beatmap:
        rawInformations = beatmap.read()
        return rawInformations

def translateInformations(mapInformations):
    # We take all the informations. I don't even know if I will use them...
    splittedInformations = mapInformations.split("[")
    informationsGeneral = splittedInformations[1].split("]")[1]
    informationsEditor = splittedInformations[2].split("]")[1]
    informationsMetadata = splittedInformations[3].split("]")[1]
    informationsDifficulty = splittedInformations[4].split("]")[1]
    informationsEvents = splittedInformations[5].split("]")[1]
    informationsTimingPoints = splittedInformations[6].split("]")[1]
    informationsCoulours = splittedInformations[7].split("]")[1]
    informationsHitObjects = splittedInformations[8].split("]")[1]

    HitObjects = informationsHitObjects.split("\n")[1::]
    timer = int(HitObjects[0].split(",")[2]) # We get the time of the first object and initialize the timer
    for circle in range(len(HitObjects)-1):
        HitObjects[circle] = HitObjects[circle].split(",")
        if len(HitObjects[circle]) == 6: # Spinner
            timer = hitSpinner(timer, HitObjects[circle])
        elif len(HitObjects[circle]) == 5: # Hit Circle
            timer = hitCircle(timer, HitObjects[circle])
        else: # Slider
            continue

def hitSpinner(timer, information):
    startX = int(information[0])
    startY = int(information[1])
    startTime = int(information[2])
    endTime = int(information[5])

    last = time.time()
    while timer < startTime:
        now = time.time()
        elapsed = (now - last) * 1000
        timer += elapsed
        last = now
        time.sleep(0.001)

    # Move to spinner center
    screenX, screenY = osuToScreen(startX, startY)
    win32api.SetCursorPos((screenX, screenY))
    time.sleep(0.02)

    # Press spinner key
    keyboard.press("w")

    # Spinner parameters
    spinRadius = 100
    spinsPerSecond = 5
    angle = 0

    spinnerStart = time.time()
    spinnerDuration = max(0, (endTime - startTime) / 1000 - 0.10)

    # Spin loop
    while time.time() - spinnerStart < spinnerDuration:
        angle += spinsPerSecond * 360 * 0.01
        rad = math.radians(angle)

        offsetX = int(spinRadius * math.cos(rad))
        offsetY = int(spinRadius * math.sin(rad))

        win32api.SetCursorPos((screenX + offsetX, screenY + offsetY))
        time.sleep(0.01)
    keyboard.release("w")
    win32api.SetCursorPos((screenX, screenY)) # Return cursor to center

    return endTime

def hitCircle(timer, information):
    startX = int(information[0])
    startY = int(information[1])
    startTime = int(information[2])

    last = time.time()
    while timer < startTime:
        now = time.time()
        elapsed = (now - last) * 1000
        timer += elapsed
        last = now
        time.sleep(0.001)


    # Move to circle position
    screenX, screenY = osuToScreen(startX, startY)
    win32api.SetCursorPos((screenX, screenY))
    time.sleep(0.02)

    # Press circle key
    keyboard.press_and_release("w")
    return startTime

##### Main code

keyboard.wait("x")
artist, title, difficulty = getMapName()
if not -1 in [artist, title, difficulty]:
    folderPath = getMapFolder(artist, title)
    mapFile = getMapFile(folderPath, title, difficulty)
    if mapFile != -1:
        mapRawInformations = getMapInformations(folderPath,mapFile)
        translateInformations(mapRawInformations)
    

####################
"""
256,192,1358,8,4,6530 # SPINNER (start_x, start_y, start_time, type, hitSound, end_time)
120,348,6875,6,0,B|204:384|304:332,1,160,2|2 # SLIDER
288,96,9116,5,2 # HIT CIRCLE
"""
####################