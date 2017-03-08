#! usr/bin/env python

import os, shutil, re, glob
from datetime import date
# from pathlib import Path
from ftpLogger import statusLog, rejectLog

eventFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Events"
artFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Gallery_Exhibitions"
filmFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
rejectPath = "/Users/michael/Desktop/drive2Piction/FTPs/_Rejects/"

listLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt"
rejectLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterRejectList.txt"

today = str(date.today())

with open(listLogFile,"r") as logged:
	loggedList = list(logged)
	allLogged = ''.join(loggedList)		

with open(rejectLogFile,"r") as rejects:
	rejectList = list(rejects)
	allRejects = ''.join(rejectList)

def acceptFile(base,filePath):
	currentAction = "accepting a file"
	print(currentAction)
	statusLog(currentAction,filePath,base)
	if not re.search(base,allLogged):
		currentAction = "sending to Piction"
		print(base+" not in list")
		statusLog(currentAction,filePath,base)
		sortSend(base,filePath)

	else:
		currentAction = "already in Piction"
		print(base+" found in list, skipping")
		statusLog(currentAction,filePath,base)


def sortSend(base,filePath):
	if "Film" in filePath:
		if not base in os.listdir(filmFTPpath):
			shutil.copy(filePath,filmFTPpath)
	elif "Event" in filePath:
		if not base in os.listdir(eventFTPpath):
			shutil.copy(filePath, eventFTPpath)
	else:
		if "Art" in filePath:
			if not base in os.listdir(artFTPpath):
				shutil.copy(filePath,artFTPpath)


def rejectFile(base,filePath):
	if not base in os.listdir(rejectPath):
		if not re.search(base,allRejects):
			print("rejecting"+filePath)
			# HAVING THIS CHMOD HERE BROKE THINGS, BUT I STILL NEED TO CHANGE PERMISSIONS. COPYING
			# FROM THE DRIVE FOLDER KEEPS SOME STUPID PERMISSIONS AND I CAN'T RENAME REJECTED FILES.
			# MAYBE COULD PUT THIS IN THE MASTER SCRIPT AFTER EVERYTHING IS DONE?
			os.chmod(filePath,0o770)
			rejectLog(base)
			shutil.copy(filePath,rejectPath)
	else:
		print("Already rejected")
