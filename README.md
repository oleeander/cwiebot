C wie .. bot
============

What?
-----
This bot periodically fetches a website, processes it and sends grabbed content to twitter.

How?
----
It's implemented in Python 2 and uses BeautifulSoup and tweepy.

After selecting an entry "randomly" out of a couple of entries, it generates a hash and looks for it in a json object which is stored in a file. If it 
isn't in there, it will tweet the entry after adding the hash to the json object and will update the file.

Many actions are logged in another file and in the terminal using colours. (great for screen)

Where?
------
[here](https://twitter.com/cwiezukunft).
