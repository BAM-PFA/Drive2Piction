#! usr/bin/env python

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
	process(driveSourceFolder)
	currentAction = "time to ftp"
	File = "Ftp"
	statusLog(currentAction,root,File)
	os.chdir(ftpRoot)
	put(globPattern)
	currentAction = "done"
	statusLog(currentAction,driveSourceFolder,File)
	print((("*")*100)+"\nDONE\n"+(("*")*100))   
	# CHMOD IS NEEDED BECAUSE FILE PERMISSIONS ARE EITHER RESTRICTED
	# BY DRIVE OR COME FROM OTHER SOURCES AS RESTRICTED
	# IT COULD HAPPEN HERE AFTER EVERTHING IS DONE, OR AT THE POINT
	# OF MOVING.
	# os.chdir(rejectPath)
	# for file in os.listdir('.'):
	# 	os.chmod(file,0o770)
except:
	currentAction = "failure"
	File = "Failed to start"
	statusLog(currentAction,root,File)