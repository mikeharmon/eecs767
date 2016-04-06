#!/usr/bin/env python
#    -*-    encoding: UTF-8    -*-

import sys
import os
import errno
import logging
import re
from os import listdir
from os.path import isfile, join
from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint


class WikiHTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'br') and not self.hide_output:
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p':
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r'\s+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = unichr(name2codepoint[name])
            self._buf.append(c)

    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._buf.append(unichr(n))

    def get_text(self):
        return re.sub(r' +', ' ', ''.join(self._buf))

def html_to_text(html):
    """
    Given a piece of HTML, return the plain text it contains.
    This handles entities and char refs, but not javascript and stylesheets.
    """
    parser = WikiHTMLToText()
    try:
		os.chdir('C:\HTMLdocs')
		fo = open(file_name, "r")
#		fo = open('Acadia_National_Park.htm', "r")
		file_text = fo.read().decode('utf8')
		parser.feed(file_text)
		parser.close()
    except HTMLParseError:
        pass
    return parser.get_text()

def text_to_html(text):
    """
    Convert the given text to html, wrapping what looks like URLs with <a> tags,
    converting newlines to <br> tags and converting confusing chars into html
    entities.
    """
    def f(mo):
        t = mo.group()
        if len(t) == 1:
            return {'&':'&amp;', "'":'&#39;', '"':'&quot;', '<':'&lt;', '>':'&gt;'}.get(t)
        return '<a href="%s">%s</a>' % (t, t)
    return re.sub(r'https?://[^] ()"\';]+|[&\'"<>]', f, text)

	
userpath = raw_input("Enter the directory with your files: ")
targetfiles = [f for f in listdir(userpath) if isfile(join(userpath, f))]
print "The following files will be parsed: \n"
for f in (targetfiles):
	print f
try:
	input("\n\nPress enter to begin processing files\n\n")
except SyntaxError:
    pass

os.chdir(userpath)   # Change current working directory

if os.path.isdir('./temp_dir'):		# Create a temporary subdirectory to store working files
    pass
else:
    os.mkdir('./temp_dir')
	
for file_name in (targetfiles):
	try:
		fo = open(file_name, "r")
	except IOError:
		print "There was an error reading file"
		sys.exit()
	print "Processing file: ",file_name
	file_text = fo.read().decode('utf8')
	output_text = file_name+".ftxt"
	try:
		fo = open('./temp_dir/'+output_text, "w")

	except IOError:
		print "There was an error writing file"
		sys.exit() 
	documenttext = html_to_text(file_text)
	fo.write(documenttext.encode('utf8') + '\n')
	fo.close()                     
 


    

