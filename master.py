#! usr/bin/env python

from fileCheck import process
from FTPer import put
from ftpLogger import statusLog

from datetime import date
import os

today = str(date.today())

root = "/Users/michael/Desktop/Drive"
ftpRoot = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections"
thisFolder = "**"

try:
	currentAction = "initial"
	os.chdir(root)
	File = "Start"
	statusLog(currentAction,root,File)
	process(thisFolder)
	currentAction = "time to ftp"
	File = "Ftp"
	statusLog(currentAction,root,File)
	os.chdir(ftpRoot)
	put(thisFolder)
	currentAction = "done"
	statusLog(currentAction,thisFolder,File)
except:
	currentAction = "failure"
	File = "Failed to start"
	statusLog(currentAction,root,File)