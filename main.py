#Import Some libraries
from lobe import ImageModel
import os
import glob
import argparse
import time
#Import my libraries
import GB_NoteReading
import GB_VideoGenerator

def main() :
    #Set up some variables -------------------------------------------------------
    currentDir = os.getcwd()
    errorRangeCursor = 6
    ColorCursor = (150, 235, 152)
    model = ImageModel.load(currentDir + "\\NoteClassifierV2\\NoteClassifierV4 ONNX")


    # Parse the arguments
    parser = argparse.ArgumentParser(description='Informations')
    parser.add_argument('--videotab', type=str, help="Path of the video to learn from")
    parser.add_argument('--videoplay', type=str, help="Path of the notes and sounds to use to create the final video")
    parser.add_argument('--supptemp', type=bool, help="Option to delete the temp data stored to create the final video", default=True)
    parser.add_argument('--savenotes', type=bool, help="Option to save the notes images in the dataset folder", default=False)
    parser.add_argument('--notesjson', type=str, help="Path to an already generated (or custom) json file to use", default="nothing")

    args = parser.parse_args()
    videoFilePath = args.videotab
    suppTemp = args.supptemp
    saveNotes = args.savenotes
    videoPlayPath = args.videoplay
    notesJson = args.notesjson

    #Read the notes from the video-------------------------------------------------

    start_time = time.time()
    if notesJson == "nothing" :
        GB_NoteReading.ReadNotesFromVideo(videoFilePath,ColorCursor, errorRangeCursor, model,saveNotes)
        dataSong = GB_VideoGenerator.readJsonSongFile("FileOutput.json")
    else :
        dataSong = GB_VideoGenerator.readJsonSongFile(notesJson)
        GB_NoteReading.ExtractTabImagesFromJson(dataSong)
    print("Notes extracted in " + str( time.time() - start_time) + "s")

    #Generates a video from the notes---------------------------------------------
    start_time = time.time()
    GB_VideoGenerator.CreateSong(dataSong, videoPlayPath)
    GB_VideoGenerator.CreateVidOpenCv(dataSong, videoPlayPath, fps=30)
    GB_VideoGenerator.CompileSoundandAudio("project.mp4", "SongresultTest.wav")

    #Erase the files used to create the final video
    if suppTemp == True :
        files = glob.glob(currentDir + "\\Temp\\*")
        for f in files:
            os.remove(f)
    print("Video generated in " + str(time.time() - start_time) + "s")

if __name__ == "__main__" :
    main()