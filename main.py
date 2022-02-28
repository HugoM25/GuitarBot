#Import Some libraries
from lobe import ImageModel
from moviepy.editor import *
from pydub import AudioSegment
import cv2
import sys
import os
import glob
import argparse

#Import my libraries
import GB_NoteReading
import GB_VideoGenerator

def main() :

    #Set up some variables ---------- ---------------------------------------------

    currentDir = os.getcwd()
    errorRangeCursor = 6
    ColorCursor = (150, 235, 152)
    videoFilePath = currentDir + "\\Videos\\" + "polish_cow.mp4"
    suppTemp = True
    model = ImageModel.load(currentDir + "\\NoteClassifierV2\\NoteClassifierV4 ONNX")
    video = cv2.VideoCapture(videoFilePath)
    fps = video.get(cv2.CAP_PROP_FPS)

    # Parse the arguments
    parser = argparse.ArgumentParser(description='Informations')
    parser.add_argument('--videotab', type=str, help="Path of the video to learn from")
    parser.add_argument('--supptemp', type=bool, help="Option to delete the temp data stored to create the final video", default=True)
    parser.add_argument('--savenotes', type=bool, help="Option to save the notes images in the dataset folder", default=False)
    args = parser.parse_args()
    videoFilePath = args.videotab
    suppTemp = args.supptemp
    saveNotes = args.savenotes

    #Read the notes from the video-------------------------------------------------
    GB_NoteReading.ReadNotesFromVideo(videoFilePath,ColorCursor, errorRangeCursor, model, fps,saveNotes)

    #Generates a video from the notes---------------------------------------------
    AudioSegment.converter = r"D:\Projet_Python\ffmpeg\bin\ffmpeg.exe"

    ListeNotes = GB_VideoGenerator.readJsonSongFile("FileOutput.json")
    GB_VideoGenerator.CreateSong(ListeNotes)
    GB_VideoGenerator.CreateVidOpenCv(ListeNotes, fps=30)
    GB_VideoGenerator.CompileSoundandAudio("project.mp4", "SongresultTest.wav")

    #Erase the files used to create the final video
    if suppTemp == True :
        files = glob.glob(currentDir + "\\Temp\\*")
        for f in files:
            os.remove(f)


if __name__ == "__main__" :
    main()