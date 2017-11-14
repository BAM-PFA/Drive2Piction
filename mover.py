#!/Users/michael/anaconda/bin/python3.5

import os, shutil, re, glob
from datetime import date
from ftpLogger import statusLog, rejectLog
from shlex import quote

eventFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/Event_Images"
artFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/Gallery_Exhibition_Images"
filmFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/Film_Stills"
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


def sortSend(base,filePath):
	print("sorting "+base)
	if "Film " in filePath:
		if not base in os.listdir(filmFTPpath):
			shutil.copy(filePath,filmFTPpath)
			
	elif "Events " in filePath:
		if not base in os.listdir(eventFTPpath):
			# escaped = re.sub('[\ ]','\\ ',filePath)
			shutil.copy(filePath, eventFTPpath)
			
	else:
		if "Exhibitions " in filePath:
			if not base in os.listdir(artFTPpath):
				shutil.copy(filePath,artFTPpath)

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
