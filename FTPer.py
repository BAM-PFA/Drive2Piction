#!/usr/bin/env python3

import os, re, pexpect, codecs
from glob import glob
from ftpLogger import statusLog, listLog

root = "/Users/michael/Desktop/drive2Piction/FTPs/Research_Hub_Collections"
listLogFile = "/Users/michael/Desktop/drive2Piction/FTPs/masterFTPlogList.txt"


with open('/Users/michael/Desktop/drive2Piction/PictionFTP/pictioneer.txt','r',encoding="utf-8") as pword:
	pwordList = list(pword)
	answer = pwordList[0]

with open(listLogFile,"r",encoding="utf-8") as read:
	textAsList = list(read)
	allText = ''.join(textAsList)

def put(folder):

	for source in glob(folder):
		try:
			if not source.startswith("_"):  # ONLY THE RESEARCH_HUB_COLLECTIONS/ FOLDER STARTS WITH SOMETHING OTHER THAN '_'
				os.chdir(source)
				pwd = os.getcwd()
				currentAction = "trying to ftp"
				statusLog(currentAction,pwd,source)
				if ''.join(os.listdir('.')) == '.DS_Store':
					currentAction = "nothing to ftp"
					statusLog(currentAction,pwd,source)
					print("SKIPPING "+source)
				else:		
					child = pexpect.spawnu('ftp ucb1.piction.com', timeout=1000) # LOG INTO THE PICTION SERVER, TIMEOUT SET TO 1K SECONDS.
					child.expect('.*ame.*:')
					child.sendline('bampfa')
					child.expect('.*assword.*')
					child.sendline(answer)
					child.expect('ftp>')
					print("CONNECTED")
					child.sendline('cd '+source) # NAVIGATE TO THE CORRESPONDING PICTION FOLDER
					child.expect('ftp>')
					child.sendline('prompt off')
					child.expect('ftp>')
					child.sendline('binary')
					for file in os.listdir('.'):
						if not file.startswith("."):
							if not re.search(file, allText):
								print(file+" ready to ftp")
								currentAction = "now ftp per file"
								statusLog(currentAction,pwd,file)
								try:
									child.expect('ftp>')
									child.sendline('mput '+file)
									currentAction = "ftp file success"
									statusLog(currentAction,pwd,file)
									listLog(file)
								except Error as error:
									currentAction = "ftp file failure"
									statusLog(currentAction,pwd,file)
					try:
						child.expect('ftp>')
						currentAction = "ftp folder success"
						print("SUCCESS WE FTPed "+source)
						statusLog(currentAction,pwd,source)
						fileList = os.listdir('.')
						for item in fileList:
							if not item == '.DS_Store':
								os.remove(item)
					except Error as error:
						currentAction = "failed to FTP"
						print("FAILED TO ftp "+source)
						pass
					currentAction = "cleanup"
					statusLog(currentAction,pwd,source)
				os.chdir(root)
			else:
				pass
		except:
			pwd = os.getcwd()
			currentAction = "failed before FTP"
			statusLog(currentAction, pwd, source)
