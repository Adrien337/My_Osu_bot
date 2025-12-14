##### Libraries importation

import keyboard
import os
import win32gui

##### Path to Osu! map folder

userName = "" # Put your user name here
pathToSongs = fr"C:\Users\{userName}\AppData\Local\osu!\Songs"


##### All the functions

def getMapName():
    try:
        currentWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if not currentWindow: # If there's no window detected
            print("No active window detected")
            return -1
        if "osu!" not in currentWindow.lower(): # If Osu! isn't focused
            print("Focus the osu! window")
            return -1
        if currentWindow == "osu!": # If we did not choose a beatmap
            print("Choose a beatmap")
            return -1
        
        mapNameInformations = currentWindow.split(" - ") # We get rid of the "osu!" in the window name
        mapArtist = mapNameInformations[1] # We take the artist name
        mapName = mapNameInformations[2].split("[")[0] # We take the beatmap name after getting rid of the beatmap creator

        return mapArtist, mapName
    except:
        print("Something went wrong. Please try again") # Please tell me that this will never appear
        return -1

def getMapInfos(artist, title): # Don't work properly. I think I know the reason it don't work.
    # Get all folders inside Songs
    folders = [f for f in os.listdir(pathToSongs) if os.path.isdir(os.path.join(pathToSongs, f))]

    for folder in folders:
        if (artist.lower() in folder.lower()) and (title.lower() in folder.lower()):
            folder_path = os.path.join(pathToSongs, folder)
            print(f"Beatmap found! The folder is {folder_path}")
            return folder_path

    print("Beatmap not found. Please check your folders")
    return -1

##### Main code

keyboard.wait("x")
artist, title = getMapName()
print(f"Artist : {artist}")
print(f"Title : {title}")

getMapInfos(artist, title)