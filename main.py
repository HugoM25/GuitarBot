#Import Some libraries
from lobe import ImageModel
from moviepy.editor import *
from pydub import AudioSegment
import cv2
import sys
import argparse

#Import my libraries
import GB_NoteReading
import GB_VideoGenerator

def main() :

    #Set up some variables ---------- ---------------------------------------------

    currentDir = os.getcwd()
    errorRangeCursor = 6
    ColorCursor = (150, 235, 152)
    videoFilePath = currentDir + "\\Videos\\" + "tabvideo_coffin.mp4"
    model = ImageModel.load(currentDir + "\\NoteClassifierV2\\NoteClassifierV4 ONNX")
    video = cv2.VideoCapture(videoFilePath)
    fps = video.get(cv2.CAP_PROP_FPS)

    # Parse the arguments
    parser = argparse.ArgumentParser(description='Informations')
    parser.add_argument('--videotab', type=str, help="Path of the video to learn from")
    args = parser.parse_args()

    videoFilePath = args.videotab

    #Read the notes from the video-------------------------------------------------
    GB_NoteReading.ReadNotesFromVideo(videoFilePath,ColorCursor, errorRangeCursor, model, fps)
    print("Analyze of the video done. Proceeding to create the video :")

    #Generates a video from the notes---------------------------------------------
    AudioSegment.converter = r"D:\Projet_Python\ffmpeg\bin\ffmpeg.exe"

    ListeNotes = GB_VideoGenerator.readJsonSongFile("FileOutput.json")
    GB_VideoGenerator.CreateSong(ListeNotes)
    GB_VideoGenerator.CreateVidOpenCv(ListeNotes, fps=30)
    GB_VideoGenerator.CompileSoundandAudio("project.mp4", "SongresultTest.wav")

if __name__ == "__main__" :
    main()