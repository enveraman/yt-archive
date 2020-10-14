from googleapiclient.discovery import build
import re
import sys, os
import Songlist

'''
Param: dur - a string of the form ##H##M##S
Returns: a string of the form HH:MM:SS formatted with time conventions
'''
def format_duration(dur):
    hrs_pt = re.compile(r'(\d+)H')
    min_pt = re.compile(r'(\d+)M')
    sec_pt = re.compile(r'(\d+)S')

    hrs = hrs_pt.search(dur).group(1) if "H" in dur else "0"
    mins = min_pt.search(dur).group(1) if "M" in dur else "0"
    secs = sec_pt.search(dur).group(1) if "S" in dur else "0"

    if int(hrs) < 10:
        hrs = "0" + hrs
    if int(mins) < 10:
        mins = "0" + mins
    if int(secs) < 10:
        secs = "0" + secs

    return ":".join([hrs, mins, secs])

'''
Param: date - a string of the form __T___Z
Returns: a string of the form "YYYY/MM/DD, HH:MM:SS UTC"
'''
def format_date(date):
    date_pt = re.compile(r'^(.+)T')
    time_pt = re.compile(r'T(.+)Z')

    dt = date_pt.search(date).group(1).replace("-", "/")
    tm = time_pt.search(date).group(1)

    return dt + ", " + tm + " UTC"

'''
Param: desc - a string
Returns: desc with all instances of "\n", "\'", and "\"" replaced with "\\n", "\\'", and "\\"" respectively
- This is to allow desc to be writtene into a string in Songlist.py
'''
def format_desc(desc):
    newdesc = ""
    for ch in desc:
        if ch == "\n":
            newdesc += "\\n"
        elif ch == "\'" or ch == "\"":
            newdesc += "\\" + ch
        else:
            newdesc += ch
    return newdesc

#APITest (3 vids): PLorw3mfu-J0gEgljMVhsWcIzZYaYL29_u

playlistid = input("Enter playlist id: ") #input playlist id

api_file = os.path.join(sys.path[0], 'APIKEY.txt') #path to API key
api_txt = open(api_file, "r", encoding = "utf-8")

'''
IMPORTANT: You must obtain a YouTube API key in order to use this program.
- This video (0:00 - 5:00) gives a detailed guide of how to obtain an API key: https://www.youtube.com/watch?v=th5_9woFJmk
- Once you obtain your API key, paste it in the separate file named "APIKEY.txt", with no extra spaces or new lines
'''
api_key = api_txt.read() #get from yt
plst_id = playlistid #get from yt playlist
yt = build("youtube", "v3", developerKey = api_key)

api_txt.close()

plst_req = yt.playlists().list( #request details of type Playlist
    part = "contentDetails, snippet",
    id = plst_id
)

plst_raw = plst_req.execute()

plst_raw = plst_raw['items'][0] #list of playlist info

plst_title = plst_raw['snippet']['title']
plst_author = plst_raw['snippet']['channelTitle']
plst_authorId = plst_raw['snippet']['channelId']
plst_desc = plst_raw['snippet']['description']
plst_size = plst_raw['contentDetails']['itemCount']

nextPageToken = None #controls which page
ind = 1
newsongs = 0 #new songs since last run

songlist = Songlist.songlist.copy() #taken from Songlist.py
songids = Songlist.songids.copy()

while True:
    plst_req = yt.playlistItems().list( #requests details of each item in the playlist (not videos yet)
        part = "contentDetails, snippet",
        playlistId = plst_id,
        maxResults = 50, #50 is max vids on a page
        pageToken = nextPageToken #current page
    )

    plst_raw = plst_req.execute() #contains playlist on current page

    vid_ids = [] #video ids taken from current playlist
    pub_date = {} #keys: video ids, vals: date published

    for vid in plst_raw['items']:
        vid_ids.append(vid['contentDetails']['videoId']) #take video ids
        pub_date[vid['contentDetails']['videoId']] = vid['snippet']['publishedAt'] #take when added to playlist

    song_req = yt.videos().list( #requests details of each video in playlist
        part = "snippet, contentDetails, localizations",
        id = ",".join(vid_ids)
    )

    song_raw = song_req.execute() #contains info on each video on current page

    #formatting
    for vid in song_raw['items']:
        if vid['id'] in songids: #if already saved, skip
            continue
        
        songdict = { #constructing info on video
            "title": vid['snippet']['title'],
            "author": vid['snippet']['channelTitle'],
            "id": vid['id'],
            "date": format_date(vid['snippet']['publishedAt']),
            "dateAdded": format_date(pub_date[vid['id']]),
            "duration": format_duration(vid['contentDetails']['duration']),
            "thumbnails": vid['snippet']['thumbnails'],
            "description": vid['snippet']['description'],
        }
        
        #english localizations, if they exist
        if 'localizations' in vid.keys() and 'en' in vid['localizations'].keys():
            songdict["engTitle"] = vid['localizations']['en']['title']
            songdict["engDescription"] = vid['localizations']['en']['description']
        else:
            songdict["engTitle"] = ""
            songdict["engDescription"] = ""

        #records saved data
        songlist.append(songdict)
        songids.add(vid["id"])

        #print statement :D
        print("Processed " + str(ind) + " videos")
        ind += 1

    #goes to next page
    nextPageToken = plst_raw.get('nextPageToken')
    print("Loading next page...")
    if not nextPageToken: #exit loop if no more pages
        break

fileName = os.path.join(sys.path[0], 'Songlist.py') #path to Songlist.py
data = open(fileName, "w", encoding = "utf-8")

'''
See Templates/Songlist_blank.py for general template of Songlist.py. 
This code below just fills in that template with the saved info.
'''
data.write("playlistId = \"" + plst_id + "\"\n")
data.write("title = \"" + plst_title + "\"\n")
data.write("author = \"" + plst_author + "\"\n")
data.write("authorId = \"" + plst_authorId + "\"\n")
data.write("description = \"" + format_desc(plst_desc) + "\"\n")
data.write("size = " + str(plst_size) + " # includes unavailable videos" + "\n" )

data.write("songids = " + str(songids) + "\n")
data.write("songlist = " + str(songlist))

print("Complete")