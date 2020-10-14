import sys, os
import shutil
import datetime

'''
Print statement method cuz why not? (Love seeing those print statements fly by)
'''
def printlog(fileName):
    print("Copied " + fileName + " successfully")

'''
Input to where to save. Saves data to the folder "_saved/<copyinp> (CURRENT TIME)"
'''
copyinp = input("Name of folder to save info to (enter \"DELETE\" to reset without saving): ")

if copyinp == "DELETE": #do not save data
    print("Song info not saved")

#want to delete?
resetinp = input("Continue to delete data? (Y/N): ")

while resetinp != "Y" and yninp != "N": #if resetinp was not Y or N
    resetinp = input("Please enter \"Y\" to delete data, \"N\" to cancel: ")

'''
Paths to data to be saved. This saves
- Songlist.py
- SavedThumbnails.py
- Thumbnails folder (including all contents)
- Output folder (including all contents)
'''
sl = os.path.join(sys.path[0], "Songlist.py")
st = os.path.join(sys.path[0], "SavedThumbnails.py")
tn = os.path.join(sys.path[0], "Thumbnails")
ot = os.path.join(sys.path[0], "Output")

#if chose to save
if copyinp != "DELETE":
    #copy
    print("\n-Copying-\n")

    temp = str(datetime.datetime.now().replace(microsecond=0)) #current time (screw ms)
    date = temp.replace(":", "H", 1).replace(":", "M", 1) + "S" #i strongly dislike datetime :(

    des = "_saved\\" + copyinp + " (" + date + ")" #saves all data to a folder in _saved
    #creates folders to save to
    os.makedirs(os.path.join(sys.path[0], des))
    os.makedirs(os.path.join(sys.path[0], des + "\\Thumbnails"))
    os.makedirs(os.path.join(sys.path[0], des + "\\Output"))

    print("Begin archiving to " + des)

    #destination file location saves
    des_sl = os.path.join(sys.path[0], des + "\\Songlist.py")
    des_st = os.path.join(sys.path[0], des + "\\SavedThumbnails.py")
    des_tn = os.path.join(sys.path[0], des + "\\Thumbnails")
    des_ot = os.path.join(sys.path[0], des + "\\Output")

    shutil.copy(sl, des_sl) #saving Songlist.py
    printlog("Songlist.py")

    shutil.copy(st, des_st) #saving SavedThumbnails.py
    printlog("SavedThumbnails.py")

    print("\nThumbnails:")
    pics = os.listdir(tn)

    for pic in pics: #saves all pictures in Thumbnails
        curr = os.path.join(tn, pic)
        des_curr = os.path.join(des_tn, pic)
        shutil.copy(curr, des_curr)
        printlog(pic)

    print("\nOutput:")

    docs = os.listdir(ot)

    for doc in docs: #saves all files in Output
        curr = os.path.join(ot, doc)
        des_curr = os.path.join(des_ot, doc)
        shutil.copy(curr, des_curr)
        printlog(doc)

#if chose to reset
if resetinp == "Y":
    #reset
    print("\n-Resetting-\n")

    #path to templates of Songlist and SavedThumbnails
    res_sl = os.path.join(sys.path[0], "Templates\\Songlist_blank.py")
    print("Reset Songlist.py")
    res_st = os.path.join(sys.path[0], "Templates\\SavedThumbnails_blank.py")
    print("Reset SavedThumbnails.py")

    #copies templates to current files
    shutil.copy(res_sl, sl)
    shutil.copy(res_st, st)

    #remove Thumbnails and Output
    shutil.rmtree(tn)
    os.makedirs(os.path.join(sys.path[0], "Thumbnails"))
    print("Removed Thumbnails")

    shutil.rmtree(ot)
    os.makedirs(os.path.join(sys.path[0], "Output"))
    print("Removed Output")
