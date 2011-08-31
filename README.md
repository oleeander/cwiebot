C wie .. bot
============

What?
-----
This is a some kind of a bot which gets a website, processes it and grabs content to tweet it.

How?
----
It's implemented in Python 2 and uses BeautifulSoup and tweepy.

After selecting an entry "randomly" out of a couple of entrys it generates a hash and look for it in a json object which is stored in a file. If it 
isn't in, it tweets the entry, adds the hash to the json object and saves the file.

Many actions will be logged in another file and in the terminal using colours. (great for screen)

Where?
------
[here](https://twitter.com/cwiezukunft).
