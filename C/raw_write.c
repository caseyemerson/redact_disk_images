///*
// * write.c
// *
// *  Created on: Dec 29, 2013
// *      Author: cemerson
// *      from: http://stackoverflow.com/questions/7749134/reading-and-writing-a-buffer-in-binary-file
// */
//
//#include <stdio.h>
//#include <string.h>
//#include <stdlib.h>
//
//int main( int argc, char ** argv ) {
//	FILE* pFile;
//	char* yourFilePath  = "test.file";
//	char* yourBuffer    = "Please delete casey@unc.edu from your database. He likes his privacy!";
//	int   yorBufferSize = strlen(yourBuffer) + 1;
//
//	/* Reserve memory for your readed buffer */
//	char* readedBuffer = malloc(yorBufferSize);
//
//	if (readedBuffer==0){
//	    puts("Can't reserve memory for Test!");
//	}
//
//	/* Write your buffer to disk. */
//	pFile = fopen(yourFilePath,"wb");
//
//	if (pFile){
//	    fwrite(yourBuffer, yorBufferSize, 1, pFile);
//	    puts("Wrote to file!");
//	}
//	else{
//	    puts("Something wrong writing to File.");
//	}
//
//	fclose(pFile);
//
//	/* Now, we read the file and get its information. */
//	pFile = fopen(yourFilePath,"rb");
//
//	if (pFile){
//	    fread(readedBuffer, yorBufferSize, 1, pFile);
//	    puts("Read from file!");
//	}
//	else{
//	    puts("Something wrong reading from File.\n");
//	}
//
//	/* Compare buffers. */
//	if (!memcmp(readedBuffer, yourBuffer, yorBufferSize)){
//	    puts("readBuffer = yourBuffer");
//	}
//	else{
//	    puts("Buffers are different!");
//	}
//
//	/* Free the reserved memory. */
//	free(readedBuffer);
//
//	fclose(pFile);
//	return 0;
//}
