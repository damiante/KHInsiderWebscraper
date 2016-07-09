#!/usr/bin/python

# downloads.khinsider.com webscraper, written by Damian Testa, 09/07/2016
# This Python program crawls over game soundtrack pages at khinsider.com and
# scrapes all the MP3 files from a soundtrack. It was written out of frustration
# at the khinsider.com system of directing traffic to the site in exchange for
# album downloads. Just give it the url of the page which lists all of the
# available mp3 files for that game, and it will fetch all of those files and
# dump them into a folder for you.

import os
import sys
import urllib
from lxml import html

HASHLEN = 10

url = raw_input("Enter a url to scrape for mp3 files: ")

#Check to see if a valid album name exists within the given url. An example
#is "http://downloads.khinsider.com/game-soundtracks/album/jade-cocoon", which
#has the valid album name of "jade-cocoon"

try:
	albumname = url[url.index("album/")+6:]
except ValueError:
	print "Error: URL contains no valid album title."
	sys.exit()

if not os.path.exists("./" + albumname):
	os.makedirs(albumname)

page = html.fromstring(urllib.urlopen(url).read())

for link in page.xpath("//a"):
	#There are often two links to the same thing, so avoid repetition
	#by checking the link's text for "Download"

	if link.text == "Download":
		continue
	thislink = link.get("href")

	if albumname in thislink:
		subpage = html.fromstring(urllib.urlopen(thislink).read())

		for sublink in subpage.xpath("//a"):
			target = sublink.get("href")

			if not target.endswith(".mp3"):
				continue

			#filename is the end of the url, after the final slash.

			finalslashpos = 0
			for i in range(len(target)):
				if target[i] == "/":
					finalslashpos = i

			filename = target[finalslashpos:]
			urllib.urlretrieve(sublink.get("href"),\
			"./" + albumname + "/" + filename)
