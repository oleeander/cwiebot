#!/usr/bin/python2
# -*- coding: utf-8 -*-

# cwiebot.py version 2.2.1 // sine 2.0 slower and with more bugs! (TM)
# Written 28 Jul 2011 by Oleander R (@fleischhorn)
# This work is released under the GNU GPL, version 2 or later.
# Usage: python2 cwiebot.py

import httplib2, tweepy, json, time, random, hashlib, os, sys
from BeautifulSoup import BeautifulSoup

# the following function is from adam @ stackoverflow
def smart_truncate(content, length=110, suffix='...'):
	if len(content) <= length:
		return content
	else:
		return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

#log
def log(text):
	try:
		logfile = open("/tmp/cwiebot_{0}.log".format(os.getpid()), "a")
		try:
			logfile.write(text + "\n")
		finally:
			logfile.close()
	except:
		pass

#formatting the log
def formatlog(text):
	text = time.strftime('[%F %T %Z]') + " [" + str(os.getpid()) + "] " + text
	log(text)
	return text

def tweet(obj, text, hash, lat, long):
	print formatlog("\033[91mtweeting:\033[0m {0}".format(text))
	try:
		obj.update_status(text, lat=lat, long=long)
	except Exception, e:
		pass
		print formatlog("\033[1;37;41merror tweeting {0}: {1}\033[0m".format(hash, e))
	else:
		print formatlog("\033[1;37;42mtweeted\033[0m {0}".format(hash))

def main():
	print formatlog("\033[1;37;42mstarted.\033[0m")
	#oauth foo
	auth = tweepy.OAuthHandler('consumertoken', 'consumersecret')
	auth.set_access_token('accesstoken', 'accesssecret')
	#access api
	twitter = tweepy.API(auth)

	#request the page (now a little bit more failsafe)
	while True:
		try:
			print formatlog("\033[1;37;42mloading...\033[0m")
			#create new http object
			http = httplib2.Http()
			#do the request
			status, content = http.request('http://c-wie.de/')
			if status['status'] == "200":
				print formatlog("\033[1;37;42mloaded.\033[0m")
			else:
				print formatlog("\033[1;37;42mdidn't get back 200.\033[0m")
				exit(0)
			break
		except Exception, e:
			pass
			print formatlog("\033[1;37;41merror: {0}. retry in 10 seconds...\033[0m".format(e))
			time.sleep(10)
	#create new beautifulsoup object from page
	website = BeautifulSoup(content)

	#find all links with the class main
	wiecs1 = website.findAll('a', attrs={'class' : 'main'})
	
	#create an empty array for the tweets
	wiecs2 = []
	sys.stdout.write("\033[32m")
	for wiec in wiecs1:
		#find the text and remove the "C wie "
		text = wiec.find(text=True).replace('C wie ', '').encode('utf-8')
		
		#get the destination
		link = wiec['href']
		
		#formatfoo
		wiec = '{0} http://c-wie.de{1}'.format(smart_truncate(text), link).decode('utf-8').encode('utf-8')
		
		#print
		print formatlog(wiec)
		
		#append tweet to list
		wiecs2.append(wiec)
	sys.stdout.write("\033[0m")

	#get hashes and import them as list object
	#$ echo "[]" > tweets.txt
	with open('tweets.txt') as dumper:
		tweets = json.load(dumper)

	#take five tweets if possible
	if len(wiecs2) >= 5:
		wiecs = random.sample(wiecs2, 5)
	else:
		wiecs = wiecs2
	
	formatlog("--")
	sys.stdout.write("\033[34m")
	for wiec in wiecs:
		print formatlog(wiec)
	sys.stdout.write("\033[0m")

	#counter
	count = 0
	#shortsleep false
	global shortsleep
	shortsleep = "0"
	
	for wiec in wiecs:
		#generate hash
		hash = hashlib.md5(wiec).hexdigest()
		
		#check if it's already tweeted
		if (hash in tweets) == False:
			#tweet them with the location of cdu mv HQ
			tweet(twitter, wiec, hash, lat="53.63568", long="11.40931")
			
			#append hash to list to mark as tweeted
			tweets.append(hash)
			
			#count up
			count = count + 1
			
			#sleep for a while
			if count < len(wiecs):
				seconds = random.randint(70,220)
				print formatlog("\033[34;40mwaiting {0} seconds...\033[0m".format(seconds))
				time.sleep(seconds)
		else:
			#sleep shortly
			shortsleep = "1"

	#save the hashes
	dumper = open('tweets.txt', 'w')
	json.dump(tweets,dumper)
	dumper.close()
	print formatlog("\033[1;37;42msaved tweets.\033[0m")

if __name__ == '__main__':
	while True:
		while True:
			try:
				main()
				break
			except Exception, e:
				pass
				print formatlog("\033[1;37;41merror: {0}. retry in 10 seconds...\033[0m".format(e))
				time.sleep(10)
		if shortsleep == "1":
			#stop being a timelineterrorist for a short time
			print formatlog("\033[1;37;42mreloading in 23 seconds...\033[0m")
			time.sleep(23)
		else:
			#stop being a timelineterrorist for a while
			print formatlog("\033[1;37;42mreloading in 240 seconds...\033[0m")
			time.sleep(240)
