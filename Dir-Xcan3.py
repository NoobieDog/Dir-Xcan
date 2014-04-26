#!/usr/bin/python
# LAST UPDATE 27/04/14
#
# DIR-XCAN.PY
# THIS PROGRAM IS A PYTHON VERSION OF THE OWASP'S DIRBUSTER PROJECT THAT IS NOW CLOSED
# https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project
#
# I CREATED THIS PROJECT TO FAMILIARISE MYSELF WITH ARGUMENTS AND FILES
#
# ADD ME ON TWITTER @NOOBIEDOG

# TO DO LIST

# ADD STATS AND MORE OPTIONS AT THE END

__author__ = '@NoobieDog'

from sys import argv
import argparse
import Queue
import sys
import threading
import urllib2
import time

def mapcount(listing): # Get number of lines in the directory list file
	lines = 0
	with open(listing) as f:
		lines = sum(1 for line in f)
	return lines
	
parser = argparse.ArgumentParser(
				version='3.0', 
				description='A Python version of DirBuster',
				epilog='I wrote this program to get used to Python with Arguments, Files and Threading')

parser.add_argument('-t', action="store", help='Website Domain or IP', required=False)
parser.add_argument('-f', action="store", help='Directory word list', required=False)
parser.add_argument('-o', action="store", help='Output file name (HTML)', required=False)
parser.add_argument('-n', action="store", help='Number of threads', required=False)

try:
    results = parser.parse_args()
	
except IOError, msg:
    parser.error(str(msg))
	
print '''
  _____ _____ _____     __   _______          _   _ 
 |  __ \_   _|  __ \    \ \ / / ____|   /\   | \ | |
 | |  | || | | |__) |____\ V / |       /  \  |  \| |
 | |  | || | |  _  /______> <| |      / /\ \ | . ` |
 | |__| || |_| | \ \     / . \ |____ / ____ \| |\  |
 |_____/_____|_|  \_\   /_/ \_\_____/_/    \_\_| \_|
                                                    
 Release Date 27/04/2014  - Release Version V.3.0
 By @NoobieDog
'''


if len(argv) == 1:													# If no args are given, still able to run the program
	print ' Enter the target URL or IP (e.g. http://google.com). please leave trailing slash off'
	target = raw_input(" Target: ")
	if not target.startswith("http://"): 							# lets you forget the http://
		target = 'http://' + target
	print ' Enter the name of the dir list to be scanned'
	listing = raw_input(" File List: ")
	print ' Filename you want to export the Code 200 directorys too?'
	outputname = raw_input(" Output Filename: ")
	print ' How many threads do you want to use? (Use less for slow connections)'
	ThreadNumber = int(raw_input(" Threads: "))
	print ' lines to try..' + str(mapcount(listing)) 				# Print how many lines were gonna try
	
elif not results.t or not results.f or not results.o:				# If any args are given but dont match the options.
	parser.print_help()
	exit()
else:																# Has args and there correct!
	target = results.t
	if not target.startswith("http://"): 							# lets you forget the http://
		target = 'http://' + target
	listing = results.f
	outputname = results.o
	ThreadNumber = int(results.n)
	print ' lines to try..' + str(mapcount(listing)) 				# Print how many lines were gonna try	

#Read file line by line
hosts = open(listing,"r")
queue = Queue.Queue()
NotFound = 0
NotAuthorised = 0
Found = 0
Forbidden = 0													# All stuff for counting variables
Other = 0
LinesLeft = int(mapcount(listing))
Lines = int(mapcount(listing))


def GetURL(host, target):
	global NotFound, NotAuthorised, Found, Forbidden, Other, LinesLeft, Lines
	sys.stdout.write("\r %d Found, %d Forbidden, %d NotFound, %d Other, %d Percent Left" % (Found, Forbidden, NotFound, Other, LinesLeft*100/Lines))
	sys.stdout.flush()											# show latest values in the scan then flush the output
	
	try: 
		url = urllib2.urlopen(target + '/' + str(host)) 		# try each line in file with the given url or ip
	
	except urllib2.HTTPError as e:
		if e.code == 401:
			Other += 1
			LinesLeft -= 1
		elif e.code == 403:
			Forbidden = Forbidden + 1
			LinesLeft -= 1
		elif e.code == 404:										# Need to look at making this shizz better (array or list)
			NotFound += 1
			LinesLeft -= 1
		elif e.code == 503:
			Other += 1
			LinesLeft -= 1
		else:
			Other += 1
			LinesLeft -= 1
			
	except urllib2.URLError as e:								# If an Error occurs print reason to screen and to output file.
		# outputfile.write("We failed to reach a server.<br>Reason: " + e.reason + "</BODY></HTML>");
		print "\n ERROR: %s" % (e.reason)
		
	else:														# if a code 200 is given back then print the url to a file for result based filtering
		Found += 1
		LinesLeft -= 1
		outputfile.write("<A HREF='" + target + "/" + host + "'>" + target + '/' + host + "<br>\n");


class ThreadUrl(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
            #grabs host from queue
			host = self.queue.get()
			GetURL(host, target)
            #grabs urls of hosts and prints first 1024 bytes of page
			self.queue.task_done()									#signals to queue job is done


def main():
    
    #spawn a pool of threads, and pass them queue instance 
    for i in range(ThreadNumber):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hosts:
        queue.put(host)
    
    #wait on the queue until everything has been processed
    queue.join()
	
	
outputfile = open(outputname, "wb")								# open output file.
outputfile.write("<HTML><HEAD><TITLE>" + target + "</TITLE></HEAD><BODY>\n");
start = time.time()
main()
outputfile.write("</BODY></HTML>");								# close files and finish the program
outputfile.close()
hosts.close()
print "\n Elapsed Time: %s" % (time.time() - start)
