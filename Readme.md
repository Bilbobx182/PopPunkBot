PopPunkBot

A bot I use to take Artist and song names from reddit/r/poppunkers and add the top of the week to spotify.

For the python script to work you need the spotify credentials for apps. server.js deals with the authentication.

How to run: 
0) Have Spotify, Node.js, and Python 3 installed.

https://www.spotify.com/ie/download/windows/

https://nodejs.org/en/

https://www.python.org/downloads/

Open command prompt and type in the following:
pip install praw
pip install spotipy
pip install beautifulsoup4
pip install requests

Now we have all the libraries and all the programs needed.

1) Start the server.js by typing in "Node server.js" into command prompt/terminal(Note, I haven't tested this in any osX nor any Linux distro).

2) Edit the Python code, you will want to change the following variables. 

	username ="Spotify Username goes here"
	
	pid = "Spotify playlist URI goes here"
	
	sub="The subreddit you want to scrape music from goes here"

3) Start the python program, it will ask you to validate yourself. Then you simply copy and paste the validated URL back to the cmd prompt. 

4) Hopefully it should add it all for you to the playlist.


If you still can't figure it all out here's a youtube video of me going through it. https://youtu.be/dMox-eKDXs0