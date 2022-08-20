# GuitarBot

# What is it ?
Guitarbot is a command line tool to generate videos from tutorials from the youtube channel : [tab sheet music](https://www.youtube.com/c/TabSheetMusic)
<img src="https://github.com/HugoM25/GuitarBot/blob/master/example_frame.png"  />

<h2> Examples </h2> 
Videos with tabs displayed : https://youtu.be/8GiqTDT1wqc

# How to use it ?

<h2> Usage </h2>
To use this program you can use a command like this :

```Shell
python main.py --videotab your_video.mp4 --videoplay VideosToUseFolder
```

The available arguments are: 

- `--videotab` : The path to the video tutorial (only 360p videos are supported)  
- `--videoplay` : Path of the folder with the notes and sounds to use to create the final video (check setup instruction to know the correct format of the folder) 
- `--supptemp` : Contains the decision to delete/backup the temporary files used for the video (by default TRUE)
- `--savenotes` : Contains the decision to save the notes images (used for data gathering to improve the ML model)  (by default FALSE)
- `--taboverlay` : Contains the decision to show the tab with the note played on the video (by default FALSE)

<h2> Setup </h2>
You will then need to have a folder named `NoteRES` containing your audio and video recordings of each note arranged according to this layout: 

:file_folder: NotesRES 
- :file_folder: String1 
- :file_folder: String2
- :file_folder: String3
- :file_folder: String4
- :file_folder: String5
- :file_folder: String6  <-- (The lowest string)

With each string folder having the same structure as the following: 

:file_folder: StringX
- :sound: son0.wav
- :movie_camera: vid0.mp4
- ...
- ...
- :sound: son21.wav
- :movie_camera: vid21.mp4
