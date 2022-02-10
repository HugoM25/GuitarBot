import cv2
import os
import numpy as np
import math
from PIL import Image
from lobe import ImageModel

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

            #Write the frame (for debugging purposes)
            cv2.imwrite("MyFrames\\frame" + str(currentframe) + ".png", frame)

            currentframe += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()

    return ListImagesTab

#Calcule la distance entre deux points
def DistanceEuclidean(list1,list2):
    distance = 0
    for i in range(0,len(list1)) :
        distance += (list2[i]-list1[i])**2
    return math.sqrt(distance)

#Cherche la position du curseur vert
def CheckForCursorPos(imageArray, colorToLookFor) :

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

    if (distanceMin > 50) :
        return -1
    else :
        return iIndex

def CountFile(dir) :
    count = 0
    for path in os.listdir(dir) :
        if os.path.isfile(os.path.join(dir, path)):
            count += 1

    return  count

def GetNoteImagesLobe(imageToLook,model,CursorPosX,dimensionImage,frameNum, fps, margeApresCurseur = 3, humanHelp = False) :

    lignesPos = [13, 25, 37, 49, 61, 73]
    i = 0
    found = False
    noteListe = [0, 0, 0, 0]

    while i < len(lignesPos) and found == False:

        noteImg = imageToLook[lignesPos[i]:lignesPos[i] + dimensionImage,
                  CursorPosX + margeApresCurseur:CursorPosX + dimensionImage + margeApresCurseur]
        image = Image.fromarray(noteImg)

        resultStats = model.predict(image)

        result = resultStats.prediction

        if resultStats.labels[0][1] < 1.0 :
            if humanHelp == True :
                result = AskHumanForHelp(resultStats, imageToLook)

        print(resultStats)
        print('Note found is :' + result)
        if result != 'Data_nothing':
            chiffre = result[5:]
            image.save("D:\Projet_Python\GuitarBot_KNN\DataTrainModel\Data_"+ str(chiffre) +"\image" + str(frameNum + 30000) +".jpg")
            noteListe = [i + 1, chiffre, frameNum * (1 / fps), frameNum]
            found = True
        else:
            i += 1

    return noteListe

def AskHumanForHelp(resultStats, imageNote) :
    print("Est ce un :" + resultStats.labels[1][0])
    cv2.imshow("OK", imageNote)
    cv2.waitKey(0)

    return "Data_" + str(input("chiffre vu :"))


def WriteNotesInFile(finalNoteListe) :
    with open("MySong.txt","w") as f :
        for i in finalNoteListe :
            if i[0] != 0 :
                f.write(str(i[0]) +"," + str(i[1]) +"," + str(i[2])[0:8]+ "," + str(i[3]) +"\n")

if __name__ == "__main__" :
    currentDir = os.getcwd()

    #Initalize lobe
    model = ImageModel.load('D:\\Projet_Python\\GuitarBot_KNN\\NoteClassifierV2\\NoteClassifierV4 ONNX')
    lastPositionCursor = -2
    ColorCursor = (150, 235, 152)

    errorRangeCursor = 6
    video = cv2.VideoCapture(currentDir + "\\Videos\\Spider-Man 2 - Pizza Theme Guitar Tutorial.mp4")
    fps = video.get(cv2.CAP_PROP_FPS)
    finalNoteListe = []

    listImages = ExtractTabImagesFromVideo(currentDir + "\\Videos\\Spider-Man 2 - Pizza Theme Guitar Tutorial.mp4")


    for i in range (0, len(listImages)):
        print("Looking at frame number " + str(i))
        im = listImages[i]
        positionCursor = CheckForCursorPos(im, ColorCursor)

        if positionCursor == -1:
            print("No cursor was found. Skipping this frame...")
            pass
        elif positionCursor < lastPositionCursor + errorRangeCursor and positionCursor > lastPositionCursor - errorRangeCursor :
            print("Cursor found at the same position. Skipping this frame...")
            pass
        else:
            print("Cursor found at pos : " + str(positionCursor))
            finalNoteListe.append(GetNoteImagesLobe(im,positionCursor,11,i,fps))

        lastPositionCursor = positionCursor

    print(finalNoteListe)
    WriteNotesInFile(finalNoteListe)


