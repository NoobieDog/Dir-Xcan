#!/usr/bin/python
# LAST UPDATE 01/10/14
#
# DIR-XCAN5.PY
# This program is for finding hidden directories that are not directly linked on a website. It find HTTP response code 200 directories and outputs the URL to file.

# THIS PROGRAM IS A PYTHON VERSION OF THE OWASP'S DIRBUSTER PROJECT THAT IS NOW CLOSED
# https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project
#
# 	This script uses OWASP's DirBuster list - directory-list-2.3-medium.txt
#
# 	Copyright 2007 James Fisher
#
# 	This work is licensed under the Creative Commons 
# 	Attribution-Share Alike 3.0 License. To view a copy of this 
# 	license, visit http://creativecommons.org/licenses/by-sa/3.0/ 
# 	or send a letter to Creative Commons, 171 Second Street, 
# 	Suite 300, San Francisco, California, 94105, USA.
#
# ADD ME ON TWITTER @NOOBIEDOG

#Changelog:
	# [DONE] - Http Authentication
	# [DONE] - Add COLOR.
	# [DONE] - http Proxy options.
	# [DONE] - Kill threads on Ctrl+C.
	# [DONE] - Defaults added to Arguments.
	# [DONE] - Now using Requests instead of Urllib2.
	# [DONE] - Verbose modes added, prints found and Non-Authed folders.
	# [DONE] - Added User-Agent option.
#TODO:
	# SOCKS Proxy options.
	# Change number of threads on responce time from server.
	# Fix error reporting for connection issues.
	# Add Pause/Stop/Start functions to script.
	# Add XML output option.
	# Custom 404 page option.
	# Add NTLM Authentication

__author__ = '@NoobieDog'

from sys import argv
import argparse
import Queue
import sys
import threading
import requests
import time
import base64

														# Console colors
W  = '\033[0m'  										# white (normal)
R  = '\033[31m'											# red
G  = '\033[32m' 										# green
O  = '\033[33m' 										# orange
B  = '\033[34m' 										# blue
GR = '\033[37m' 										# gray
BB = '\033[1m'  										# Bold
NB = '\033[0m'  										# Not bold

def mapcount(listing):
	lines = 0
	with open(listing) as f:
		lines = sum(1 for line in f)
	return lines
	
parser = argparse.ArgumentParser(
				version='5.0', 
				description='A Python version of DirBuster',
				epilog='Dir-Xcan is a multi threaded python application designed to brute force directories on web/application servers.')

parser.add_argument('-s', action="store", help='Website Domain or IP')
parser.add_argument('-d', action="store", help='Directory word list', default="directorylist.txt")
parser.add_argument('-o', action="store", help='Output file name (HTML)', default="Dir-Xcan-results.html")
parser.add_argument('-n', action="store", help='Number of threads', default="5")
parser.add_argument('-p', action="store", help='Proxy address and port (host:port)')
parser.add_argument('-a', action="store", help='Authentication BasicHTTP(username:password)')
parser.add_argument('-u', action="store", help='User-Agent', default="Mozilla/5.0")
parser.add_argument("-V", action="store_true", help="Output information about new data.")

try:
    results = parser.parse_args()

except IOError, msg:
    parser.error(str(msg))

	
print O + '''
 %s _____ _____ _____     __   _______          _   _ 
 |  __ \_   _|  __ \    \ \ / / ____|   /\   | \ | |
 | |  | || | | |__) |____\ V / |       /  \  |  \| |
 | |  | || | |  _  /______> <| |      / /\ \ | . ` |
 | |__| || |_| | \ \     / . \ |____ / ____ \| |\  |
 |_____/_____|_|  \_\   /_/ \_\_____/_/    \_\_| \_|%s
                                                    
 %sRelease Date%s: 06/10/2014
 %sRelease Version%s: V.5.0
 %sCode%s: stuart@sensepost.com // @NoobieDog
 %sVisit%s:  www.sensepost.com // @sensepost
''' %(BB,NB,R,W,R,W,R,W,R,W)

ProxyOpt = False
AuthOpt = False

if not results.s or not results.d:
	parser.print_help()
	exit()
else:
	target = results.s
	if not target.startswith("http"):
		print R + ' Please include the http:// or https:// parts' + W
		exit()
	list_file = results.d
	outputname = results.o
	ThreadNumber = int(results.n)
	Proxy_Addr = results.p
	Auth_Data = results.a
	Usr_Agent = results.u
	if results.p:
		ProxyOpt = True
		Proxies = {
  			"http": Proxy_Addr,
			}
	if results.a:
		AuthOpt = True
		Auth_User, Auth_Pwd = results.a.split(':', 1)
	if results.u:
		headers = {
    		'User-Agent': Usr_Agent,
			}
	print O + ' lines to try..' + str(mapcount(list_file)) + W

with open(list_file) as f:
	directorys = f.readlines()
queue = Queue.Queue()
NotFound = 0
NotAuthorised = 0
Found = 0
Forbidden = 0
Other = 0
LinesLeft = len(directorys)
Lines = len(directorys)

def GetURL(host, target):
	global NotFound, Found, Forbidden, Other, LinesLeft, Lines
	sys.stdout.write("\r\x1b[K \033[31m%d \033[0mFound, \033[33m%d \033[0mForbidden, \033[32m%d \033[0mNotFound, \033[37m%d \033[0mOther, \033[37m%d \033[0mPercent Left" % (Found, Forbidden, NotFound, Other, LinesLeft*100/Lines))
	sys.stdout.flush()
	
	try: 
		if AuthOpt == True:
			url = requests.get(target + '/' + str(host.rstrip()), auth=(Auth_User, Auth_Pwd), headers=headers)
		elif ProxyOpt == True:
			url = requests.get(target + '/' + str(host.rstrip()), proxies=Proxies, headers=headers)
		elif AuthOpt and ProxyOpt == True:
			url = requests.get(target + '/' + str(host.rstrip()), proxies=Proxy_Addr, auth=(Auth_User, Auth_Pwd), headers=headers)
		else:
			url = requests.get(target + '/' + str(host.rstrip()), headers=headers)
			
		code = url.status_code
		if code == 401:
			Other += 1
			LinesLeft -= 1
			outputfile.write("<A HREF='" + target + "/" + host + "'>" + target + '/' + host + " - <STRONG>REQUIRES AUTHENTICATION</STRONG><br>\n");
			if results.V:
				sys.stdout.write("\r\x1b[K\033[33m %s/%s\033[0m-REQUIRES AUTHENTICATION" % (target, host)) 		# Doesnt print after value :S
				sys.stdout.flush()	
				
		elif code == 403:
			Forbidden = Forbidden + 1
			LinesLeft -= 1
		elif code == 404:																							# Need to look at making this shizz better (array or list)
			NotFound += 1
			LinesLeft -= 1
		elif code == 200:
			Found += 1
			LinesLeft -= 1
			outputfile.write("<A HREF='" + target + "/" + host + "'>" + target + '/' + host + "<br>\n");
			if results.V:
				sys.stdout.write("\r\x1b[K\033[31m %s/%s\033[0m-FOUND" % (target, host)) 							# Doesnt print after value :S
				sys.stdout.flush()
		else:
			Other += 1
			LinesLeft -= 1

			
	except requests.ConnectionError, e:
		outputfile.write("We failed to reach a server.<br>Reason: Connection Error</BODY></HTML>");
		outputfile.close()
		print R + "\n ERROR: Connection Error - Check target is correct or exists" + W
		sys.exit()
	        
class ThreadUrl(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			try:																									# NEED TO EXIT THE THREADS AND SCRIPT BETTER
				host = self.queue.get()
				GetURL(host, target)
				self.queue.task_done()
			except (SystemExit):
				print R + '\n Shutting down! ' + W + '....'	

def main():   
    for i in range(ThreadNumber):

		   	t = ThreadUrl(queue)
		   	t.setDaemon(True)
			t.start()

    for host in directorys:
        try:
	        queue.put(host)
	        queue.join()
    	except (KeyboardInterrupt, SystemExit):
        	print R + '\n Ctrl+C Detected! ' + W + '....' + R + '\n Shutting down! ' + W + '....'
        	sys.exit()

outputfile = open(outputname, "wb")
outputfile.write("<HTML><HEAD><TITLE>" + target + "</TITLE></HEAD><BODY>\n");
start = time.time()
main()
outputfile.write("</BODY></HTML>");
outputfile.close()
print O + '\n Elapsed Time: \033[0m%s' % (time.time() - start)
