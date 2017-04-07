#!/Users/michael/anaconda/bin/python3.5

import os, shutil, re, glob
from datetime import date
from ftpLogger import statusLog, rejectLog

eventFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Events"
artFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Gallery_Exhibitions"
filmFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
rejectPath = "/Users/michael/Desktop/drive2Piction/FTPs/_Rejects"

listLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt"
rejectLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterRejectList.txt"

today = str(date.today())

with open(listLogFile,"r+",encoding="utf-8") as logged:
	loggedList = list(logged)
	allLogged = ''.join(loggedList)		

with open(rejectLogFile,"r+",encoding="utf-8") as rejects:
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
	if "Film " in filePath:
		if not base in os.listdir(filmFTPpath):
			shutil.copy(filePath,filmFTPpath)
	elif "Events " in filePath:
		if not base in os.listdir(eventFTPpath):
			shutil.copy(filePath, eventFTPpath)
	else:
		if "Exhibitions " in filePath:
			if not base in os.listdir(artFTPpath):
				shutil.copy(filePath,artFTPpath)


def rejectFile(base,filePath):
	print("Starting the rejection process...")

	# if not re.search(base,allRejects):
	if not base in allRejects:
		print("rejecting "+base)
		# HAVE TO RESET PERMISSIONS ON THESE FILES, NOT TOTALLY
		# SURE WHY, BUT THEY GET SET INCONSISTENTLY BY DRIVE (?)
		# nevermind, this keeps breaking the script. Will file this step in to-do.
		# os.chmod(filePath,0o770)
		rejectLog(base)
		for File in glob.glob(filePath):
			shutil.copy(File,rejectPath)
			# os.chmod(rejectPath+"/"+File,0o770)
	else:
		print("Already rejected")
