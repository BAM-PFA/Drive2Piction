#!/Users/michael/anaconda/bin/python

from datetime import date
from glob import glob
from random import randint
from ftpLogger import statusLog
from mover import acceptFile, rejectFile
from pathlib import Path

import os, re, shutil, datetime, time

today = str(date.today())
timeStamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d:%H:%M:%S:%f'))

year = "((19|20)*([0-9]{2}|[0-9]{4})+)" # matches optional century, has to have either 2 or 4 digits
month = "(0[1-9]|1[012])"
day = "(0[1-9]|[12][0-9]|3[01])*" # day is optional
wordMonths = "((jan[a-z]*)|(feb[a-z]*)|(mar[a-z]*)|(apr[a-z]*)|(may[a-z]*)|(jun[a-z]*)|(jul[a-z]*)|(aug[a-z]*)|(sep[a-z]*)|(oct[a-z]*)|(nov[a-z]*)|(dec[a-z]*))"

filmPath = "Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
eventPath = "Research_Hub_Collections/RH_Events"
exhibitionPath = "Research_Hub_Collections/RH_Gallery_Exhibitions"
# ftpPath = "/Users/michael/Desktop/testingFolders/ftpFolder/" # I USED THIS PATH TO TEST THE FILE CHECKER.
															   # ONCE THE FILE CHECKER WAS COMPLETE I COULD PASS FILES
															   # TO THE FTP SCRIPT INSTEAD.

yyyymmdd = year+"-*"+month+"-*"+day # since day is optional this also covers yyyymm
mmddyyyy = month+"-*"+day+"-*"+year # since day is optional this also covers mmyyyy
wordmonthYear = wordMonths+"-*"+day+"-*"+year+"*"
yearWordmonth = year+"-*"+wordMonths+"-*"+day

imageTypes = [".jpg",".JPG",".tif",".TIF",".jpeg",".JPEG",".tiff",".TIFF",".png",".PNG"]
combinedDateFormats = re.compile(r''+'.*_(('+year+')|('+yyyymmdd+')|('+mmddyyyy+')|('+wordmonthYear+')|('+yearWordmonth+'))_.*',re.IGNORECASE)
filmRegex = re.compile(r'^([a-z]+)(\_|-)*([a-z0-9]*(\_|-))*(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
eventRegex = re.compile(r'^(event)_(([a-z]|[0-9])*(\_|-))+(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
exhibitionRegex = re.compile(r'(([a-z]|[0-9])*(\_|-))+(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
badCharacterRegex = re.compile(r'(.*)(\$|%|\^|&|\*|#|@|!|\)|\(|\*|\+|=|\ |á|à|ä|å|À|Á|è|é| \
					ê|ë|È|É|Ò|Ó|Ö|ò|ó|ô|ö|â|ì|í|Ì|Í|î|ü|Ü|Ú|Ù|ù|ú|©|¿|\?|\“| \
					\”|\"|\/|\’|\‘|\'|\´|\`|¨|\')(.*)',re.IGNORECASE) # WOW THIS IS A LONG LIST (AN ACCENTED é KILLED THE SCRIPT)

def checkDate(base,filePath):
	try:
		with open(filePath) as thingie:
			if re.match(combinedDateFormats,base):
				currentAction = "accepting date"
				statusLog(currentAction,filePath,base)
				acceptFile(base,filePath)	
			else:
				currentAction = "bad date"
				statusLog(currentAction,filePath,base)
				rejectFile(base, filePath)
	except FileNotFoundError as ex:
		currentAction = "event image already rejected"
		statusLog(currentAction,filePath,base)

def checkFilenameFormat(base,filePath):
	currentAction = "Checking the Filename Format"
	print("STARTING THE FILECHECK PROCESS")
	statusLog(currentAction,filePath,base)	

	# FIRST CHECK FOR BAD CHARACTERS #
	if re.match(badCharacterRegex, base):
		currentAction = "Bad characters found"
		statusLog(currentAction,filePath,base)
		print(currentAction+" in "+base)
		rejectFile(base, filePath)

	else:	
		
		# CHECKING FILM STILLS #

		if "Film" in filePath:
			if re.match(filmRegex,base):
				print("THE FILM STILL IS ACCEPTED "+base+"\r")
				acceptFile(base,filePath)
			else:
				currentAction = "rejecting a film still"
				statusLog(currentAction,filePath,base)	
				rejectFile(base, filePath)

		
		# CHECKING EVENT IMAGES #
		elif "Event" in filePath:
			try:
				with open(filePath) as eventFile:
					if re.match(eventRegex,base):
						currentAction = "event image name format is ok"
						statusLog(currentAction,filePath,base)
						checkDate(base,filePath)
					else:
						currentAction = "rejecting an event image"
						statusLog(currentAction,filePath,base)
						rejectFile(base, filePath)
			except FileNotFoundError as ex:
				currentAction = "event image already rejected"
				statusLog(currentAction,filePath,base)

		# CHECKING GALLERY EXHIBITION PHOTOS #
		else:
			if "Art" in filePath: 
				try:
					with open(filePath) as gallImage:
							if re.match(exhibitionRegex, base):
								currentAction = "exhibition image name format is ok"
								statusLog(currentAction,filePath,base)
								checkDate(base,filePath)
							else:
								currentAction = "rejecting an exhibition image"
								statusLog(currentAction,filePath,base)
								rejectFile(base, filePath)
				except FileNotFoundError as ex:
					currentAction = "exhibition image already rejected"
					statusLog(currentAction,filePath,base)

## ~~ MASTER SCRIPT POINTS HERE, THIS IS THE STARTING POINT ~~ ##

def process(folder):
	for item in glob("'"+folder+"'",recursive=True):  # HAD TO ADD EXTRA QUOTES FOR CRON / LAUNCH DAEMON TO BE ABLE TO HANDLE THIS VARIABLE
		filePath = os.path.abspath(item)
		print(filePath)
		base = os.path.basename(item)
		if os.path.isfile(item):
			if not item.startswith("."):
				if any(x in base for x in imageTypes):
					print(item)
					checkFilenameFormat(base,filePath)
				
				# REJECT NON-IMAGE FILES OR IMAGES WITHOUT CORRECT FILETYPE #
				else:
					currentAction = "Bad filetype"
					statusLog(currentAction,filePath,base)

