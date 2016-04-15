#!/usr/bin/python
import praw
import os
import spotipy
import sys
import spotipy.util as util
import pprint
import re

#I removed any IDs or info related to what I use and left it blank.
user_agent = ("")
username=""
tid=""
pid=""
scope = 'playlist-modify-public'

Cid=""
Cs=""
SRI= "http://localhost:8888/callback"
onetrack=0
track_ids = []

r = praw.Reddit(user_agent = user_agent)

if not os.path.isfile("songlist.txt"):
    songlist = []
else:
    with open("songlist.txt", "r") as u:
        songlist = u.read()
        songlist = songlist.split("\n")
        songlist = filter(None, songlist)

subreddit = r.get_subreddit("poppunkers")

for submission in subreddit.get_top_from_week(limit=175):
    print(submission.title)
    num = submission.title.find(' - ')
    if num != -1:
         with open("songlist.txt", "a") as f:
            if len(sys.argv) > 1:
                search_str = sys.argv[1]
            else:
                submission.title.replace("-","")
                search_str = submission.title

            sp = spotipy.Spotify()
            result = sp.search(search_str)

            if '(' or ')' or '[' or ']' not in result:
                for i, t in enumerate(result['tracks']['items']):
                    if(onetrack<=0):
                        track_ids.append(t['id'])
                        onetrack=onetrack +1
                        f.write(submission.title)
                        f.write("\n")
                token = util.prompt_for_user_token(username, scope, Cid, Cs, SRI)
                if token:
                    sp = spotipy.Spotify(auth=token)
                    sp.trace = False
    onetrack=0
results = sp.user_playlist_add_tracks(username, pid, track_ids)
print(results)