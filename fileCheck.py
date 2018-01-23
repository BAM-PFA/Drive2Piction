#!/usr/bin/env python3

import os, re, datetime, time
from datetime import date
from ftpLogger import statusLog
from mover import acceptFile, rejectFile

today = str(date.today())
timeStamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d:%H:%M:%S:%f'))

year = "((19|20)*([0-9]{2}|[0-9]{4})+)" # matches optional century, has to have either 2 or 4 digits
month = "(0[1-9]|1[012])"
day = "(0[1-9]|[12][0-9]|3[01])*" # day is optional
wordMonths = "((jan[a-z]*)|(feb[a-z]*)|(mar[a-z]*)|(apr[a-z]*)|(may[a-z]*)|(jun[a-z]*)|(jul[a-z]*)|(aug[a-z]*)|(sep[a-z]*)|(oct[a-z]*)|(nov[a-z]*)|(dec[a-z]*))"

filmPath = "Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
eventPath = "Research_Hub_Collections/RH_Events"
exhibitionPath = "Research_Hub_Collections/RH_Gallery_Exhibitions"
root = "/Users/michael/Google Drive"

yyyymmdd = year+"-*"+month+"-*"+day # since day is optional this also covers yyyymm
mmddyyyy = month+"-*"+day+"-*"+year # since day is optional this also covers mmyyyy
wordmonthYear = wordMonths+"-*"+day+"-*"+year+"*"
yearWordmonth = year+"-*"+wordMonths+"-*"+day

imageTypes = [".jpg",".JPG",".tif",".TIF",".jpeg",".JPEG",".tiff",".TIFF",".png",".PNG"]
combinedDateFormats = re.compile(r''+'.*_(('+year+')|('+yyyymmdd+')|('+mmddyyyy+')|('+wordmonthYear+')|('+yearWordmonth+'))_.*',re.IGNORECASE)
filmRegex = re.compile(r'^([a-z]+)(\_|-)*([a-z0-9]*(\_|-))*(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
eventRegex = re.compile(r'^(event)_(([a-z]|[0-9])*(\_|-))+(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
exhibitionRegex = re.compile(r'(([a-z]|[0-9])*(\_|-))+(\d{3}\.)([a-z]{3,4})',re.IGNORECASE)
badCharacterList = ["é","$","%","^","&","*","#","@","!",")","(","*","+","="," ","á","à","ä","å","À","Á","è","é","ê","ë","È","É","Ò","Ó","Ö","ò","ó","ô","ö","â","ì","í","Ì","Í","î","ü","Ü","Ú","Ù","ù","ú","©","¿","?","“","”","\"","/","’","‘","'","´","`","¨","\\"]
badCharacterRegex = re.compile(r'(.*)(\$|%|\^|&|\*|#|@|!|\)|\(|\*|\+|=|\ |á|à|ä|å|À|Á|è|é|é| \
					ê|ë|È|É|Ò|Ó|Ö|ò|ó|ô|ö|â|ì|í|Ì|Í|î|ü|Ü|Ú|Ù|ù|ú|©|¿|\?|\“| \
					\”|\"|\/|\’|\‘|\'|\´|\`|¨|\')(.*)',re.IGNORECASE) # WOW THIS IS A LONG LIST

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
	currentAction = "Checking the Filename Format on "
	print("STARTING THE FILECHECK PROCESS on "+base)
	statusLog(currentAction,filePath,base)	

	# CHECK FOR BAD CHARACTERS. THIS IS SORT OF REDUNDANT 
	# GIVEN THE CHECK IN process(), BUT IT WILL CATCH ANYTHING THAT SLIPS THROUGH

	if re.match(badCharacterRegex, base):
		currentAction = "Bad characters found"
		statusLog(currentAction,filePath,base)
		print(currentAction+" in "+base)
		rejectFile(base,filePath)

	else:	
		
		# CHECKING FILM STILLS #
		if "Film " in filePath:
			if re.match(filmRegex,base):
				print("THE FILM STILL IS ACCEPTED "+base+"\r")
				acceptFile(base,filePath)
			else:
				currentAction = "rejecting a film still"
				statusLog(currentAction,filePath,base)	
				rejectFile(base, filePath)

		# CHECKING EVENT IMAGES #
		elif "Events " in filePath:
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
			if "Exhibitions " in filePath: 
				try:
					with open(filePath) as gallImage:
						if re.match(exhibitionRegex, base):
							acceptFile(base,filePath) # ORIGINALLY THIS SENT EXH IMAGES TO checkDate()
						else:
							currentAction = "rejecting an exhibition image"
							statusLog(currentAction,filePath,base)
							rejectFile(base, filePath)
				except FileNotFoundError as ex:
					currentAction = "exhibition image already rejected"
					statusLog(currentAction,filePath,base)

## ~~ MASTER SCRIPT POINTS HERE, THIS IS THE STARTING POINT ~~ ##

def process(folder):
	for root, directories, filenames in os.walk(folder):
		if "Images " in root:
			for item in filenames:
				if not item.startswith("."):
					if any(ext in item for ext in imageTypes):
						print("THIS IS AN IMAGE, DUDE")

						# THIS STEP REPLACES ALL BAD CHARACTERS WITH AN ASTERISK.						
						for char in badCharacterList:
							if char in item:
								item = item.replace(char,"*")
						base = item
						print(base)
						# THE NEXT FEW LINES CUT OUT ANYTHING BETWEEN THE FIRST ASTERISK AND THE 
						# CHARACTER AFTER THE LAST ASTERISK. THAT WAY, rejectFile() CAN USE
						# GLOB TO FIND THE FILEPATH OF THE EXISTING FILE (WITH BAD CHARACTERS
						# IN THE FILENAME), E.G. thisIsAFileThatHad*BadCharacters.ext
						charIndex = 0
						charIndexList = []						
						while charIndex < len(base):
							charIndex = base.find('*',charIndex)
							if charIndex == -1:
								break
							charIndexList.append(charIndex)
							charIndex += 1
						if not charIndexList == []:
							base = base[:charIndexList[0]] + base[(charIndexList[-1]):]
						# AND IF THERE WERE NO ASTERISKS, LEAVE IT ALONE.
						else:
							base = base
						filePath = root+"/"+base
						checkFilenameFormat(base,filePath)
					else:
						
						# REJECT NON-IMAGE FILES OR IMAGES WITHOUT CORRECT FILETYPE #
						base = item
						filePath = root+"/"+base
						currentAction = "Bad filetype"
						statusLog(currentAction,filePath,base)
