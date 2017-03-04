#! usr/bin/env python

from datetime import date
from pyfiglet import Figlet
import os, re, shutil, datetime, time

today = str(date.today())

filmPath = "Research_Hub_Collections/RH_PFA_Film_Stills_Series_Collection"
eventPath = "Research_Hub_Collections/RH_Events"
exhibitionPath = "Research_Hub_Collections/RH_Gallery_Exhibitions"
pathToLog = "/Users/michael/Desktop/drive2Piction/FTPs/"+today+"_checker-log.txt"

fig = Figlet(font='fantasy_')
isoFig = Figlet(font='isometric3')

def statusLog(currentAction,filePath,base):
	with open(pathToLog,"a") as log:
		
		## ~~ TURNING THINGS ON ~~ ##

		if currentAction == "initial":
			print("Starting")
			log.write((("#" * 70) + (("\n#") + ((" ") * 68) + "#") * 2) + ("\n#" + (" " * 4) +("HELLO AND WELCOME TO THE DRIVE/PICTION FTP LOG FOR ")+ today + ((" " * 3)+"#\n"))+("#"+(" " * 68) +("#\n"))+("#" * 70)+"\n\n")

		## ~~ STARTING THE FILENAME CHECK PROCESS ~~ ##

		elif currentAction == "Checking the Filename Format":
			if "Film " in filePath:
				log.write(base+": this film still is being checked ...\r")
			elif "Event " in filePath:
				log.write(base+": this event file is being checked ...\r")
			else:
				if "Art " in filePath:
					log.write(base+": this exhibition file is being checked ...\r")
		
		# CHECKING FOR BAD CHARACTERS AND FILETYPES

		elif currentAction == "Bad characters found":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+" is REJECTED!!! There are illegal characters in the filename!\r\r"+("#"*50)+"\r\r")
		elif currentAction == "Bad filetype":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+" is REJECTED!!! It isn't even an image!\r\r"+("#"*50)+"\r\r")


		# ERROR HANDLING FOR DUPLICATE FILES

		elif currentAction == "renaming a duplicate file":
			log.write("Oops there is already a file named "+base+"so this copy is being renamed and rejected.\r\r"+("#"*50)+"\r\r")
		
		# CHECKING FILENAME FORMATS

		# elif currentAction == "accepting a film still":
			# log.write(base+" is a film still that is ok to FTP, go ahead.\r")
		elif currentAction == "rejecting a film still":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this film still, please.\r\r"+("#"*50)+"\r\r")
		
		elif currentAction == "event image name format is ok":
			log.write(base+": filename format is ok, proceeding to check the date ...\r")
		elif currentAction == "rejecting an event image":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this event image, please.\r\r"+("#"*50)+"\r\r")
		
		elif currentAction == "exhibition image name format is ok":
			log.write(base+": filename format is ok, proceeding to check the date ...\r")
		elif currentAction == "rejecting an exhibition image":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+": try renaming this exhibition image, please.\r\r"+("#"*50)+"\r\r")

		# CHECKING DATES IN EVENT AND EXHIBITION IMAGES

		elif currentAction == "checking date":
			log.write("... Ok now we are checking the date on "+base+" ... \r")
		# elif currentAction == "accepting date":
		# 	log.write(base+": SUCCESS, you didn't fuck up the filename, let's FTP this sucker .... \r\r"+("#"*50)+"\r\r")
		elif currentAction == "bad date":
			log.write("\r\r"+fig.renderText('ERROR!!!')+'\r'+base+":  Oops, the date format is incorrect, please check it and rename it.\r\r"+("#"*50)+"\r\r")

		# ACCEPTING FILENAME FORMAT, CHECKING FOR DUPE IN PICTION FTP LIST

		elif currentAction == "accepting a file":
			log.write(base+": SUCCESS, you didn't fuck up the filename, let's see if it's already in Piction .... \r")
		elif currentAction == "already in Piction":
			log.write(base+": Already in Piction, skipping, sucka."+"\r\r"+("#"*50)+"\r\r")
		elif currentAction == "sending to Piction":
			log.write(base+" Holy shit this file is ready to be FTPed\r\r"+("#"*50)+"\r\r")


		## ~~ STARTING THE FTP PROCESS ~~ ##

		elif currentAction == "time to ftp":
			log.write((("@" * 70) + (("\n@") + ((" ") * 68) + "@") * 2) + ("\n@" + (" " * 6) + "BEGINNING THE FTP PROCESS, HOLD TF ON" + ((" " * 25)+"@\n"))+("@"+(" " * 68) +("@\n"))+("@" * 70)+"\n\n")
		elif currentAction == "trying to ftp":
			log.write("////////    Starting the FTP process for "+base+"    ////////\r\r"+("#"*50)+"\r\r")
		elif currentAction == "now ftp per file":
			log.write("Starting to FTP: "+base+"\r")
		elif currentAction == "ftp file success":
			log.write("Great, looks like "+base+"FTPed OK.... moving on ...\r")
		elif currentAction == "ftp file failure":
			log.write(fig.renderText("SAD!")+"\r\rFailed to FTP "+base)
		elif currentAction == "ftp folder success":
			log.write("\r"+(isoFig.renderText("WOO HOO"))+"\r\rWe processed "+base+"\r\r"+("#"*50)+"\r\r")
			# log.write("\\\\\\\\\\ Failed to FTP thid folder ////////////")
		else:
			if currentAction == "failed to FTP":
				log.write("Sorry, couldn't FTP "+base)