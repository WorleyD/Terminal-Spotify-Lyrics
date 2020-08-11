import socket
import spotipy
import spotipy.util as util
from time import sleep

HOSTNAME = socket.gethostname()
PORT = 5123
clear = "\n"*55

def getToken(username):
	host = HOSTNAME  # as both code is running on same pc
	port = PORT  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	message = "token:" + username
	client_socket.send(message.encode())  # send message
	token = client_socket.recv(1024).decode()  # receive response
	client_socket.close()  # close the connection

	return token

def getLyrics(songName, artist):
	host = HOSTNAME  # as both code is running on same pc
	port = PORT  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	message = "lyric:" + songName + ";" + artist
	client_socket.send(message.encode())  # send message
	lyrics = client_socket.recv(4096).decode()  # receive response
	client_socket.close()  # close the connection

	return lyrics


if __name__ == '__main__':
	print("Please enter your spotify username")
	username = input()
	while True:
		token = getToken(username)
		print("Token received: " + token)
		while token:
			if token != "ERR":
				sp = spotipy.Spotify(auth=token)

				#Sometimes the first song does not load properly, likely an issue here
				sleep(1)
				#clear the console initially for cleaner output
				print(clear)

				
				#get currently playing track from spotify
				track = sp.current_user_playing_track()
				if track == None:
					print("No track playing! Exiting..")
					sys.exit(1)
					
				info = track['item']

					#pull the song name and artist from the spotify resposne
				artist = info['album']['artists'][0]['name']
				song = info['name']
					
				#trim any extras off song title for easier genius searching (ex. Song - Single or Song - Stripped)
				if " - " in song:
					song_title = song[0:song.find("-")-1]
				else:
					song_title = song

				print(clear)
				print(artist," - ",song)

				lyrics = getLyrics(song_title, artist)
					
				print("\n", lyrics)

				while True:
					t = sp.current_user_playing_track()
					i = t['item']
					s = i['name']
					if s != song:
						#print(s, song)
						break
					sleep(1)

				#clear the console
				print(clear)	
		