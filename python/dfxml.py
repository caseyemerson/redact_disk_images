
"""IMPORTS GO HERE"""
import os
import subprocess
import xml.etree.ElementTree as ET
import string
import re


"""VARIABLES DEFINED HERE"""
flags = {}	# define dictionary (key value pair)

""" FUNCTIONS GO HERE"""

def 
dfxml = subprocess.check_output(["ewfinfo", "terry-work-usb-2009-12-11.E01", "-f", "dfxml"])
root = ET.fromstring(dfxml)

""" BUILD THE EWFACQUIRE SUB.PROCESS """

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
		#flags['-N'] = notes.text

#insert data into notes section
"""
insert into notes:
acquisition_date
acquisition_version
system_date
set_identifier
hashdigest + type attrib + coding attrib
"""

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
flags['-t'] = 'terry' # update this one

""" MAIN STARTS HERE"""

ewfacquire = ['ewfacquire', 'terry.raw', '-u', '-N', 'this is a note']	# initialize variable
[ewfacquire.extend([str(key),str(value)]) for key,value in flags.items()]	# convert the flags key/value dictionary to a list
subprocess.check_call(ewfacquire)	# call ewfacquire with the dfxml arguments 

ET.dump(root)

"""
-b sectors per chunk
-B Media size - requires some parsing?
-c compression method
-D description
-e examiner
-E evidence number
-f File format
-g Error granularity
-m Media type
-M Is physical
-N Notes
-o Offset (0)
-p sectors_per_chunk
-P Bytes per sector
-S Segment file size ?
-t [output file] no extension

media characteristics? (logical)
compression method? (deflate)
number of retries (2)

insert into notes:
acquisition_date
acquisition_version
system_date
set_identifier
hashdigest + type attrib + coding attrib
"""
