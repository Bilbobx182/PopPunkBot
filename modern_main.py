import praw
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secrets import PRAW_TOKEN_SECRET, PRAW_TOKEN_ID, SPOTIFY_SECRET, SPOTIFY_ID
import re
from datetime import datetime


def get_now():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def get_song_titles():
    subs = ['poppunkers', 'hiphopheads', 'emo', 'importedhiphop']
    titles = []

    reddit_con = praw.Reddit(
        client_id=PRAW_TOKEN_ID,
        client_secret=PRAW_TOKEN_SECRET,
        user_agent="TaifuWiddies")

    for submission in reddit_con.subreddit("+".join(subs)).hot(limit=100):
        print(f'www.reddit.com/{submission.permalink}')
        if ("-" in submission.title):
            titles.append(re.sub("[\(\[].*?[\)\]]", "", submission.title).lstrip())
    return titles


def get_track_IDs(track_titles):
    sp_scope = "playlist-modify user-library-read user-read-private playlist-modify-private user-library-modify"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=sp_scope,
                                                   client_secret=SPOTIFY_SECRET,
                                                   client_id=SPOTIFY_ID,
                                                   redirect_uri='http://localhost:8000/'))
    playlist = sp.user_playlist_create(user='eternal_atom', name=f"Test {get_now()}", public=False,
                                       description='Auto gened by xyz')
    spotify_tracks = []
    for track in track_titles:
        result = sp.search(track)
        if len(result['tracks']['items']) > 0:
            spotify_tracks.append(result['tracks']['items'][0]['uri'])
    sp.playlist_add_items(playlist_id=playlist['id'], items=spotify_tracks)


def main():
    print(get_now())
    get_track_IDs(get_song_titles())
    print(get_now())
main()
