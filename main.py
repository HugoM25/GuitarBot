#Import Some libraries
from lobe import ImageModel
import cv2
from moviepy.editor import *
from pydub import AudioSegment
import cv2

#Import my libraries
import GB_NoteReading
import GB_VideoGenerator

def main() :

    #Set up some variables ---------- ---------------------------------------------
    currentDir = os.getcwd()
    lastPositionCursor = -2
    errorRangeCursor = 6
    ColorCursor = (150, 235, 152)
    videoFileName = "Mario Kart Wii - Coconut Mall Guitar Tutorial.mp4"
    model = ImageModel.load(currentDir + "\\NoteClassifierV2\\NoteClassifierV4 ONNX")
    video = cv2.VideoCapture(currentDir + "\\Videos\\" + videoFileName)
    fps = video.get(cv2.CAP_PROP_FPS)
    finalNoteListe = []

    #Read the notes from a video--------------------------------------------------
    listImages = GB_NoteReading.ExtractTabImagesFromVideo(currentDir + "\\Videos\\" + videoFileName)
    for i in range(0, len(listImages)):
        print("looking at frame" + str(i))
        im = listImages[i]
        positionCursor = GB_NoteReading.CheckForCursorPos(im, ColorCursor)
        if positionCursor == -1:
            print("No cursor was found. Skipping this frame...")
            pass
        elif positionCursor < lastPositionCursor + errorRangeCursor and positionCursor > lastPositionCursor - errorRangeCursor:
            print("Cursor found at the same position. Skipping this frame...")
            pass
        else:
            print("Cursor found at pos : " + str(positionCursor))
            finalNoteListe.append(GB_NoteReading.GetNoteImagesLobe(im, model, positionCursor, 11, i, fps, humanHelp=False))
        lastPositionCursor = positionCursor
    GB_NoteReading.WriteNotesInFile(finalNoteListe)

    print("Analyze of the video done. Proceeding to create the video :")
    #Generates a video from the notes---------------------------------------------
    AudioSegment.converter = r"D:\Projet_Python\ffmpeg\bin\ffmpeg.exe"
    ListeNotes = GB_VideoGenerator.readTextFile()
    print("Creation of the soundtrack in progress")
    GB_VideoGenerator.CreateSongT2(ListeNotes)
    print("Creation of the visuals in progress")
    GB_VideoGenerator.CreateVidOpenCv2(ListeNotes, seconds=2 * 60 + 20, fps=30)
    print("Final editing started")
    GB_VideoGenerator.CompileSoundandAudio("project.mp4", "SongresultTest.wav")

if __name__ == "__main__" :
    main()