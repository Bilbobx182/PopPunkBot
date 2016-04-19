#!/usr/bin/python
import praw
import os
import spotipy
import sys
import spotipy.util as util

#"Declaring" variables for the first time.
user_agent = ("bilbobx182crawler")
username ="eternal_atom"
tid = ""
pid = "03VDb9C66xFlisFCMqxgwz"
scope = 'playlist-modify-public'

Cid = "1b2904aec1c64e45941b35bfe7a66792"
Cs = "a7f0819ab0fa4cee99d7d8f3a34d6193"
SRI = "http://localhost:8888/callback"
onetrack = 0
track_ids = []
sub = "music"

r = praw.Reddit(user_agent = user_agent)

# Checking to see if a text file for song list(They're the spotify URI codes) is there
if not os.path.isfile("songlist.txt"):
    songlist = []
else:
    with open("songlist.txt", "r") as u:
        songlist = u.read()
        songlist = songlist.split("\n")
        songlist = filter(None, songlist)


# tells it to go to /r/poppunkers
subreddit = r.get_subreddit(sub)
counter=0
# the main loop of the program, it tells it as long as there's a submission in the top X amount loop around.
for submission in subreddit.get_top_from_week(limit=1000):
    num = submission.title.find(' - ')
    if num != -1:
        with open("songlist.txt", "a") as f:
            # The format for songs is "Artist - Song ()" This way we can assume MOST titles that have a " - " are a song.
            if(" - " in submission.title):
                counter=counter+1
                submission.title.replace("-","")
                search_str = submission.title

                # Checking to see if the song has any extra stuff after artist - song generally extra is tagged with () so we remove them.
            if any("(" or ")" in lis for lis in search_str):
                start = search_str.find('(')
                end = search_str.find(')')
                if start != -1 and end != -1:
                    result = search_str[start:end + 1]
                    search_str = search_str.replace(result,"")
            else:
                search_str = submission.title

            # however some users submit it in a wrong format with [] instead so we remove those too
            if any("[" or "]" in lis for lis in search_str):
                start = search_str.find('[')
                end = search_str.find(']')
                if start != -1 and end != -1:
                    result = search_str[start:end + 1]
                    search_str = search_str.replace(result, "")
            else:
                search_str=submission.title
            print(search_str)

            # Creating the spotify query to see if a song is in it's database.
            sp = spotipy.Spotify()
            result = sp.search(search_str)
            for i, t in enumerate(result['tracks']['items']):
                # gets the first track ID and only that ID so it wont repeat through album or singles
                if (onetrack <= 0):
                        track_ids.append(t['id'])
                        onetrack = onetrack + 1
                        f.write(t['id'])
                        f.write("\n")

#so the program can handle high amounts of tracks
        if (len(track_ids) > 80):
            token = util.prompt_for_user_token(username, scope, Cid, Cs, SRI)
            if token:
                sp = spotipy.Spotify(auth=token)
                sp.trace = False
                results = sp.user_playlist_add_tracks(username, pid, track_ids)
                print(len(track_ids))
                track_ids.clear()
        onetrack = 0
print(len(track_ids))
#Adding the track to spotify

