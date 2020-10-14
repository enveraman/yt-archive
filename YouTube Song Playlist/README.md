# YouTube Song Playlist

### Author: Enver Aman

## Description

Given a YouTube playlist ID, this project requests information from Google's YouTube API, and formats playlist information, noteably videos in the playlist, into a python file, from which it is easier to manipulate to analyze such data.

Please note that, in order for correct compliation of all programs, files should be run in *this* order:

```song_archive.py -> thumbnail_archive.py -> markdown_output.py / xlsx_output.py (or any other _output file)```

---

## **IMPORTANT**

You must obtain a YouTube API key in order to use this program. This video (0:00 - 5:00) gives a detailed guide of how to obtain an API key: https://www.youtube.com/watch?v=th5_9woFJmk.

Once you obtain your API key, paste it in the file named ```APIKEY.txt```, with **no extra characters, spaces, or new lines**. Replace the placeholder text there, ***all of it***. Your API key should start with ```AI``` followed by a series of letters and digits. For example, if your API key is ```AIe1L2p3M4a5X6e```, then the file ```APIKEY.txt``` should consist of **ONLY** this:

```AIe1L2p3M4a5X6e```

and ***NOTHING ELSE!!!***

This step is _crucial_, otherwise ```song_archive.py``` will not run correctly.

An explanation: The YouTube API key is used to request YouTube information from Google. ```song_archive.py``` will be the only file that uses the API key.

However, please note that overusing the API key in a single day will incur charges on the owner of the API key (probably won't be an issue, but please don't use ```song_archive.py``` on 1,000 video long playlists 100 times a day). As of 10/13/2020, the daily quota limit on a free Google API key is 10,000 units.

More technically, given a playlist with $n$ videos, ```song_archive.py``` requires $1 + 2\lceil n/50 \rceil$ units (of API requests I guess), where $\lceil x \rceil$ is the smallest integer larger than or equal to $x$ (basically $x$ when you round up). That means that you can archive playlists with up to $249,950$ videos per day (only once though)!

---

## Files

### ```_archive``` files:

```song_archive.py```: Please see the **IMPORTANT** note above. You must have an API key from Google in order to continue.

This file takes in as an input a YouTube playlist ID and creates the python file ```Songlist.py```, which contains detailed information about the inputted playlist along with the videos in the playlist. See below for more detailed information.

```thumbnail_archive.py```: Given a valid ```Songlist.py``` file (one generated from ```song_archive.py```), this file downloads the largest resolution thumbnail image from each video in the playlist used to generate ```Songlist.py```. These images are downloaded to the ```Thumbnails``` folder.

This file also generates the file ```SavedThumbnails.py```, which lists the video IDs of the videos whose thumbnails have been downloaded, so as to avoid unnecessary repeated downloads.

```copyreset_archive.py```: Copies the files ```Songlist.py``` and ```SavedThumbnails.py```, and the folders ```Thumbnails``` and ```Output```, and moves these to a folder in the folder ```_saved```. The folder the information is moved to is named by the user and contains the date and time it was moved.

For example, the user may input "Archive" to name their folder, so the program will save the data to the folder ```Archive (8/16/2020 14:42:01)```, where, of course, the date and time will be current to when the file is run.

### ```_output``` files:

```markdown_output.py```: Given a valid ```Songlist.py``` file, this file creates a markdown file that gives a nice way to see view information in ```Songlist.py```. An example of what this file produces is contained in ```markdown_sample.md```.

The markdown file generated is saved in the ```Output``` folder.

```xlsx_output.py```: Given a valid ```Songlist.py``` file, this file produces an xlsx (Excel) file that gives much of the information in ```Songlist.py``` in a spreadsheet form. An example of what this file produces is contained in ```xlsx_sample.xlsx```.

The xlsx file generated is saved in the ```Output``` folder.

**NOTE**: For this program to correctly work, you need to install ```XlsxWriter```. You can use pip to install this: in your command prompt, type in ```pip install XlsxWriter```.

### Template (```_blank```) files:

These include all files in the ```Templates``` folder, which has the two files ```Songlist_blank.py``` and ```SavedThumbnails_blank.py```. When ```copyreset_archive.py``` is run, it uses these two files as templates for ```Songlist.py``` and ```SavedThumbnails```.

---

## ```Songlist.py```

Contains detailed information about an inputted playlist and its videos. Here is its format.

Variables:
- ```playlistId```: youtube playlist id    
- ```title```: title of playlist  
- ```author```: channel who made playlist  
- ```authorId```: youtube channel id for author  
- ```description```: description of playlist  
- ```size```: number of videos in playlist, including unavailable ones  
- ```songlist```: (see more)  

The variable ```songlist``` is an array of dictionarys. Each dictionary in the array represents one video. The format of each dictionary is as such:

```python
{
    'title': (string),
    'engTitle': (string),
    'author': (string),
    'id': (string),
    'date': (string),
    'dateAdded': (string)
    'duration': (string),
    'thumbnails': (dictionary),
    'description': (string),
    'engDescription': (string),
}
```

```'title'``` - title of video

```'engTitle'``` - english version of the title of the video, if it exists. If it doesn't, this value is an empty string

```'author'``` - channel name of channel who posted the video

```'id'``` - video id

```'date'``` - the day and time the video was released, formatted as "YYYY/MM/DD, (time) UTC"

```'dateAdded'``` - the day and time the video was added to the playlist, formatted as "YYYY/MM/DD, (time) UTC"

```'duration'``` - length of video, formatted as "HH:MM:SS"

```'thumbnails'``` - dictionary of various thumbnail resolutions. Within this dictionary, the possible keys are ```'maxres'```, ```'standard'```, ```'high'```, ```'medium'```, ```'default'```, where each key corresponds to a thumbnail resolution, which contains another dictionary (note that a dictionary within ```'thumbnails'``` may not have all of the 5 possible keys, but contains at least one). The format of each thumbnail resolution dictionary is as follows,

```python
{
    'url': (string)
    'width': (int)
    'height': (int)
}
```

Here, ```'url'``` contains a link to the image, and ```'width'``` and ```'height'``` give the dimensions of the image. 

```'description'``` - description of video

```'engDescription'``` - english version of the description, if it exists, otherwise this is an empty string

Be sure to extend whatever program you use to unicode/utf-8, many videos may contain non-ASCII characters.

---

## ```SavedThumbnails.py```

Contains a set named ```saved``` of video IDs (strings). Each member of this set has its highest resolution thumbnail saved in the ```Thumbnails``` folder.

---

I put some sample archives generated in the ```_saved``` folder. In particular, the folders ```APITest``` and ```Kagerou Project``` (huge fan of Kagepro btw :D) are some sample exports generated by ```copyreset_archive.py```. They each contain a Markdown output document and an Excel output spreadsheet.

Their corresponding playlist IDs are the following:

APITest: PLorw3mfu-J0gEgljMVhsWcIzZYaYL29_u

Kagerou Project: PLc3ovJ5PZjKRleiWwSlIBMtql8nYISZaJ

Enjoy!