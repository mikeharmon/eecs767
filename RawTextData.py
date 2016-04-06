#!/usr/bin/env python
#    -*-    encoding: UTF-8    -*-
import sys
import os
import errno
import logging
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from os import listdir
from os.path import isfile, join


class MyHTMLParser(HTMLParser):

#	def handle_starttag(self, tag, attrs):
#		fo.write('self \n')
#		fo.write('{} {} {} \n'.format(self, tag, attrs))		
#	def handle_endtag(self, tag):
#fo.write("%s %s \n")
#		fo.write('{} {} \n'.format(self, tag))	
#   def handle_data(self, data):
#		self.getpos()
#		fo.write("%s %s %s \n")
#		fo.write('{} \n'.format(data))

	def handle_data(self, data):
		fo.write(data.encode('utf8') + '\n')

		
userpath = raw_input("Enter the directory with your files: ")
targetfiles = [f for f in listdir(userpath) if isfile(join(userpath, f))]
print "The following files will be parsed: \n"
for f in (targetfiles):
	print f
try:
	input("\n\nPress enter to continue")
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
	output_text = file_name+".raw"
	try:
		fo = open('./temp_dir/'+output_text, "w")
#		fo = open('./temp_dir'+output_text, "w")		
	except IOError:
		print "There was an error writing file"
		sys.exit() 
	parser = MyHTMLParser()
	parser.feed(file_text)         
	fo.close()                     
	parser.close() 
	
	
    