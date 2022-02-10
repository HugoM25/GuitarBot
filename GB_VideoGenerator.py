from pydub import AudioSegment
import os
import numpy as np
import cv2
from moviepy.editor import *
import glob
from timeit import default_timer as timer

#Return the notes an their timestamp from the file
def readTextFile() :
    with open("MySong.txt", "r") as f:
        lines = f.readlines()
        Listefinale = []
        for line in lines:
            miniliste = []
            listemp = line.split(",")
            if listemp != []:
                miniliste.append(listemp[0])
                miniliste.append(listemp[1])
                miniliste.append(listemp[2][:8])
                Listefinale.append(miniliste)

    return Listefinale


def CreateSong(ListeNotes) :

    current_path = os.getcwd() + "\\"

    ChannelsSound = []
    for i in range(0, 6):
        soundChannel = AudioSegment.silent(duration=100)
        ChannelsSound.append(soundChannel)

    for i in ListeNotes:
        indexCorde = int(i[0]) - 1
        while ChannelsSound[indexCorde].duration_seconds < float(i[2]):
            ChannelsSound[indexCorde] += AudioSegment.silent(duration=1000)
        audionote = AudioSegment.from_wav(current_path + "Notes720p\\Fret" + str(i[0]) + "\\son" + str(i[1]) + ".wav")
        ChannelsSound[indexCorde] = ChannelsSound[indexCorde][:(float(i[2]) * 1000)] + audionote

    biggerIndex = 0

    for j in range(0, len(ChannelsSound)):
        if (ChannelsSound[j].duration_seconds > ChannelsSound[biggerIndex].duration_seconds):
            biggerIndex = j

    multiChannel = ChannelsSound[biggerIndex]

    for j in range(0, len(ChannelsSound)):
        if j != biggerIndex:
            multiChannel = multiChannel.overlay(ChannelsSound[j])

    multiChannel.export(current_path + "SongresultTest.wav")


def CreateSongT2(ListeNotes) :

    current_path = os.getcwd() + "\\"
    finalSoundTrack = AudioSegment.silent(duration=2000)

    audionote = AudioSegment.silent(duration=100)
    for i in ListeNotes:
        timeAjout = 0
        if finalSoundTrack.duration_seconds < float(i[2]) :
            timeAjout = float(i[2]) - finalSoundTrack.duration_seconds

        audionote = AudioSegment.from_wav(current_path + "Notes720p\\Fret" + str(i[0]) + "\\son" + str(i[1]) + ".wav")

        # Overlay addition might sound better :
        overlayNotesChannel = finalSoundTrack + AudioSegment.silent(duration=((timeAjout + audionote.duration_seconds)*1000))
        overlayNotesChannel = overlayNotesChannel.overlay(audionote,position=float(i[2])*1000, gain_during_overlay=-8)

        finalSoundTrack = overlayNotesChannel

    #Tronque au temps de la dernière note
    tempsFinal = float (ListeNotes[-1][2]) + audionote.duration_seconds
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

def CreateVidOpenCv2(listeNotes, seconds=100, fps=30.0):

    current_path = os.getcwd() + "\\"
    frameNum = 0
    lastImageFill = BlankImage(1280,720)

    #Comble le début de la vidéo avec des frames par défauts
    for i in range(0, int(fps * float(listeNotes[0][2]))):
        cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", lastImageFill)
        frameNum += 1

    for noteNum in range(0, len(listeNotes)):
        timeNote = float(listeNotes[noteNum][2])
        #Check if there is enough frames to reach the note
        if frameNum < int(fps * timeNote):
            #Complete the video until the note's time
            framesNeeded = int(fps * timeNote) - frameNum
            for j in range(0, framesNeeded):
                cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", lastImageFill)
                frameNum += 1
        #Add the frames of the note
        pathNote = current_path + "Notes720p\\Fret" + str(listeNotes[noteNum][0]) + "\\vid" + str(listeNotes[noteNum][1])  + ".mp4"
        listImgNote = ExtractImagesFromVideo(pathNote)
        for img in listImgNote:
            #if there is too much frames then add just enough to reach the notes
            if noteNum + 1 < len(listeNotes) and frameNum < int(fps* float(listeNotes[noteNum+1][2])) :
                cv2.imwrite(current_path + "Temp\\frame" + str(frameNum) + ".jpg", img)
                frameNum += 1
                lastImageFill = img
            elif noteNum +1 > len(listeNotes) :
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
    ListeNotes = readTextFile()
    CreateSong(ListeNotes)
    CreateVidOpenCv2(ListeNotes, seconds=2*60+20, fps=30)

    CompileSoundandAudio("project.mp4", "SongresultTest.wav")

def test(formatVid) :
    AudioSegment.converter = r"D:\Projet_Python\ffmpeg\bin\ffmpeg.exe"
    #Read notes from the generated file
    ListeNotes = readTextFile()
    #CreateSongT2(ListeNotes)

    CreateVidOpenCv2(ListeNotes, seconds=2*60+20, fps=30)

    #CompileSoundandAudio("project.mp4", "SongresultTest.wav")

if __name__ == "__main__" :
    test((1280,720))
    #main((1280,720))
