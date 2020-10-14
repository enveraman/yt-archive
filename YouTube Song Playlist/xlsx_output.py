import Songlist
import xlsxwriter #need to download, use "pip install XlsxWriter"
import sys, os
import datetime

#file name input
inp = input("Enter file name to export to (include .xlsx at the end): ")

#note: cannot edit an existing xlsx file with XlsxWriter
fileName = os.path.join(sys.path[0], "Output\\" + inp)
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()

#now
date = str(datetime.datetime.now().date()).replace("-", "/")

bold = workbook.add_format({'bold': True}) #bold typeset

#prelim info
worksheet.write(0, 0, Songlist.title + " - " + Songlist.author + " (Updated " + date + ")")
worksheet.write(1, 0, "Playlist ID: " + Songlist.playlistId)
worksheet.write(2, 0, "Total videos: " + str(Songlist.size) + "; Available: " + str(len(Songlist.songlist)) + "; Unavailable: " + str(Songlist.size - len(Songlist.songlist)))

#categories
worksheet.write(4, 0, "Video Title", bold)
worksheet.write(4, 1, "Author", bold)
worksheet.write(4, 2, "Thumbnail", bold)
worksheet.write(4, 3, "Video", bold)
worksheet.write(4, 4, "Video ID", bold)
worksheet.write(4, 5, "Date Published", bold)
worksheet.write(4, 6, "Duration", bold)
worksheet.write(4, 7, "Date Added", bold)
worksheet.write(4, 8, "English Title (if any)", bold)

row = 5
col = 0

#spacing
worksheet.set_column(0, 0, 100)
worksheet.set_column(1, 1, 40)
worksheet.set_column(2, 2, 10)
worksheet.set_column(3, 3, 10)
worksheet.set_column(4, 7, 25)
worksheet.set_column(8, 8, 100)

for vid in Songlist.songlist: #all songs
    worksheet.write(row, 0, vid['title'])
    worksheet.write(row, 1, vid['author'])

    pic = "..\\Thumbnails\\" + vid['id'] + ".jpg"
    worksheet.write_url(row, 2, pic, string = "TN")
    worksheet.write_url(row, 3, "https://www.youtube.com/watch?v=" + vid['id'], string = "VD")

    worksheet.write(row, 4, vid['id'])
    worksheet.write(row, 5, vid['date'])
    worksheet.write(row, 6, vid['duration'])
    worksheet.write(row, 7, vid['dateAdded'])
    worksheet.write(row, 8, vid['engTitle'])
    row += 1
    
    print("Processed " + vid['id'])

workbook.close()