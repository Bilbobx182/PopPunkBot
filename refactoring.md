## Looking back

So a 5 years ago, I wrote something to scrape reddit, and put the songs into a spotify playlist.

This project was something I was really proud of. _really_ proud of. 
It was the first project i produced something really cool and viable.
I hadn't looked at this code in years,now that I have, I am reminded of a quote from bojack horseman.
 _"When You Look at something through Rose-Colored Glasses, All the Red Flags Just Look Like Flags"_
 
But looking at it now, I cringe in some ways. A lot of things are wrong, a lot of things could be better.
Let's look at the red flags that lurked for me in something I took pride in.
 
 
## Global variables

There are arguments both [for](http://heather.cs.ucdavis.edu/~matloff/globals.html) and [against](https://softwareengineering.stackexchange.com/questions/47923/when-is-it-ok-to-use-a-global-variable
) global variables. But in this case I didn't need them, most of them could have existed within the scope of their functions.

Things like 
```
#Spotify Variables
pid = "playlist here"
scope = 'playlist-modify-private'
```


## Variable naming
You probably caught it from the above already, but my naming is far from perfect.
We all think we are good at it until, one day, we realise we're not. We're not infallible.

I originally had : 
```
pid = "playlist here"
Cid = 'Spotify client id'
Cs = 'Spotify client secret'
```

We could make this far more legible by making them constants and a normal variable.
```
SPOTIFY_CLIENT_ID = 'SPOTIFY_ID'
SPOTIFY_SECRET = 'SPOTIFY_SECRET'

spotify_playlist_id = 'ID here'
```
The reasoning for this is about [following convention](https://www.python.org/dev/peps/pep-0008/#constants).
The spotify client ID and secret shouldn't change and could in theory be shared with other components.
To avoid leaking them, keeping them in a secrets.py may be easier. Or even better pull them from something like AWS parameter store.

## Follow the conventions 

I know your IDE does most of this for you, but always take a look at the style guides.
[There are short summaries of them everywhere](https://tandysony.com/2018/02/14/pep-8.html).
When I originally wrote the script, I broke a lot of style rules.
This is important as it makes it harder to refactor, It makes it harder to read.
But most of all, if the rules are out the window, then it's harder to collaborate.
Try align your projects with the [zen of python](https://www.python.org/dev/peps/pep-0020/) 
"_Beautiful is better than ugly...Readability counts._"


## Ugly complexity and bad approaches.

I used to break convention a lot, be it method names or variables names.
Being truthful, I wrote some damn ugly code.
To put salt in the wound, I used to write some pretty naive approaches. 
Before adding a song to a playlist, I had a .txt file, of unsorted songs that I'd then search later to avoid adding duplicates.

```
if not os.path.isfile("songlist.txt"):
    songlist = []
else:
    with open("songlist.txt", "r") as u:
        songlist = u.read()
        songlist = songlist.split("\n")
        songlist = filter(None, songlist)
```
The issues with the above is, a raw '.txt' file is a pain in the ass to manage long term. 
It's unsorted, so the program will take increasingly longer to find duplicates.
If that file goes, my list of duplicates goes too.

But that's not the largest source of shame in the project. 
If I had the string of `[some text] Nujabes - Lady brown (ft. Cise Starr from CYNE)` I wanted
`Nujabes - Lady brown`, here was my approach to that :

```
info = '[some text] Nujabes - Lady brown (ft. Cise Starr from CYNE)'

        start = info.find('(')
        end = info.find(')')
        if start != -1 and end != -1:
            result = info[start:end + 1]
            info = info.replace(result, "")

    if any("[" or "]" in lis for lis in info):
        start = info.find('[')
        end = info.find(']')
        if start != -1 and end != -1:
            result = info[start:end + 1]
            info = info.replace(result, "")
```

When really I didn't need half that amount of code. I could have done it in a legible, one liner regex.
 `re.sub("[\(\[].*?[\)\]]", "", song_title_here)`
 
Things can often times be done much better, but to do things better you need experience or someone with expierence to review.

 
 ## Conclusion
 
 I like ending things on a positive note.
 If there's anything I want you to take away from this, it's nothing about style guides nor variable naming.
 What I want you to take away from this read is one thing "motivation".
 Do you think I improved overnight? Nope.
 
 I've improved a lot in the past years, but that was chipping away at my craft each day.
 That means every time you create,write, and make something new. You improve too !
Chances are, you  can do a lot more than you did 5 years ago. You can achieve a lot more tomorrow than you did today.
 You just need to keep on making steps and strides towards that better future.