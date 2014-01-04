///*
// * overwrite.c
// *
// *  Created on: Jan 3, 2014
// *      Author: cemerson
// */
//
//#include <stdio.h>
//#include <string.h>
//#include <stdlib.h>
//
//
//int overwrite(char diskimage, int offset, int length){
//	printf("diskimage = %c\n", diskimage);
//	int endoffset = offset + length;
//	char byte = '\x00';
//	FILE * file = fopen(&diskimage, "r+b");
//
//	if (!file){
//		printf("Cannot open file %c\n", diskimage);
//		return 1;
//	}
//	else{
//		for(int i = offset; i < endoffset; i++){
//			fwrite(&byte, sizeof(byte), 1, file);
//			printf("overwrote offset %d\n", i);
//		}
//		printf("Overwrote from offset %d to %d in %c\n", offset, endoffset, diskimage);
//	}
//
//	fclose(file);
//	return 0;
//}
//
//// MAIN PROGRAM
//int main( int argc, char ** argv ) {
//
//	char* filePath  = "test.file";
//	int featureoffset = 14;
//	int featurelength = 5;
//
//	overwrite(filePath, featureoffset, featurelength);
//	return 0;
//}
