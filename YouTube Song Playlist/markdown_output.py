import Songlist
import datetime
import sys, os

#special characters in markdown that need to be escaped
special_ch = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']

#escapes (puts a \) behind any special characters in special_ch
def escSpec(s):
    newStr = ""
    for ch in s:
        if ch in special_ch:
            newStr += "\\"
        newStr += ch
    return newStr

#correctly formats a blockquote
def blockquote(s):
    return ">" + escSpec(s).replace("\r", "").replace("\n", "  \n>")

#takes picture from Thumbnails
def format_picture(vid_id):
    img = "<img src = \"../Thumbnails/" + vid_id + ".jpg\">"
    return "<center> \n" + img + "\n</center>\n"

'''
The next few methods are of the form "format_THING".
These determine how a certain THING is formatted in the
output document.
'''

def format_index(ind, vid_id):
    link = "https://www.youtube.com/watch?v=" + vid_id
    return "## **" + str(ind) + ".** " + link + "\n"

def format_title(title):
    return "**Title:** " + escSpec(title) + "  "

def format_author(author):
    return "**Author:** " + escSpec(author) + "  "

def format_id(vid_id):
    return "**Video ID:** " + escSpec(vid_id) + "  "

def format_date(date):
    return "**Date Published:** " + escSpec(date) + "  "

def format_duration(dur):
    return "**Duration:** " + escSpec(dur) + "  "

def format_thumbnails(thumbnails):
    thnls = "\n**Thumbnails:**  \n"
    for t in thumbnails.keys():
        thnls += t + ": " + thumbnails[t]['url'] + "  \n"
    return thnls

def format_description(desc):
    return "**Description:**  \n" + blockquote(desc)

#time now
date = str(datetime.datetime.now().date()).replace("-", "/")

#file name input
inp = input("Enter file name to export to (include .md at the end): ")

fileName = os.path.join(sys.path[0], "Output\\" + inp) #path to file
data = open(fileName, "w", encoding = "utf-8")

data.write("# **" + Songlist.title + "** - " + Songlist.author + " (Updated " + date + ")  \n\n")

if Songlist.description != "":
    data.write(Songlist.description + "  \n\n --- \n\n")

data.write("Playlist ID: " + Songlist.playlistId + "  \n")
data.write("Channel ID: " + Songlist.authorId + "  \n\n")

data.write("Total Videos: " + str(Songlist.size) + "  \n")
data.write("Available: " + str(len(Songlist.songlist)) + "  \n")
data.write("Unavailable: " + str(Songlist.size - len(Songlist.songlist)) + "  \n")

r = 1
for song in Songlist.songlist: #goes through every video
    info = [
        "\n---\n",
        format_picture(song['id']),
        format_index(r, song['id']),
        format_title(song['title']),
        format_author(song['author']),
        format_id(song['id']),
        format_date(song['date']),
        format_duration(song['duration']),
        format_thumbnails(song['thumbnails']),
        format_description(song['description']),
    ]
    data.write("\n".join(info))
    print("Processed " + str(r) + " videos")
    r += 1

data.close()
