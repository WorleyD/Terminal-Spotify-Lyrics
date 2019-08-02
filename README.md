A terminal based spotify app that displays the lyrics for whatever you're currently listening to. 
  
Dependencies:  
  -Beautiful Soup 4
  -Spotipy
  
To run this you'll need a Spotify API client and secret (and username), as well as a Genius API client, secret, and access token. place all these into a config in the same directory as spotify.py with the format:

username=[Spotify username]  
spotify_clientID=[Spotify client id]  
spotify_secret=[Spotidy secret]  
genius_clientID=[Genius client id]  
genius_secret=[Genius secret]  
hostname=http://localhost:8888/callback/  
genius_token=[Genius access token]  

You'll need to authenticate your spotify account with the app on the first run
