import praw
import time

sub = 'poppunkers'
user_agent = ("bilbobx182crawler")
r = praw.Reddit(user_agent=user_agent)
REDDIT_USERNAME =
REDDIT_PASS =
r.login(REDDIT_USERNAME, REDDIT_PASS)

title="What Are You Listening To?"+'('+time.strftime("%B,")+" week :" + time.strftime("%U ")+ time.strftime("%Y") + ')'

body="""For those that are new, the drill is we discuss any artist/album/genre/song that you listened to this week."

Also feel free to discuss any bands that are touring or even a tiny bit of self promotion"""

footer= """
____________________

Looking for playlists?"

[/r/poppunkers updated weekly](https://open.spotify.com/user/eternal_atom/playlist/6GXK27XsRSngHWROTtOsst)

[/r/poppunkers all time](https://open.spotify.com/user/eternal_atom/playlist/1rhn3N89QlT2jGRTRR3hBy)

If there are any problems with this bot,or if you love it pm /u/eternal_atom"""

r.submit(sub, title, body + footer)




