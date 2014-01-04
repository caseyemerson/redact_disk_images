
def redact(image,beginOffset,length): # pass it the image, offset, and length

	byte ="\x00"			# hex byte used to overwrite data
	endOffset = length + beginOffset

	file = open(image, "r+b")	# open the image in read and binary write mode	

	for num in range(beginOffset,endOffset,1):
		file.seek(num,0)	# find the location of the offset from begining
		file.write(byte)	# overwrite the byte
	file.close()			# close the file

	print''
	print'Successfully redacted offset ', beginOffset, ' through ', endOffset
	print'in ', image
	print''
	return				# return

import argparse

parser = argparse.ArgumentParser(description='Redact binary features')	# store all the information necessary to parse the command line input
parser.add_argument('-i','--input', help='disk image location', required=True)	# add image file location argument
parser.add_argument('-o','--offset', type=int, help='enter begining offset of the feature', required=True)	# add offset argument
parser.add_argument('-l','--length', type=int, help='length of the feature', required=True)		# add length argument

args = parser.parse_args()	# parse the arguments and store in variable args

#print(args.input)	# used for debug
#print(args.offset)	# used for debug
#print(args.length)	# used for debug

redact(args.input,args.offset,args.length)	# call redact function, pass the image, offset, and length
