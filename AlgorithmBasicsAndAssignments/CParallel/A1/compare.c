#include <omp.h>
#include <stdbool.h>
#include <math.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <time.h>
#include <string.h>

// word dataset from: https://github.com/dwyl/english-words


void set_bit_one(int *bitArray, int i) {
    bitArray[i / 8] |= 1 << (i % 8);  // 0 => 1 only
}
 
int get_bit(int *bitArray, int i) {
    return 1 & (bitArray[i / 8] >> (i % 8));
}


int main(){
  
	char wordS[128] = {};						// word that get from a line
    char wordP[128] = {};						// word that get from a line
	struct timespec start, end;
	double time_taken;

	FILE *fpS = fopen("bitArraySerial.txt","r");
	if (fpS == NULL) {
		printf("fpS does not exist!\n");
		return 1;
	}

    FILE *fpP = fopen("bitArrayOMP.txt","r");
	if (fpP == NULL) {
		printf("fpP does not exist!\n");
		return 1;
	}

	for (int i = 0; i < 100; i++){
		fgets(wordS, 128, fpS);		// get line of words
        fgets(wordP, 128, fpP);		// get line of words
		if (strcmp(wordS, wordP) != 0) {
			printf("row %d is different\n", i);
			printf("S - %s\n", wordS);
			printf("P - %s\n", wordP);
			return 0;
		}
	}


	fclose(fpS);
    fclose(fpP);

	printf("both are the same\n");
	

	return 0;

}



