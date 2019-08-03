A short program that displays the lyrics for whatever you're currently listening to on Spotify in the terminal.  
  
Dependencies:  
      - Beautiful Soup 4  
      - Spotipy  
  
To run this you'll need a Spotify API client and secret (and username), as well as a Genius API client, secret, and access token. place all these into a config in the same directory as spotify.py with the format:

username=[Spotify username]  
spotify_clientID=[Spotify client id]  
spotify_secret=[Spotidy secret]  
genius_clientID=[Genius client id]  
genius_secret=[Genius secret]  
hostname=[hostname url (localhost is usually fine)]  
genius_token=[Genius access token]  
  
You'll need to authenticate your spotify account with the app on the first run.

See the following link for example output:  
https://imgur.com/a/EjkTpV4  
  
Known Issues:  
	- Rarely the same song and lyrics will be briefly printed when switching songs, the clear command makes this relatively unnoticeable and increasing the minimum bound further may make things feel slow   
	- if artist name isnt a 100% match the genius lookup will return None. This is only an issue for bands with multiple aliases (ex. 3OH!3, IDKHow, etc.) and seems infrequent.  
	- Genius requests some times take forever  

