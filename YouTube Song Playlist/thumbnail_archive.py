import requests
from SavedThumbnails import saved
from Songlist import songlist
import os, sys

'''
Chooses the highest resolution thumbnail.
Chooses in the order (first is most preferred, last is least preferred):

maxres -> standard -> high -> medium -> default

Note that thumbnails is a dictionary, and the keys of thumbnails will always contain at least
one of these strings.
'''
def bestPicture(thumbnails):
    resolutions = ["maxres", "standard", "high", "medium", "default"]
    for resol in resolutions:
        if resol in thumbnails.keys():
            url = thumbnails[resol]['url']
            return url

num = 1
newSaved = saved.copy() #set of video ids saved
for vid in songlist:
    if not vid['id'] in saved: #if this vid thumbnail has not been saved
        newSaved.add(vid['id'])

        pic = requests.get(bestPicture(vid['thumbnails'])) #url of thumbnail
        fileExt = os.path.join(sys.path[0], "Thumbnails\\" + vid['id'] + ".jpg") #path saved (of the form Thumbnails/<video id>.jpg)
        picfile = open(fileExt, "wb")

        picfile.write(pic.content) #save picture to file
        picfile.close()

        print("(" + str(num) + ") Downloaded thumbnail id " + vid['id'])
        num += 1

fileName = os.path.join(sys.path[0], 'SavedThumbnails.py') #updates set of video ids of saved thumbnails
newTN = open(fileName, "w")
newTN.write("saved = " + str(newSaved))
newTN.close()
