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

int divisionHash(key, moduloValue){
	/*
		Perform division Hashing, by simple geting the modulo with the param value.
		Param:
			key: the integer being hashed
			moduloValue: the moduloValue that being as part of hashing
		Return:
			key % moduloValue
	*/
    return (key * key) % moduloValue;    
}

int midSquareHash(key){
	/*
		Perform Mid-Square Hashing, square the param key.
		If even, takes the middle 4 digit from it. 
		If odd, take middle 3 digit .
		Param:
			key: the integer being hashed
		Return:
			square: the variable that hashed by calculating the middle one/two digit.
	*/
    int square = key * key;
    int digit = (int) floor(log10(square)) + 1 % 2;
    
	if (digit > 4) {
		if (digit % 2 == 0){
			square = square / pow(10, (digit / 2 - 2));
			square -= (square / 10000) * 10000;
		} else {
			square = square / pow(10, ((digit - 3) / 2));
			square -= (square / 1000) * 1000;
		}
	}
    return square;
}

int digitFoldHash(key){
	/*
		Perform Digit-Fold Hashing, make it the power of itself to be larger spread across the array,
		spilt the param value every 4 digit and add them together.
		Param:
			key: the interger being hashed
		Return:
			sum: the hashed value after the calculation.
	*/
    int sum = 0;
	key = key * key;
    while (key > 0) {
        sum += key - key / 10000 * 10000;
        key = key / 10000;
    }
    return sum;
}

int strToInt(char *string){
	/*
		Take the array that stores the string, treat it as integer and sum them up.
		Param:
			*string: the string array to be turned in int
		return:
			total: sum of all char in string represented in int 
	*/
	int total = 0;
	for (int i = 0; i < strlen(string); i++){
		total += string[i];
	}
	return (int) total;
}



#define SIZE (10000)
#define ARRAY_SIZE(x) (x/8+(!!(x%8)))

void toggle_bit(char *bitArray, int i) {
    bitArray[i / 8] ^= 1 << (i % 8);
}
 
char get_bit(char *bitArray, int i) {
    return 1 & (bitArray[i / 8] >> (i % 8));
}

// print bit array
void printBitArray(char *bitArray){
	for (int i = 0; i <= SIZE; i++){
		if ((i - 1) % 50 == 0) {
			printf("%d | ", i);
		}
		printf("%d ", get_bit(bitArray, i));
		if (i % 5 == 0) {printf("  ");}
		if (i % 50 == 0) {printf("\n");}
	}
}

int main(){
    char bitArray[ARRAY_SIZE(SIZE + 1)] = { 0 };
    int moduloValue = 9973;					// value to be use as modulo standard.
    
	FILE *fp;
	char word[50] = {};						// character of the same word will be grouped and processed
	char ch;								// temp character for checking
	int selectCount = 0;					// total amount of words in selected txt
	int approxCount = 0;					// count of how many it thinks its included
	int fullWordAmount = 0;					// full word list amount
	char fileName[] = "words_alpha.txt";	// selected word list
	int wordInt = 0;						// the int from str for processing
	struct timespec start, end, startComp, endComp;
	double time_taken;

	clock_gettime(CLOCK_MONOTONIC, &start); 

	fp = fopen(fileName,"r");
	if (fp == NULL) {
		printf("file does not exist!\n");
		return 1;
	}


	for (int i = 0; i < 370106; i++){	// 370106 words in "words_alpha.txt", 
		fgets(word, 50, fp);			// get line of words
		strtok(word,"\n");				// get rid of new line
		strtok(word,"\r");				// get rid of return the line start
		wordInt = strToInt(word); 
		if (!get_bit(bitArray, divisionHash(wordInt,moduloValue))) { toggle_bit(bitArray, divisionHash(wordInt,moduloValue)); }
		if (!get_bit(bitArray, midSquareHash(wordInt))) { toggle_bit(bitArray, midSquareHash(wordInt));	}
		if (!get_bit(bitArray, digitFoldHash(wordInt))) { toggle_bit(bitArray, digitFoldHash(wordInt));	}
		selectCount++;
	}

	fclose(fp);

	printf("Arrayed for %d words from %s. \n", selectCount, fileName);
	
	clock_gettime(CLOCK_MONOTONIC, &end);
	time_taken = (end.tv_sec - start.tv_sec) * 1e9; 
    time_taken = (time_taken + (end.tv_nsec - start.tv_nsec)) * 1e-9; 
	printf("Overall time: %lf\n", time_taken);

	printBitArray(bitArray);

	return 0;

    
}
