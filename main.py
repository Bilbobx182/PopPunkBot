#!/usr/bin/python
import praw
import os
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
import requests

#Reddit variables
user_agent = ("bilbobx182crawler")
sub = "poppunkers"
r = praw.Reddit(user_agent = user_agent)

# Spotify variables
pid = "6GXK27XsRSngHWROTtOsst" #playlist id
username ="eternal_atom" #Spotify username
scope = 'playlist-modify-private' #scope of playlist
Cid = "1b2904aec1c64e45941b35bfe7a66792" # Spotify ID
Cs = "a7f0819ab0fa4cee99d7d8f3a34d6193" # Spotify secret ID
SRI = "http://localhost:8888/callback" # Host

onetrack = 0
track_ids = []

if not os.path.isfile("songlist.txt"):
    songlist = []
else:
    with open("songlist.txt", "r") as u:
        songlist = u.read()
        songlist = songlist.split("\n")
        songlist = filter(None, songlist)


def titleparse(songdata,num):

    info=songdata
    global onetrack
    global track_ids
    
    # Only used if it's a link and the title is wrong AND it's a youtube link so it gets the YT video title.
    if num==1:
        response = requests.get(songdata)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        title = title.split('-')
        titlelen = len(title)
        fixedtitle = ""
        i = 0
        while (i < (titlelen - 1)):
            fixedtitle = fixedtitle + title[i]
            i += 1
        info = fixedtitle

    if " - " in info:
        info.replace("-", "")

    if any("(" or ")" in lis for lis in info):
        start = info.find('(')
        end = info.find(')')
        if start != -1 and end != -1:
            result = info[start:end + 1]
            info=info.replace(result, "")

    # however some users submit it in a wrong format with [] instead so we remove those too
    if any("[" or "]" in lis for lis in info):
        start = info.find('[')
        end = info.find(']')
        if start != -1 and end != -1:
            result = info[start:end + 1]
            info = info.replace(result, "")

    sp = spotipy.Spotify()
    # Creating the spotify query to see if a song is in it's database.
    with open("songlist.txt", "a") as f:
        result = sp.search(info)
        for i, t in enumerate(result['tracks']['items']):
            # gets the first track ID and only that ID so it wont repeat through album or singles
            if onetrack <= 0:
                temp = t['id']
                if temp in songlist:
                    # For Duplicates
                    print("ITS HERE ALREADY")
                    break
                else:
                    track_ids.append(t['id'])
                    onetrack = onetrack + 1
                    f.write(t['id'])
                    f.write("\n")

    print("DONE: " + info)

# tells it to go to /r/poppunkers
subreddit = r.get_subreddit(sub)
counter=0

# the main loop of the program, it tells it as long as there's a submission in the top X amount loop around.
for submission in subreddit.get_top_from_week(limit=300):
    num = submission.title.find(' - ')
    if num != -1:
        titleparse(submission.title, 0)

    elif 'youtu' in submission.url:
        titleparse(submission.url, 1)

    if len(track_ids) > 80:
        token = util.prompt_for_user_token(username, scope, Cid, Cs, SRI)
        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, pid, track_ids)
            print(len(track_ids))
            track_ids.clear()
    onetrack = 0

if 80 >= len(track_ids) > 0:
    token = util.prompt_for_user_token(username, scope, Cid, Cs, SRI)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, pid, track_ids)
        track_ids.clear()
print(len(track_ids))
