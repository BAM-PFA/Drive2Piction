#! usr/bin/env python

import os, re, pexpect
from glob import glob
from ftpLogger import statusLog

root = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections"
imageTypes = [".jpg",".tif"]

with open('/Users/michael/Desktop/drive2Piction/PictionFTP/pictioneer.txt','r') as pword:
	pwordList = list(pword)
	answer = pwordList[0]

def put(folder):
	for source in glob(folder):
		if not source.startswith("_"):
			os.chdir(source)
			pwd = os.getcwd()
			currentAction = "trying to ftp"
			statusLog(currentAction,pwd,source)

			child = pexpect.spawnu('ftp ucb1.piction.com') # LOG INTO THE PICTION SERVER
			child.expect('.*ame.*:')
			child.sendline('bampfa')
			child.expect('.*assword.*')
			child.sendline(answer)
			child.expect('ftp>')
			child.sendline('cd Research_Hub_Collections/'+source) # NAVIGATE TO THE CORRESPONDING PICTION FOLDER
			child.expect('ftp>')
			child.sendline('prompt off') 

			for file in os.listdir('.'):
				if not file.startswith("."):
					if any(x in file for x in imageTypes):
						print(file+"to ftp")
						currentAction = "now ftp per file"
						statusLog(currentAction,pwd,file)
						child.expect('ftp>')
						child.sendline('mput '+file) 
			try:
				child.expect('ftp>')
				currentAction = "ftp success"
				print("SUCCESS WE FTPeD "+source)
			except Error as error:
				child.expect('ftp>')
				print("FAILED TO ftp "+source)
			os.chdir(root)

	# child.interact()