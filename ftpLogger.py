#!/Users/michael/anaconda/bin/python3.5

import os, re, shutil, datetime, time
from datetime import date
from pyfiglet import Figlet
from pathlib import Path

today = str(date.today())

filmPath = "Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
eventPath = "Research_Hub_Collections/RH_Events"
exhibitionPath = "Research_Hub_Collections/RH_Gallery_Exhibitions"

pathToFTPLog = "/Users/michael/Desktop/drive2Piction/FTPs/"+today+"_FTP-log.txt"
FTPlogPath = Path(pathToFTPLog)
listLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt"
listLogPath = Path(listLogFile)
rejectLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterRejectList.txt"
rejectLogPath = Path(rejectLogFile)

fig = Figlet(font='fantasy_')
caliFig = Figlet(font='caligraphy')
isoFig = Figlet(font='isometric3')

if FTPlogPath.is_file():
	print("there's a list for "+today+" already.")
else:
	with open(pathToFTPLog,"w+",encoding="utf-8") as f:
		print("starting a log for "+today)

if listLogPath.is_file():
	print("the masterList exists, way to go.")
	with open(listLogFile,"a+",encoding="utf-8") as List:
		List.write("\r"+(("*")*100)+("\r\r")+fig.renderText(today)+("\r\r")+(("*")*100)+"\r")
else:
	with open(listLogFile,"w+",encoding="utf-8") as List:
		List.write((("#" * 70) + (("\n#") + ((" ") * 68) + "#") * 2) + ("\n#" + (" " * 4)) + "HELLO AND WELCOME TO THE BIG LIST OF PICS"+(" " * 23)+"#\n#" + (" " * 4)+"SENT TO PICTION VIA GOOGLE DRIVE. Started "+today+((" " * 12)+"#\n")+("#"+(" " * 68) +("#\n"))+("#" * 70)+"\n\n")

if rejectLogPath.is_file():
	print("the rejectList exists, way to go.")
	with open(rejectLogFile,"a+",encoding="utf-8") as todayDivider:
		todayDivider.write("\r"+(("*")*100)+("\r\r")+fig.renderText(today)+("\r\r")+(("*")*100)+"\r")
else:
	with open(rejectLogFile,"w+",encoding="utf-8") as List:
		List.write((("#" * 70) + (("\n#") + ((" ") * 68) + "#") * 2) + ("\n#" + (" " * 4)) + "HELLO AND WELCOME TO THE BIG LIST OF PICS"+(" " * 23)+"#\n#" + (" " * 4)+"REJECTED FROM PICTION. Started "+today+((" " * 23)+"#\n")+("#"+(" " * 68) +("#\n"))+("#" * 70)+"\n\n")

## ~~ DON'T LOOK AT THIS, NOTHING TO SEE HERE, MOVE ALONG ~~ ##

from PIL import Image
import numpy as np

chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))

f = "/Users/michael/Desktop/drive2Piction/FTPs/trash.png"
SC= .14 #size adjustment factor
WCF= 7/4.0 # character width fudge factor.
GCF= 1.8 #? some strange color correction fudge factor

im = Image.open(f)
S =( int(round(im.size[0]*SC*WCF)),  int(round(im.size[1]*SC)) )
img = np.array(im.convert("L").resize(S), dtype=float)
img -= img.min()
img = np.rint((1.0 - img/img.max())**GCF*(chars.size-1))

trash =	( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )

## ~~ HERE'S THE STUFF ~~ ##

def rejectLog(base):
	with open(rejectLogFile,"a+",encoding="utf-8") as rejected:
		rejected.write(base+" rejected on "+today+"\n")

def listLog(base):
	with open(listLogFile,"a+",encoding="utf-8") as masterList:
		masterList.write(base+" sent to Piction on "+today+"\n")

def statusLog(currentAction,filePath,base):
	with open(pathToFTPLog,"a+",encoding="utf-8") as log:
		
		## ~~ TURNING THINGS ON ~~ ##

		if currentAction == "initial":
			print("Starting")
			log.write((("#" * 70) + (("\n#") + ((" ") * 68) + "#") * 2) + ("\n#" + (" " * 4) +("HELLO AND WELCOME TO THE DRIVE/PICTION FTP LOG FOR ")+ today + ((" " * 3)+"#\n"))+("#"+(" " * 68) +("#\n"))+("#" * 70)+"\n\n")

		## ~~ STARTING THE FILENAME CHECK PROCESS ~~ ##



		elif currentAction == "Checking the Filename Format":
			if "Film " in filePath:
				log.write(base+": This film still is being checked ...\r")
			elif "Events " in filePath:
				log.write(filePath+base+": This event file is being checked ...\r")
			else:
				if "Exhibitions " in filePath:
					log.write(base+": This exhibition file is being checked ...\r")
		
		# CHECKING FOR BAD CHARACTERS AND FILETYPES

		elif currentAction == "Bad characters found":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+" is REJECTED!!! There are illegal characters in the filename!\r\r"+("#"*50)+"\r\r")
		elif currentAction == "Bad filetype":
			log.write("\rWOMP WOMP : "+filePath+base+" is REJECTED!!! It isn't even an image!\r\r"+("#"*50)+"\r\r")

		# ERROR HANDLING FOR DUPLICATE FILES

		elif currentAction == "renaming a duplicate file":
			log.write("Oops there is already a file named "+base+"so this copy is being renamed and rejected.\r\r"+("#"*50)+"\r\r")
		
		# CHECKING FILENAME FORMATS

		elif currentAction == "rejecting a film still":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this film still, please.\r\r"+("#"*50)+"\r\r")
		
		elif currentAction == "event image name format is ok":
			log.write(base+": Filename format is ok, proceeding to check the date ...\r")
		elif currentAction == "rejecting an event image":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this event image, please.\r\r"+("#"*50)+"\r\r")
		
		elif currentAction == "exhibition image name format is ok":
			log.write(base+": Filename format is ok, proceeding to check the date ...\r")
		elif currentAction == "rejecting an exhibition image":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this exhibition image, please.\r\r"+("#"*50)+"\r\r")

		# CHECKING DATES IN EVENT AND EXHIBITION IMAGES

		elif currentAction == "checking date":
			log.write("... Ok now we are checking the date on "+base+" ... \r")
		elif currentAction == "bad date":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+":  Oops, the date format is incorrect, please check it and rename it.\r\r"+("#"*50)+"\r\r")

		# ACCEPTING FILENAME FORMAT, CHECKING FOR DUPE IN PICTION FTP LIST

		elif currentAction == "accepting a file":
			log.write(base+": SUCCESS, you didn't mess up the filename, let's see if it's already in Piction .... \r")
		elif currentAction == "already in Piction":
			log.write(base+": Already in Piction, skipping this file."+"\r\r"+("#"*50)+"\r\r")
		elif currentAction == "sending to Piction":
			log.write(base+": Holy moly this file is ready to be FTPed\r\r"+("#"*50)+"\r\r")


		## ~~ STARTING THE FTP PROCESS ~~ ##

		elif currentAction == "time to ftp":
			log.write((("@" * 70) + (("\n@") + ((" ") * 68) + "@") * 2) + ("\n@" + (" " * 6) + "BEGINNING THE FTP PROCESS, HOLD TF ON" + ((" " * 25)+"@\n"))+("@"+(" " * 68) +("@\n"))+("@" * 70)+"\n\n")
		elif currentAction == "trying to ftp":
			log.write("////////    Starting the FTP process for "+base+"    ////////\r\r"+("#"*50)+"\r\r")
		elif currentAction == "nothing to ftp":
			log.write("\r\r"+fig.renderText('SHUCKS')+"\r\rNothing to see here, moving on.... \r\r"+("#"*50)+"\r\r")
		elif currentAction == "now ftp per file":
			log.write("Starting to FTP: "+base+"\r")
		elif currentAction == "ftp file success":
			log.write("Great, looks like "+base+" FTPed OK.... moving on ...\r\r")
		elif currentAction == "ftp file failure":
			log.write(fig.renderText("SAD!")+"\r\rFailed to FTP "+base)
		elif currentAction == "ftp folder success":
			log.write("\r"+(isoFig.renderText("WOO HOO"))+"\r\rWe processed "+base+"\r\r")
		elif currentAction == "cleanup":
			log.write("Now cleaning up the mess\r"+trash+"\r\r"+("#"*50)+"\r\r")
		elif currentAction == "done":
			log.write((((("%")*90)+"\r")*2)+caliFig.renderText("DONE")+(((("%")*90)+"\r")*2))
		elif currentAction == "failed before FTP":
			log.write("XXXXXXXX    Failed to FTP at "+filePath+"    XXXXXXXX\r\r"+("#"*50)+"\r\r")
		elif currentAction == "failed to copy to ftp path":
			log.write("XXXXX  Failed to copy "+filePath+" to FTP folder XXXXX\r\r"+("#"*50)+"\r\r")
		else:
			if currentAction == "failed to FTP":
				log.write("Sorry, couldn't FTP "+base)

'''
KIND OF WANT TO USE THIS DRAGON FROM COWSAY:
import subprocess
from pyfiglet import Figlet

fig = Figlet(font = 'fantasy_')

hello = ((("#")*39)+"\n\n"+((" ")*5)+"HELLO AND WELCOME TO THE FTP LOG FOR:\n\n"+today+"\n\n"+(("#")*39))

file = open('dragon.txt ','w')

dragon = subprocess.call(['cowsay','-f','dragon',hello],stdout=file)
'''
