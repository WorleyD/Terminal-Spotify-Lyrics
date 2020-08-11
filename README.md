
A short program that displays the lyrics for whatever you're currently listening to on Spotify in the terminal.  
  
  This program was recently refactored and is currently unstable and unhosted. 

## **Client Dependencies:**

      - Python3
      - Spotipy
  


## **Run instructions (Once server is hosted):**

	 1. Install Python 3 	
	 2. Install Spotipy library (use command ```pip
	    install spotipy```) 	
	 3. Download client.py 	
	 4. Start listening to spotify
	 5. Launch client.py 	
	 6. Enter your username 	
	 7. Follow login and authentication prompt 	
	 8.  Enjoy!

  


See the following link for example output:  
https://imgur.com/a/EjkTpV4  
 
  

## **Known Issues:**

	1. Lyrics sometimes do not return properly, but work if refreshed (e.g. going back to the same song)
		- Proposed Solution: Implement multiple checks for lyrics up to a certain maximum

	2. Genius requests some times take forever  
		- Proposed Solution: Perhaps switch from Requests to a better library

	3. Program crashes when spotify token expires
		- Proposed Solution: Not sure yet, find some clean way to regenerate it 

 
If a token expires while in use, simply relaunch the program until I find a convenient workaround :)
