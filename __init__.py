#!/usr/bin/python
import praw
import os
import spotipy
import sys
import spotipy.util as util
import pprint
import re

#"Declaring" variables for the first time.
user_agent = ("")
username=""
pid=""
scope = 'playlist-modify-public'

Cid=""
Cs=""
SRI= "http://localhost:8888/callback"
onetrack=0
track_ids = []

r = praw.Reddit(user_agent = user_agent)

#Checking to see if a text file for song list si there
if not os.path.isfile("songlist.txt"):
    songlist = []
else:
    #otherwise it reads the song list and splits it at each new line
    with open("songlist.txt", "r") as u:
        songlist = u.read()
        songlist = songlist.split("\n")
        songlist = filter(None, songlist)

#tells it to go to /r/poppunkers
subreddit = r.get_subreddit("poppunkers")
#the main loop of the program, it tells it as long as there's a submission in the top X amount loop around.
for submission in subreddit.get_top_from_week(limit=175):
    print(submission.title)
    #The format for songs is "Artist - Song ()" This way we can assume MOST titles that have a " - " are a song.
    num = submission.title.find(' - ')
    if num != -1:
        #opeining songlist in append so we can add new songs as we go in the append.
         with open("songlist.txt", "a") as f:
            if len(sys.argv) > 1:
                search_str = sys.argv[1]
            else:
                #remove the "-" as it will mess with spotify.
                submission.title.replace("-","")
                search_str = submission.title

            #Creating the spotify query to see if a song is in it's database.
            sp = spotipy.Spotify()
            result = sp.search(search_str)

            #dealing with errors, if the song has a () [] it wont try add it
            if '(' or ')' or '[' or ']' not in result:
                for i, t in enumerate(result['tracks']['items']):
                    # gets the first track ID and only that ID so it wont repeat through album or singles
                    if(onetrack<=0):
                        track_ids.append(t['id'])
                        onetrack=onetrack +1

                        # writes the title the file
                        f.write(submission.title)
                        f.write("\n")
                #Connecting to Spotify
                token = util.prompt_for_user_token(username, scope, Cid, Cs, SRI)
                if token:
                    sp = spotipy.Spotify(auth=token)
                    sp.trace = False
    onetrack=0
    #adds the track to Spotify playlist
results = sp.user_playlist_add_tracks(username, pid, track_ids)
print(results)