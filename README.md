Dir-Xcan
========
Dir-Xcan3 is a free and open source scanner. Based on the OWASP's DirBuster project that is now closed. It is _mostly_ experimental software. <br />

This program is for finding hidden directories that are not directly links on a website. It find HTTP response code 200 directories and outputs the URL to file. <br />

--**** Use at your own risk. ****-- <br />

+ Tested on: Linux 3.2.6 Ubuntu/Debian (Backtrack & Kali), Windows Multiple Variants. <br />

## Usage:

    root@bt:~# Dir-Xcan3.py

    Now you may follow the simple prompts.

    [1:] Enter the target URL or IP (e.g. http://google.com). please leave trailing slash off
            Example : testphp.vulnweb.com
            

    [2:] Enter the name of the Dir list file to be scanned
            Example : directorylist.txt

    [3:] Filename you want to export the HTTP Code 200 directories too?
            Example : httpok-vulnweb.html
	
	[4:] How many threads do you want to use? (Use less for slow connections)
            Example : 3

    [OR] 
	
	root@bt:~# Dir-Xcan3.py -t testphp.vulnweb.com -f directorylist.txt -o Vulnweb.html -n 3
	
				-t = Target domain name or ip
				-f = Filename of the list you want to scan for
				-o = Output Filename for logging of Code 200 Responses
				-n = Number of threads	
						
			Other Arguments:
				
				-v = Version information
				-h = Help menu
						
        The program will print out the code 200 HTTP Responses to the output file.
        
        It will feed you the percentage of the scan until completion and the ammount of time it took
        to complete the task.
		
        Enjoy. :]
                                                                    ~/ NoobieDog

## Contact Information:

    [ NoobieDog ] - @NoobieDog on Twitter

## Original Header:

    - This was written for educational purpose and pentest only. Use it at your own risk.
    - Author will be not responsible for any damage!
    - Toolname        : Dir-Xcan3.py
    - Coder           : NoobieDog
    - Version         : 3.0

