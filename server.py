import socket
import spotipy
import spotipy.util as util
import json
from time import sleep, time
import requests
from bs4 import BeautifulSoup
import lxml
import sys

def waitForConnection():
	# get the hostname
	host = socket.gethostname()
	port = 5123  # initiate port no above 1024

	server_socket = socket.socket()  # get instance
	server_socket.bind((host, port))  # bind host address and port together

	while True:
		# configure how many client the server can listen simultaneously
		server_socket.listen(2)
		conn, address = server_socket.accept()  # accept new connection
		print("Connection from: " + str(address) + "\n")

		# receive data stream. it won't accept data packet greater than 1024 bytes
		data = conn.recv(4096).decode()
		if data:
			print("from connected user: " + str(data) + "\n")
			cmd, info = data.split(":")
			if cmd == "token":
				data = getToken(info)
			elif cmd == "lyric":
				song, artist = info.split(";")
				data = getLyrics(song,artist)
			conn.send(data.encode())  # send data to the client
			print("Sent data of length " + len(data) + " to user. \n")

	

def getToken(username):
	spotify_clientID="REMOVED"
	spotify_secret="REMOVED"
	hostname="http://localhost:8888/callback/"
	scope = "user-read-currently-playing"
	token = util.prompt_for_user_token(username, scope=scope, client_id=spotify_clientID, 
				client_secret=spotify_secret, redirect_uri=hostname)

	return token if token else "ERR"

def getLyrics(songName, artist):
	genius_clientID="REMOVED"
	genius_secret="REMOVED"
	hostname="http://localhost:8888/callback/"
	genius_token="REMOVED"
	
	headers = {'Authorization': 'Bearer ' + genius_token}
	data = {'q': songName + ' ' + artist}
	url = "https://api.genius.com/search"

	#get all hits matching our request
	response = requests.get(url, data=data, headers=headers, timeout=10)

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
		lyrics_page = requests.get(song_url, timeout=10).text
		soup = BeautifulSoup(lyrics_page, 'lxml')
		s = soup.find("div", {"class" : "lyrics"})
		if s is None:
			return "ERR"
		lyrics = soup.find("div", {"class": "lyrics"}).text

	return lyrics

if __name__ == '__main__':
	waitForConnection()
