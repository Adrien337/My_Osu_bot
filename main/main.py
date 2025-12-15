##### Libraries importation

import keyboard
import os
import win32gui

##### Path to Osu! map folder

userName = "adrie" # Put your user name here
pathToSongs = fr"C:\Users\{userName}\AppData\Local\osu!\Songs"

##### All the functions

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
    with open(f"{folderPath}\{mapFile}") as beatmap:
        rawInformations = beatmap.read()
        return rawInformations

##### Main code

keyboard.wait("x")
artist, title, difficulty = getMapName()
if not -1 in [artist, title, difficulty]:
    folderPath = getMapFolder(artist, title)
    mapFile = getMapFile(folderPath, title, difficulty)
    if mapFile != -1:
        mapInformations = getMapInformations(folderPath,mapFile)
        print(mapInformations)
