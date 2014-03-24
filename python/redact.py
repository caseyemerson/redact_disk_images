# ******************************************************************************
# This code was written by Casey Emerson on 1/9/14 for his Masters Paper at the 
# University of North Carolina School of Information and Library Science.
#
# This script reads a bookmark created by bulk_extractor file that contains one
# or more feature offsets to be redacted. It determines the format of the image
# file and if necessary, converts the image file to RAW for redaction. It then
# overwrites the offsets, and if necessary, converts the image back into the
# original file format.
# 
# For proprietary forensic image files, the script also transfers any DFXML from 
# the original file into the newly cleansed file. In addition, it appends the 
# notes section of the DFXML with the offsets and lengths of the redacted blocks
# of the disk.
# ******************************************************************************


"""IMPORTS GO HERE"""

import argparse
import os
from time import localtime, strftime
import re
import subprocess
import xml.etree.ElementTree as ET
import string



"""VARIABLES DEFINED HERE"""

offset = []	# global initialization of this empty list variable
length = []	# global initialization of this empty list variable
feature = []	# global initialization of this empty list variable
flags = {}	# define dictionary (key value pair)
saveFilePath = os.getcwd()	# get the current working directory


""" FUNCTIONS GO HERE"""

def parseBookmarks(BookmarkFile):	# open and parse the Bulk_Extractor bookmark file
	log.write('\n' + (strftime("%H:%M:%S %b %d, %Y - processing bookmark file located at: ", localtime())) + (BookmarkFile) + '\n')	# enter into log
	with open(BookmarkFile, "r") as file:		# open the bookmark file in read mode
    		for line in file:			# parse each line of the file
			if re.match(r'[0-9]+,', line):	# look for the offset (a sequence of numbers followed by a comma)
				try:
					line = line.split(', ')	# split the line into pieces using ', ' delimeter
					offset.append(line[0])	# append the first part of the line into the offset list
					feature.append((line[3]).rstrip())		# append the third part of the line into the feature list
					length.append(len((line[3]).rstrip()))		# calculate the length of the feature and append it into the length list				
				except: 
					print('Doh! something went wrong matching the offset')	# if there was a problem, display an error
					log.write((strftime("%H:%M:%S %b %d, %Y - ERROR parsing offset " + offset + " in the bookmark file ", localtime())) + '\n')	# enter into log

	log.write((strftime("%H:%M:%S %b %d, %Y - Finished parsing the bookmark file ", localtime())) + '\n')	# enter into log
	return (feature,offset,length)		# return the disk image, list of features, their offsets and lengths. This is redundant because of the global declaration of these variables


def redact(diskimage,beginOffset,featureLength): # redact the disk image by passing the image location, offset, and length of target data
	byte ="\x00"			# hex byte used to overwrite data
	endOffset = int(beginOffset) + int(featureLength)
	#print(diskimage)	# used for debug
	#print(beginOffset)	# used for debug
	#print(featureLength)	# used for debug
	#print(endOffset)	# used for debug
	#print(byte)		# used for debug

	try:
		file = open(diskimage, "r+b")	# open the image in read and binary write mode
		try:
			for num in range(int(beginOffset),int(endOffset)):
				file.seek(num,0)	# find the location of the offset from begining
				file.write(byte)	# overwrite the byte
			log.write('\n' + (strftime("%H:%M:%S %b %d, %Y -", localtime())) + ' Successfully redacted offset: ' + beginOffset + ' with \\x00 \n')
			print('Successfully redacted offset ' + beginOffset)
		except:
			log.write('\n' + (strftime("%H:%M:%S %b %d, %Y -", localtime())) + ' ERROR: REDACTING OFFSET: ' + beginOffset)
			print('ERROR redacting offset ' + beginOffset)
	except:
		print('There was a problem opening the file at ' + diskimage)
		log.write('\n' + (strftime("%H:%M:%S %b %d, %Y -", localtime())) + ' There was a problem opening the image file located: ' + diskimage)
	return		# return


def parseDFXML(ewfDiskImage):
	dfxml = subprocess.check_output(["ewfinfo", ewfDiskImage, "-f", "dfxml"])
	root = ET.fromstring(dfxml)

	if root.iter('sectors_per_chunk'):
		for sectors_per_chunk in root.iter('sectors_per_chunk'):
			flags['-b'] = sectors_per_chunk.text
			flags['-p'] = sectors_per_chunk.text

	if root.iter('media_size'):
		for media_size in root.iter('media_size'):
			flags['-B'] = (re.search('[^\(]\d+[^\s]', media_size.text)).group()	# parse the number between the parens

	if root.iter('compression_level'):
		for compression_level in root.iter('compression_level'):
			flags['-c'] = compression_level.text[:-12]

	if root.iter('case_number'):
		for case_number in root.iter('case_number'):
			flags['-C'] = case_number.text

	if root.iter('description'):
		for description in root.iter('description'):
			flags['-D'] = description.text

	if root.iter('examiner_name'):
		for examiner_name in root.iter('examiner_name'):
			flags['-e'] = examiner_name.text

	if root.iter('evidence_number'):
		for evidence_number in root.iter('evidence_number'):
			flags['-E'] = evidence_number.text

	if root.iter('file_format'):
		for file_format in root.iter('file_format'):
			flags['-f'] = file_format.text.replace(" ", "").lower()

	if root.iter('error_granularity'):
		for error_granularity in root.iter('error_granularity'):
			flags['-g'] = error_granularity.text

	if root.iter('media_type'):
		for media_type in root.iter('media_type'):
			flags['-m'] = media_type.text[:-5]

	if root.iter('is_physical'):
		for is_physical in root.iter('is_physical'):
			if is_physical.text == 'yes':
				flags['-M'] = 'physical'
			else:
				 flags['-M'] = 'logical'

	if root.iter('notes'):	# look for existing notes object
		for acquiry_information in root.iter('acquiry_information'):
			acquiry_information = ET.SubElement(acquiry_information,'notes') # if notes object doesn't exist, create the object under acquiry_information
	else:
		for acquiry_information in root.iter('acquiry_information'):
			acquiry_information = ET.SubElement(acquiry_information,'notes') # if notes object doesn't exist, create the object under acquiry_information

	if root.iter('notes'):	# look for existing notes
		for notes in root.iter('notes'):
			notes.text = 'here is a new note'
			flags['-N'] = notes.text

	if root.iter('bytes_per_sector'):
		for bytes_per_sector in root.iter('bytes_per_sector'):
			flags['-P'] = bytes_per_sector.text

	if root.iter('segment_file_size'):
		for segment_file_size in root.iter('segment_file_size'):
			flags['-S'] = segment_file_size.text
	else:
		flags['-S'] = '100 TiB'

	flags['-r'] = 2	# set the retry number to 2
	flags['-o'] = 0	# set the begining offset to zero
	flags['-t'] = args.output
	return


def exportEWF(rawDiskImage):
	ewfacquire = ['ewfacquire', rawDiskImage, '-u']	# initialize variable
	[ewfacquire.extend([str(key),str(value)]) for key,value in flags.items()]	# convert the flags key/value dictionary to a list
	subprocess.check_call(ewfacquire)	# call ewfacquire with the dfxml arguments
	return


""" MAIN STARTS HERE"""

parser = argparse.ArgumentParser(description='Redact binary features')	# store all the information necessary to parse the command line 
parser.add_argument('-i','--disk_image', help='This is the location of the disk image to be redacted', required=True)	# add image file location argument
parser.add_argument('-b','--bookmark_file', help='This is the bookmark file exported from Bulk_Extractor', required=True)	# add image file location argument
parser.add_argument('-f','--image_format', help='type of image file [EWF] [AFF] [RAW] [ISO]', required=True)	# add image file location argument
parser.add_argument('-o','--output', help='This is the output location and name (without extension) to save the redacted disk image', required=True)	# add image file location argument
args = parser.parse_args()	# parse the arguments and store in variable args
print('\nyou entered ' + args.disk_image + ' ' + args.bookmark_file + ' ' + args.image_format + ' ' + args.output)	# used for debug

try:
	log = open(saveFilePath + '/log.txt', 'w')	# open the log file
	#print('\nlog written to ' + saveFilePath + '/log.txt') # used for debug
	log.write('Script started running at ' + (strftime("%H:%M:%S on %a %b %d, %Y", localtime())) + '\n')    # write the first entry into the log
except:
	print('There was an error creating the log file')

if (args.image_format) == 'EWF':
	print('Converting EWF image to raw...')
	log.write('\n' + (strftime("%H:%M:%S %b %d, %Y - ", localtime())) + 'Converting image file from EWF to RAW...')		# update log file
	subprocess.check_call(['ewfexport', args.disk_image, '-t', args.output, '-f', 'raw', '-o', '0', '-S', '0', '-u'])	# convert the EWF disk image into RAW using ewfexport
	log.write('\n' + (strftime("%H:%M:%S %b %d, %Y - ", localtime())) + 'Successfully converted disk image file to RAW')	# update log file
	parseDFXML(args.disk_image)
	### save DFXML to temporary file, append notes section with date/time redaction script was run
"""
if args.image_format == 'AFF':
	print('Converting AFF image to raw...')
	### convert image to RAW
	### save DFXML to temporary file, append notes section with date/time redaction script was run


if args.image_format == 'ISO':
	print('Converting ISO image to raw...')
	### convert image to RAW
	### save DFXML to temporary file, append notes section with date/time redaction script was run
"""

bookmarks = parseBookmarks(saveFilePath + '/' + args.bookmark_file)	# parse the bookmark file, pass it the bookmarks file location

log.write('\nAttempting redaction on RAW disk image located at: ' + saveFilePath + '/' + args.output + '.raw\n')	# enter into log
for i in xrange(len(offset)):
	log.write('\n' + (strftime("%H:%M:%S %b %d, %Y - ", localtime())) + ' Attempting to redact offset: ' + str(bookmarks[1][i]) + ' for ' + str(bookmarks[2][i]) + ' bytes.')
	redact((saveFilePath + '/' + args.output + '.raw'),offset[i],length[i])	# call redact function, pass the image, offset, and length
	#print(bookmarks[0][i])	# used for debug
### IF original format was RAW, save the DFXML file in the same place as the redacted RAW file.

### document the redaction in the notes section of the DFXML

exportEWF(args.output + '.raw')

log.write('\nScript stopped running at ' + (strftime("%H:%M:%S on %a %b %d, %Y", localtime())))   # write out the last entry in the log
log.close()    # close the log file

