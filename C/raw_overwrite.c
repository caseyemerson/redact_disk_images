/*
 * overwrite.c
 *
 *  Created on: Jan 3, 2014
 *      Author: cemerson
 */

#include <stdio.h>

int overwrite(char *diskimage, int offset, int length){	// define the overwrite function
	int endoffset = offset + length;					// calculate the end offset of the feature

	char byte = '\x00';		// <---------------------------this is the hex byte that will be written (note: quotes matter!)

	FILE * file = fopen(diskimage, "r+b");				// open the disk image in read/write binary mode

	if (!file){											// if the file cannot be opened...
		printf("Cannot open the disk image %s!\n", diskimage);	// print error message and...
		return 1;										// exit with an error
	}

	fseek(file, offset, SEEK_SET);						// goto the offset in the file
	for(int i = offset; i < endoffset; i++){			// iterate through each byte in the file
		fwrite(&byte, sizeof(byte), 1, file);			// overwrite each byte in the feature
	}
	printf("Offset %d through offset %d in %s was overwritten", offset, endoffset, diskimage);	// print confirmation
	fclose(file);										// close the file
	return 0;											// return
}

// MAIN PROGRAM
int main( int argc, char ** argv ) {

	char * filePath  = "test.file";					// file location
	int offset = 14;									// feature offset
	int length = 5;										// length of feature

	overwrite(filePath, offset, length);				// call overwrite function, pass disk image location, feature offset, and length of feature
	return 0;											// return
}
