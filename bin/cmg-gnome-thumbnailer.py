#! /usr/bin/python

"""
 Klik CMG Thumbnailer 
 Created by : Jason Taylor (KillerKiwi)
 Created on : 26-Sep-2005
 Last Update : 11-Oct-2005
 Last Update By : Jason Taylor (KillerKiwi)

 Comments :	This is my first python script :)
		Need to read file from the end 
		This is all we need for gnome


 UPDATE: probono has spoken ;) the ar file format will be used script updated to scan for ar file 
		and extract given file.
		Note: Scanning for the ar like this is not ideal and should be dropped at some point
		- Jason Taylor 28-Sep-2005


 AR File header format:

       char    ar_name[16];      /* 16 - '/' terminated file member name (FileName) */  
       char    ar_date[12];      /* 28 - file member date */ 
       char    ar_uid[6];        /* 34 - file member user identification */ 
       char    ar_gid[6];        /* 40 - file member group identification */ 
       char    ar_mode[8];       /* 48 - file member mode (octal) */ 
       char    ar_size[10];      /* 58 - file member size (FileSize) */ 
       char    ar_fmag[2];       /* 60 - header trailer string */ 

"""

ICON_FILE_NAME = "icon"
AR_MAGIC = "!<arch>\n"
BLKSIZE = 10000
MAXCYCLES = 1000

import getopt 
import sys
import os
import string
import StringIO
#import Image, ImageDraw # Try images
from Numeric import *

def FindAr( file ):
	
	buffer = ""

	# Set pointer to end of file
	file.seek(0, 2)

	# Seek backwards for a number of cycles
	for i in range( MAXCYCLES ):

		try:

			pos = file.tell()
			offset = BLKSIZE

			# Check for valid position
			if pos - BLKSIZE < 0: 
				offset = pos;
			if offset < 0:
				return 0;

			# Move pointer
			file.seek( -offset, 1)

		        # Get new chunk to buffer 
			buffer = file.read(offset + len(AR_MAGIC)) 
			
			# Move pointer back, read moves pointer on
			file.seek( -len(buffer), 1)	

			# Test for divider
			test = buffer.rfind( AR_MAGIC )

			# If divider is found
			if test > -1:
				file.seek(  test + len( AR_MAGIC ) ,1)
				print "Found an AR archive : " 
				print pos
				return 1

		except: 
			print "No Ar Found"
			return 0

		
	print "No Ar Found"
	return 0

def ExtractFile(file, filename):
	try:
		ar_file_detail = file.readline()
		file_name_chunk = ar_file_detail[0:16].strip()
		file_size_chunk = ar_file_detail[48:58].strip()
		
		# Strip trailing char in filename
		file_name = file_name_chunk[:len(file_name_chunk)-1]
		# Convert string to number
		file_size = int(file_size_chunk)

		print "Found a file : " + file_name +" (" + file_size_chunk +" bytes)"

		if file_name == filename:

			buffer = file.read( file_size )
			print "Found The Correct File!  Extracting..."
			return buffer

		# Skip to next file and test
		file.seek( file_size, 1)
		return ExtractFile(file, filename)
	except:
		print "Error occured while reading ar"
		return 

def GetFileFromAr( ar, filename):
	file = open( ar, "r" )
	result = FindAr( file )
	#file.seek( 140, 1)
	if result == 1:
		return ExtractFile( file, filename )
	return None

def main():
	input = sys.argv[1]
	output = sys.argv[2]

	buffer = GetFileFromAr( input, ICON_FILE_NAME )

	if buffer != None:
		file = open( output , "w")
		file.write( buffer )
		file.close()
				
		del file

if __name__ == "__main__":
	main()
