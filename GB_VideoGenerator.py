from pydub import AudioSegment
import numpy as np
import cv2
from moviepy.editor import *
import json

def readJsonSongFile(filename) :
    with open(filename, "r") as fileSongJson :
        data = json.load(fileSongJson)
        return data

def CreateSongT2(dataSong) :

    current_path = os.getcwd() + "\\"
    finalSoundTrack = AudioSegment.silent(duration=2000)

    audionote = AudioSegment.silent(duration=100)
    for note in dataSong["notes"]:
        timeAjout = 0
        if finalSoundTrack.duration_seconds < float(note["time"]) :
            timeAjout = float(note["time"]) - finalSoundTrack.duration_seconds

        audionote = AudioSegment.from_wav(current_path + "Notes720p\\Fret" + str(note["corde"]) + "\\son" + str(note["case"]) + ".wav")

        # Overlay addition might sound better :
        overlayNotesChannel = finalSoundTrack + AudioSegment.silent(duration=((timeAjout + audionote.duration_seconds)*1000))
        overlayNotesChannel = overlayNotesChannel.overlay(audionote,position=float(note["time"])*1000, gain_during_overlay=-8)

        finalSoundTrack = overlayNotesChannel

    #Tronque au temps de la dernière note
    tempsFinal = float (dataSong["notes"][-1]["time"]) + audionote.duration_seconds
    finalSoundTrack = finalSoundTrack[0:tempsFinal*1000]

    #Export le son
    finalSoundTrack.export(current_path + "SongresultTest.wav", format="wav")

def ExtractImagesFromVideo(PathToVideo) :
    cam = cv2.VideoCapture(PathToVideo)
    ListImagesTab = []
    currentframe = 0

    while (True):
        ret, frame = cam.read()
        if ret:
            ListImagesTab.append(frame)
            currentframe += 1
        else:
            break
    cam.release()
    cv2.destroyAllWindows()

    return ListImagesTab

def BlankImage(width = 1920, height = 1080, color = (0,0,0)) :
    img = np.zeros((height, width,3), np.uint8)
    return img

def AddTabOverImage(image, tabPath) :
    #Resize the image
    tab = cv2.imread(tabPath)
    newTabWidth = int(image.shape[1])
    newTabHeight = int(newTabWidth * (tab.shape[0]/tab.shape[1]))
    resizedTab = cv2.resize(tab, (newTabWidth, newTabHeight), interpolation=cv2.INTER_AREA)

    xOffset = 0
    yOffset = image.shape[0]-resizedTab.shape[0]

    image[yOffset:yOffset + resizedTab.shape[0], xOffset:xOffset + resizedTab.shape[1]] = resizedTab

    return image

def WriteVideoOpenCv(pathFolderImages, numberofFrames) :
    img_array = []
    size = (1280,720)
    for i in range(0,numberofFrames) :
        #print(pathFolderImages + "frame" + str(i) + ".jpg")
        img = cv2.imread(pathFolderImages + "frame" + str(i) + ".jpg")
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)


    #out = cv2.VideoWriter(filename='project.avi', fourcc=cv2.VideoWriter_fourcc(*'DIVX'), fps=30, frameSize=size)
    out = cv2.VideoWriter(filename='project.mp4', fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=30, frameSize=size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def WriteVideo(pathFolderImages, numberOfFrames, fps=30.0) :
    image_files = []
    for i in range(0, numberOfFrames) :
        image_files.append(pathFolderImages + "frame" + str(i) +".jpg")
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile('project.mp4', codec="libx264", remove_temp= True, fps=fps)

def CreateVidOpenCv2(dataSong, fps=30.0):

    current_path = os.getcwd() + "\\"
    frameNum = 0
    lastImageFill = BlankImage(1280,720)

    #Comble le début de la vidéo avec des frames par défauts
    for i in range(0, int(fps * float(dataSong['notes'][0]['time']))):
        cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", lastImageFill)
        frameNum += 1

    for noteNum in range(0, len(dataSong['notes'])):
        timeNote = float(dataSong['notes'][noteNum]['time'])
        #Check if there is enough frames to reach the note
        if frameNum < int(fps * timeNote):
            #Complete the video until the note's time
            framesNeeded = int(fps * timeNote) - frameNum
            for j in range(0, framesNeeded):
                cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", lastImageFill)
                frameNum += 1
        #Add the frames of the note
        pathNote = current_path + "Notes720p\\Fret" + str(dataSong["notes"][noteNum]['corde']) + "\\vid" + str(dataSong["notes"][noteNum]['case'])  + ".mp4"

        listImgNote = ExtractImagesFromVideo(pathNote)
        for img in listImgNote:
            img = AddTabOverImage(img, current_path + "Temp\\" + str(dataSong["notes"][noteNum]['tab']))
            #if there is too much frames then add just enough to reach the notes
            if noteNum + 1 < len(dataSong['notes']) and frameNum < int(fps* float(dataSong['notes'][noteNum+1]['time'])) :
                cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", img)
                frameNum += 1
                lastImageFill = img
            elif noteNum +1 > len(dataSong['notes']) :
                cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", img)
                lastImageFill = img
                frameNum += 1
    WriteVideo(current_path + "Temp\\", frameNum, fps)



def CompileSoundandAudio(pathFileVideo, pathFileAudio) :
    finalVid =  VideoFileClip(pathFileVideo)
    finalAudio = AudioFileClip(pathFileAudio)

    new_audioClip = CompositeAudioClip([finalAudio])

    finalVid = finalVid.set_audio(new_audioClip)
    finalVid.write_videofile("finalVideo.mp4", codec='libx264', audio_codec="aac")



def main(formatVid) :
    AudioSegment.converter = r"D:\Projet_Python\ffmpeg\bin\ffmpeg.exe"
    #Read notes from the generated file
    #ListeNotes = readJsonSongFile("FileOutput.json")
    #print(ListeNotes)
    #CreateSongT2(ListeNotes)
    #CreateVidOpenCv2(ListeNotes, fps=30)
    #CompileSoundandAudio("project.mp4", "SongresultTest.wav")

if __name__ == "__main__" :
    main((1280,720))

