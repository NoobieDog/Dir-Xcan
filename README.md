Dir-Xcan5
========

Release Date: 18/12/2014

Dir-Xcan5 is a free and open source scanner. Based on the OWASP's DirBuster project that is now closed. It is _mostly_ experimental software. <br />

This program is for finding hidden directories that are not directly linked on a website. It find HTTP response code 200 directories and outputs the URL to file. <br />

Changelog:

    # [DONE] - Http Authentication
    # [DONE] - Add COLOR.
    # [DONE] - http Proxy options.
    # [DONE] - Kill threads on Ctrl+C.
    # [DONE] - Defaults added to Arguments.
    # [DONE] - Now using Requests instead of Urllib2.
    # [DONE] - Verbose modes added, prints found and Non-Authed folders.
    # [DONE] - Added User-Agent option.
    # [DONE] - Cookie Authentication (with multiple cookies)
    # [DONE] - SOCKS Proxy options # To use TOR socks5://127.0.0.1:9050 or socks4://127.0.0.1:9050

TODO:

	# Change number of threads on responce time from server.
	# Fix error reporting for connection issues.
	# Add Pause/Stop/Start functions to script.
	# Add XML output option.
	# Custom 404 page option.
	# Add NTLM Authentication

--**** Use at your own risk. ****-- <br />

+ Tested on: Linux 3.2.6 Ubuntu/Debian (Backtrack & Kali)<br />

## Usage:

    root@bt:~# Dir-Xcan6.py -s https://testphp.vulnweb.com -f directorylist.txt -o Dir-Xcan-results.html -n 30 -p socks5://127.0.0.1:9050 -a username:admin
                -s http://192.168.0.1 -a admin:password -u Mozilla/4.0 -V
    
                -s = Target domain name or ip
                -f = Filename of the list you want to scan for (Default is "directorylist.txt" thats included in the repo)
                -o = Output Filename for logging of Code 200 Responses (Default is "Dir-Xcan-results.html")
                -n = Number of threads  (Default is 5)
                -p = HTTP Proxy settings (ip:port)
                -a = HTTP Basic Authentication (Username:Password)
                -u = User-Agent String (Default is "Mozilla/5.0")
                -V = Verbose Mode, Prints 200 and 401 codes to the screen.

                        
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
    			  - stuart@sensepost.com
    			  - www.sensepost.com // @sensepost

## Original Header:

    - This was written for educational purpose and pentests only. Use it at your own risk.
    - Author will be not responsible for any damage!
    - Toolname        : Dir-Xcan6.py
    - Coder           : stuart@sensepost.com // @NoobieDog
    - Version         : 6.0
