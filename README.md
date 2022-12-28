<h1 align="center"> GuitarBot </h1>
<img align="center" width="100%" src="https://github.com/HugoM25/GuitarBot/blob/master/example_frame.png"  />

<!-- Table of Contents -->
# Table of Contents
- [About the Project](#about-the-project)
  * [Context](#context)
  * [Made with](#made-with)
  * [Features](#features)
- [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Files Required](#files-required)
- [Usage](#usage)
  * [Commands](#commands)
- [Examples](#examples)
- [License](#license)
- [Author](#author)



# About the project

## Context
 Guitarbot is a command line tool to generate videos from tutorials from the youtube channel : [tab sheet music](https://www.youtube.com/c/TabSheetMusic)

## Made with 

 This program is made 100% in python
 
## Features

 It allows you to generate videos of yourself playing guitar from video tutorials in a matter of minutes. You can generate videos from .json files respecting the format used by this program or use a video from the youtube channel : [tab sheet music](https://www.youtube.com/c/TabSheetMusic) with 360p resolution

# Getting started

## Prerequisites

You need to have python 3.X installed on your computer. You will also need the libraries listed in the requirements.txt file.

## Installation 

 1. Clone the repository and unzip the folder
 2. Install the libraries listed in requirements.txt  

## Files required
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

# Usage

## Commands 

To use this program you can use a command like this :

```Console
python main.py --videotab your_video.mp4 --videoplay VideosToUseFolder
```

The available arguments are: 

- `--videotab  ` : The path to the video tutorial (only 360p videos are supported)  
- `--videoplay ` : Path of the folder with the notes and sounds to use to create the final video (check setup instruction to know the correct format of the folder) 
- `--supptemp  ` : Contains the decision to delete/backup the temporary files used for the video (by default TRUE)
- `--savenotes ` : Contains the decision to save the notes images (used for data gathering to improve the ML model)  (by default FALSE)
- `--taboverlay` : Contains the decision to show the tab with the note played on the video (by default FALSE)


# Examples 

Videos with tabs displayed : https://youtu.be/8GiqTDT1wqc

Videos with edited background : https://youtu.be/g3jxPjvE8ag

# License 

Distributed under the MIT License. 

# Author 

- [@HugoM25](https://github.com/HugoM25/)
