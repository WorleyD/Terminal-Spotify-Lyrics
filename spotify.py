import spotipy
import spotipy.util as util
import json
from time import sleep, time
import requests
from bs4 import BeautifulSoup
import lxml

def get_lyrics(response):
	#get response as json
	response = response.json()

	song_url = None
	lyrics = None
	#find the first match for our artist 
	#(its highly unlikely an artist will have two songs with the same name)
	for song in response['response']['hits']:
		#get artist name from request
		i = song['result']['primary_artist']['name'].lower()
		#Special case because genius uses dumb apostrophes that spotify doesnt
		if "’" in i:
			i = i.replace("’","")
		if artist.lower() in i:
			song_url = song['result']['url']
			break
	
	#if we found a matching song, try to parse lyrics
	if song_url is not None:
		#get the page as text, parse it with bs4
		lyrics_page = requests.get(song_url, timeout=5).text
		soup = BeautifulSoup(lyrics_page, 'lxml')
		lyrics = soup.find("div", {"class": "lyrics"}).text

	return lyrics

param_dict = {}

clear = "\n"*55

#read in all client ids and secrets from a config file and store them in a dict
with open("config", "r") as f:
	params = f.read()
	options = params.split('\n')
	if len(options) == 1:
		options = params.split('\r')
	for line in options:
		key,value = line.split("=")
		param_dict[key] = value

#set scope and token for spotify
scope="user-read-currently-playing"
token = util.prompt_for_user_token(param_dict["username"], scope=scope, client_id=param_dict["spotify_clientID"], 
				client_secret=param_dict["spotify_secret"], redirect_uri=param_dict["hostname"])

#if we properly authenticated
if token:
	sp = spotipy.Spotify(auth=token)

	#clear the console initially for cleaner output
	print(clear)
	while True:
		#get currently playing track from spotify
		track = sp.current_user_playing_track()

		info = track['item']

		#pull the song name and artist from the spotify resposne
		artist = info['album']['artists'][0]['name']
		song = info['name']
		
		#trim any extras off song title for easier genius searching (ex. Song - Single or Song - Stripped)
		if " - " in song:
			song_title = song[0:song.find("-")-1]
		else:
			song_title = song
		done = track['progress_ms']
		total = info['duration_ms']
		time_left = total - done
		seconds = time_left/1000
		start = time()
		#build request for genius
		print(artist, " - ", song)
		headers = {'Authorization': 'Bearer ' + param_dict["genius_token"]}
		data = {'q': song_title + ' ' + artist}
		url = "https://api.genius.com/search"

		#get all hits matching our request
		response = requests.get(url, data=data, headers=headers, timeout=5)

		#find the right lyeics page and parse it with bs4
		lyrics = get_lyrics(response)

		#print lyrics if we parsed them
		if lyrics is not None:
			print(lyrics)
		else:
			print("Sorry, lyrics could not be found :( ")
		
		end = time()

		#remove execution time from sleep for more accurate sleep
		elapsed = end-start

		#prevent a really slow request from making sleep time negative
		if elapsed > seconds:
			elapsed = 0
			seconds = 0.5		

		#sleep for the rest of the song
		sleep(seconds - elapsed + 0.4)
		#clear the console
		print(clear)	
		
