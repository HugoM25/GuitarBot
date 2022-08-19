import cv2
import os
import numpy as np
import math
from PIL import Image
import json

#Extract frames and crop the images to get the tabs
def ExtractTabImagesFromVideo(PathToVideo) :
    cam = cv2.VideoCapture(PathToVideo)
    ListImagesTab = []
    currentframe = 0
    while (True):
        ret, frame = cam.read()
        if ret:
            frame = frame[137:223, 0:639]
            ListImagesTab.append(frame)
            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()

    return ListImagesTab

def ExtractTabImagesFromJson(dataJson) :
    notesListJson = dataJson["notes"]
    video = cv2.VideoCapture(str(dataJson["infos"]["video_tutorial_path"]))

    fps = video.get(cv2.CAP_PROP_FPS)
    for notes in notesListJson :
        frame_id = int(fps * float(notes["time"]))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = video.read()
        if ret == True :
            frame = frame[137:223, 0:639]
            cv2.imwrite('Temp\\tab' + str(frame_id) + '.jpg', frame)

    video.release()
    cv2.destroyAllWindows()

#Evaluate distance between two points
def DistanceEuclidean(list1,list2):
    distance = 0
    for i in range(0,len(list1)) :
        distance += (list2[i]-list1[i])**2
    return math.sqrt(distance)

#Look for the position of the green bar
def CheckForCursorPos(imageArray, colorToLookFor, minDist=50) :

    numRows = np.shape(imageArray)[0]
    #Sum by collumns
    imageArray = np.sum(imageArray, axis=0)
    longueur = np.shape(imageArray)[0]
    imageArray = imageArray/numRows

    distanceMin = 1000
    iIndex = 0
    for i in range(0,longueur):
        distanceAct = DistanceEuclidean(imageArray[i],colorToLookFor)
        if (distanceAct <= distanceMin) :
            distanceMin = distanceAct
            iIndex = i

    if (distanceMin > minDist) :
        return -1
    else :
        return iIndex

def CountFile(dir) :
    count = 0
    for path in os.listdir(dir) :
        if os.path.isfile(os.path.join(dir, path)):
            count += 1

    return  count


def GetNoteImagesLobe(imageToLook,model,CursorPosX,dimensionImage,frameNum, fps, margeApresCurseur = 3, humanHelp = False, saveNotes=False) :
    currentDir = os.getcwd()
    lignesPos = [13, 25, 37, 49, 61, 73]
    i = 0
    found = False
    noteListe = [0, 0, 0, 0]

    while i < len(lignesPos) and found == False:

        noteImg = imageToLook[lignesPos[i]:lignesPos[i] + dimensionImage,
                  CursorPosX + margeApresCurseur:CursorPosX + dimensionImage + margeApresCurseur]
        #Check if image's empty
        noteImgClean = noteImg < 65
        for x in range(0,len(noteImgClean)) :
            for y in range(0,len(noteImgClean[x])) :
                if np.all(noteImgClean[x][y]) != True :
                    noteImgClean[x][y] = [0,0,0]



        percentageImgNb = noteImgClean.sum()/(noteImgClean.shape[0]*noteImgClean.shape[1])


        image = Image.fromarray(noteImg)
        if percentageImgNb > 0.2 :

            resultStats = model.predict(image)
            result = resultStats.prediction
            if resultStats.labels[0][1] < 1.0 :
                if humanHelp == True :
                    result = AskHumanForHelp(resultStats, imageToLook)

            if result != 'Data_nothing':
                chiffre = result[5:]
                noteListe = [i + 1, chiffre, frameNum * (1 / fps), frameNum]

                if saveNotes :
                    nbNoteImg = (len(os.listdir("DataTrainModel\\Data_" + str(chiffre)))) + 1
                    image.save(currentDir + "\DataTrainModel\Data_"+ str(chiffre) + "\image" + str(nbNoteImg) + ".jpg" )

                found = True

        i += 1
    return noteListe

def AskHumanForHelp(resultStats, imageNote) :
    print("Est ce un :" + resultStats.labels[1][0])
    cv2.imshow("OK", imageNote)
    cv2.waitKey(0)

    return "Data_" + str(input("chiffre vu :"))


def WriteNotesInFileJson(filename,notesList,tutovid, name="songName") :
    listNotes = []
    for note in notesList :
        if note[0] != 0 :
            dictNote = {
                "corde": str(note[0]),
                "case": str(note[1]),
                "time": str(note[2])[0:8],
            }
            listNotes.append(dictNote)
    infosList = {
        "name" : "songName",
        "video_tutorial_path" : "",
        "video_tutorial_fps" : "23.98"
    }
    data = {
        "infos": infosList,
        "notes": listNotes
    }
    with open(filename,"w") as outFile :
       json.dump(data, outFile)


def ReadNotesFromVideo(videoFilePath, colorCursor, errorRangeCursor, model, fps, saveNotes=False) :
    finalNoteListe = []
    lastPositionCursor = -2
    listImages = ExtractTabImagesFromVideo(videoFilePath)

    for i in range(0, len(listImages)):

        #print("looking at frame" + str(i))
        im = listImages[i]
        positionCursor = CheckForCursorPos(im, colorCursor)
        if positionCursor == -1:
            #print("No cursor was found. Skipping this frame...")
            pass
        elif positionCursor < lastPositionCursor + errorRangeCursor and positionCursor > lastPositionCursor - errorRangeCursor:
            #print("Cursor found at the same position. Skipping this frame...")
            pass
        else:
            #print("Cursor found at pos : " + str(positionCursor))
            cv2.imwrite("Temp\\tab" + str(i) + ".jpg", listImages[i])
            finalNoteListe.append(GetNoteImagesLobe(im, model, positionCursor, 11, i, fps, humanHelp=False, saveNotes=saveNotes))
        lastPositionCursor = positionCursor


    WriteNotesInFileJson("FileOutput.json", finalNoteListe,videoFilePath)




