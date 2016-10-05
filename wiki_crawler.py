
from HTMLParser import HTMLParser
import re
import sys
import getopt
import os
import string
import io
import urllib2
import lxml
from lxml import etree
import httplib


meta_text_check = 0
end = 0
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
		global end 
		if end == 1 :
			return;
		global meta_text_check
		if meta_text_check == 0 :
			if tag == 'div':
				for name, value in attrs:
					if name == 'id' and value == 'mw-content-text':
						meta_text_check = 1
		
		else :
			for name, value in attrs:
				if not ((name == 'class' and value == 'reference') or (name == 'class' and value == 'mediawiki') or (name == 'class' and value == 'image') or (name == 'class' and value == 'thumb')):
					if tag == 'a':
						for name, value in attrs:
							if name == 'href':
								file("f1.txt", "a").write(value)
								file("f1.txt", "a").write("\n")
								
					if tag == 'div':
						for name, value in attrs :
							if name == 'id' and value == 'mw-hidden-catlinks':
								end = 1
								return;
						
						
						
html_page = urllib2.urlopen(sys.argv[1]).read()

parser = MyHTMLParser()
parser.feed(html_page)

lines_seen = set() # holds lines already seen
outfile = open("f2.txt", "a")
for line in open("f1.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

os.remove("f1.txt")

shakes = open("f2.txt", "r")
outfile = open("f3.txt","a")

for line in shakes:
    if re.match("/wiki/(.*)", line):
        outfile.write(line)

shakes.close()
outfile.close()

os.remove("f2.txt")


fout = open("f4.txt","a")
for line in open("f3.txt","r"):
		line = line[6:]
		fout.write(line)

fout.close()

os.remove("f3.txt")


with open('f4.txt') as rd:
	items = [x.strip() for x in rd.readlines()]

os.remove("f4.txt")

max = -1
i = -1
index = -1

highest = 0
url_str = "none"
#counting the number of backlinks each link in the page has and finding the one with highest backlinks 
for str1 in items:
	i = i+1
	str2 = "https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/"
	str3 = str2 + str1 + "&limit=sys.maxint"
	try:
            response = etree.HTML(urllib2.urlopen(str3).read())
        except (httplib.HTTPException, httplib.IncompleteRead, urllib2.URLError):
            missing.put(str3)
            continue

        current  =  len(response.xpath('//*[@id="mw-whatlinkshere-list"]//li/a'))
        if(current > highest):
            highest = current
            url_str = str1
print url_str
print "https://en.wikipedia.org/wiki/" + url_str




