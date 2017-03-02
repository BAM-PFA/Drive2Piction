#! usr/bin/env python

import os, shutil, re
from datetime import date
import glob
from pathlib import Path
from ftpLogger import statusLog

eventFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Events"
artFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_Gallery_Exhibitions"
filmFTPpath = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"

driveGlobPath = "/Users/michael/Desktop/Drive/*"
driveRoot = "/Users/michael/Desktop/Drive"
rejectPath = "/Users/michael/Desktop/drive2Piction/FTPs/_Rejects/"

listLog = "/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt"
listLogPath = Path("/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt")

today = str(date.today())

if listLogPath.is_file():
	print("the masterList exists, way to go.")
else:
	with open(listLog,"w") as List:
		List.write((("#" * 70) + (("\n#") + ((" ") * 68) + "#") * 2) + ("\n#" + (" " * 4)) + "HELLO AND WELCOME TO THE BIG LIST OF SHIT"+(" " * 23)+"#\n#" + (" " * 4)+"SENT TO PICTION VIA GOOGLE DRIVE. Started "+today+((" " * 12)+"#\n")+("#"+(" " * 68) +("#\n"))+("#" * 70)+"\n\n")

with open(listLog,"r") as read:
	textAsList = list(read)
	allText = ''.join(textAsList)		

def acceptFile(base,filePath):
	currentAction = "accepting a file"
	print(currentAction)
	statusLog(currentAction,filePath,base)
	if not re.search(base,allText):
		currentAction = "sending to Piction"
		print(base+" not in list")
		# statusLog(currentAction,pwd,base)
	else:
		currentAction = "already in Piction"
		print(base+" found in list, skipping")

	if currentAction == "sending to Piction":
		statusLog(currentAction,filePath,base)
		sortSend(base,filePath)
		with open(listLog,"a") as masterList:
			masterList.write(base+" sent to Piction on "+today+"\n")
	else:
		pass

def sortSend(base,filePath):
	if "Film" in filePath:
		shutil.copy(filePath,filmFTPpath)
	elif "Event" in filePath:
		shutil.copy(filePath, eventFTPpath)
	else:
		if "Art" in filePath:
			shutil.copy(filePath,artFTPpath)


def rejectFile(base,filePath):
	try:		
		print("moving")
		shutil.copy(filePath,rejectPath)
	except shutil.Error as error:
		randomNumber = str(randint(100,999))
		currentAction = "renaming a duplicate file"
		statusLog(currentAction,filePath,base)
		os.rename(base,rejectPath+randomNumber+"_copy-of_"+base)