#!/Users/michael/anaconda/bin/python

import os
from fileCheck import process
from FTPer import put
from ftpLogger import statusLog
from datetime import date

today = str(date.today())

root = "/Users/michael/Google Drive"
ftpRoot = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections"
rejectPath = "/Users/michael/Desktop/drive2Piction/FTPs/_Rejects"

driveSourceFolder = "**/Images */**"
globPattern = "**"

try:
	currentAction = "initial"
	os.chdir(root)
	File = "Start"
	statusLog(currentAction,root,File)
	# print(os.getcwd())
	process(driveSourceFolder)
	currentAction = "time to ftp"

	File = "Ftp"
	statusLog(currentAction,root,File)
	os.chdir(ftpRoot)
	put(globPattern)
	currentAction = "done"
	statusLog(currentAction,driveSourceFolder,File)
	print((("*")*100)+"\nDONE\n"+(("*")*100))
	# I HAD PUT THE CHMOD 770 HERE AFTER EVERYTHING WAS COMPLETE,
	# BUT I MOVED IT TO THE MOVER SCRIPT. SEEMS OK THERE.
except:
	currentAction = "failure"
	File = "Failed to start"
	statusLog(currentAction,root,File)