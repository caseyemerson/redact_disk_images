# ******************************************************************************
# This code was written by Casey Emerson on 1/9/14 for his Masters Paper at the 
# University of North Carolina School of Information and Library Science.
#
# This script reads a configuration file that contains a disk image and a one or
# more offsets of features to be redacted. It determines the format of the image
# file and if necessary, converts the image file to RAW for redaction. It then
# overwrites the offsets and, if necessary, converts the image back into the
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


"""VARIABLES DEFINED HERE"""

offset = []	# global initialization of this empty list variable
length = []	# global initialization of this empty list variable
feature = []	# global initialization of this empty list variable
saveFilePath =  os.getcwd()	# get the current working directory


""" FUNCTIONS GO HERE"""

def parseConfig(configFile):
	log.write('\n' + (strftime("%H:%M:%S %b %d, %Y - processing config file located: ", localtime())) + (configFile) + '\n')	# enter into log
	with open(configFile, "r") as file:		# open the config file in read mode
    		for line in file:			# parse each line of the file
			if 'diskimage:' in line:	# look for the string 'diskimage loacation:', if found do...
				image = line.lstrip('diskimage: ').rstrip()	# strip out the string 'diskimage:'
				log.write('\nThe disk image is located at: ' + image + '\n')	# enter into log
			if re.match(r'[0-9]+,', line):	# look for the offset (a sequence of numbers followed by a comma)
				try:
					line = line.split(', ')	# split the line into pieces using ', ' delimeter
					offset.append(line[0])	# append the first part of the line into the offset list
					feature.append((line[3]).rstrip())		# append the third part of the line into the feature list
					length.append(len((line[3]).rstrip()))		# calculate the length of the feature and append it into the length list				
				except: 
					print('Doh! something went wrong matching the offset')	# if there was a problem, display an error
	
	return (image,feature,offset,length)		# return the disk image, list of features, their offsets and lengths. This is redundant because of the global declaration of these variables


def redact(diskimage,beginOffset,featureLength): # pass it the image, offset, and length

	byte ="\x00"			# hex byte used to overwrite data
	endOffset = int(featureLength) + int(beginOffset)
	print(diskimage)	# used for debug
	print(beginOffset)	# used for debug
	print(featureLength)	# used for debug
	print(endOffset)	# used for debug
	print(byte)		# used for debug
	
	try:	
		for num in range(beginOffset,endOffset,1):
			file.seek(num,0)	# find the location of the offset from begining
			file.write(byte)	# overwrite the byte
		log.write('\n' + (strftime("%H:%M:%S on %a %b %d, %Y,", localtime())) + ' Successfully redacted offset: ' + beginOffset + ' in disk image: ' + diskimage + '\n')
	except:
		log.write('\n' + (strftime("%H:%M:%S on %a %b %d, %Y,", localtime())) + ' ERROR: THERE WAS A PROBLEM REDACTING OFFSET: ' + beginOffset + ' in disk image: ' + diskimage)
	return		# return



""" MAIN STARTS HERE"""

parser = argparse.ArgumentParser(description='Redact binary features')	# store all the information necessary to parse the command line input
parser.add_argument('-i','--input', help='config file location', required=True)	# add image file location argument
args = parser.parse_args()	# parse the arguments and store in variable args
#print('\nyou entered ' + args.input)	# used for debug

try:
	log = open(saveFilePath + '/log.txt', 'w')	# open the log file
	log.write('Script started running at ' + (strftime("%H:%M:%S on %a %b %d, %Y", localtime())))    # write the first entry into the log
except:
	print('There was an error creating the log file')


config = parseConfig(args.input)	# parse the config file, pass it the config file location

try:
	file = open(config[0], "r+b")	# open the image in read and binary write mode
except:
	print('There was a problem opening the file at ' + image)
	log.write('\n' + (strftime("%H:%M:%S on %a %b %d, %Y,", localtime())) + ' There was a problem opening the image file located: ' + image)

for i in xrange(len(offset)):
	log.write('\n' + (strftime("%H:%M:%S on %a %b %d, %Y,", localtime())) + ' Attempting to redact offset: ' + str(config[2][i]) + ', for ' + str(config[3][i]) + ' bytes.')
	redact(config[0],offset[i],length[i])	# call redact function, pass the image, offset, and length
	#print(config[1][i])

log.write('\nScript stopped running at ' + (strftime("%H:%M:%S on %a %b %d, %Y", localtime())))   # write out the last entry in the log
log.close()    # close the log file
