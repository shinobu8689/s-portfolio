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

int divisionHash(key){
	/*
		Perform division Hashing, by simple geting the modulo with the param value.
		Param:
			key: the integer being hashed
		Return:
			key % moduloValue
	*/
	int moduloValue = 9973;
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

void set_bit_one(int *bitArray, int i) {
    bitArray[i / 8] |= 1 << (i % 8);  // 0 => 1 only
}
 
int get_bit(int *bitArray, int i) {
    return 1 & (bitArray[i / 8] >> (i % 8));
}

// print bit array
void printBitArray(int *bitArray){
	for (int i = 0; i <= (SIZE - 1); i++){
		if ((i) % 100 == 0) { printf("\n%d\t | ", i); }
		printf("%d", get_bit(bitArray, i));
		if ((i + 1) % 5 == 0) {printf(" ");}
	}
	printf("\n");
}

void WriteToFile(char *pFilename, int *pArray){

	FILE *pFile = fopen(pFilename, "w");

	for (int i = 0; i <= (SIZE - 1); i++){
		if ((i) % 100 == 0) { fprintf(pFile, "\n%d | ", i); }
		fprintf(pFile, "%d", get_bit(pArray, i));
		if ((i + 1) % 5 == 0) {fprintf(pFile, " ");}
	}
	fprintf(pFile, "\n");
	fclose(pFile);
}

int main(){

    int bitArray[ARRAY_SIZE(SIZE + 1)] = { 0 };    
	FILE *fp;
	char word[50] = {};						// word that get from a line
	int selectedCount;						// total amount of words in selected txt
	char fileName[] = "words.txt";			// selected word list
	int wordInt = 0;						// the int created from str for processing
	int i;
	struct timespec start, end, startFor, endFor;
	double time_taken;

	clock_gettime(CLOCK_MONOTONIC, &start); 

	fp = fopen(fileName,"r");
	if (fp == NULL) {
		printf("file does not exist!\n");
		return 1;
	}

	clock_gettime(CLOCK_MONOTONIC, &startFor); 

	fscanf(fp, "%d", &selectedCount);	// first row get amount of rows
	
	for (i = 0; i < selectedCount; i++){
		fscanf(fp, "%s", &word);		// get line of words
		strtok(word, "\n");				// get rid of new line
		strtok(word, "\r");				// get rid of return the line start
		wordInt = strToInt(word);
		set_bit_one(bitArray, divisionHash(wordInt));	// whatever it has to set to 1 anyway
		set_bit_one(bitArray, midSquareHash(wordInt));
		set_bit_one(bitArray, digitFoldHash(wordInt));
	}

	clock_gettime(CLOCK_MONOTONIC, &endFor);

	fclose(fp);

	printf("Arrayed for %d words from %s. \n", selectedCount, fileName);
	
	clock_gettime(CLOCK_MONOTONIC, &end);

	// calculate the time taken
	time_taken = (end.tv_sec - start.tv_sec) * 1e9; 
    time_taken = (time_taken + (end.tv_nsec - start.tv_nsec)) * 1e-9; 
	printf("Overall time: %lf\n", time_taken);

	time_taken = (endFor.tv_sec - startFor.tv_sec) * 1e9; 
    time_taken = (time_taken + (endFor.tv_nsec - startFor.tv_nsec)) * 1e-9; 
	printf("For loop time: %lf\n", time_taken);
	 

	int chkArray;
	printf("\nInput 1 for BitArray: ");
	scanf("%d", &chkArray);
	if (chkArray == 1) { 
		printBitArray(bitArray);
		WriteToFile("bitArraySerial.txt", bitArray);
	}

	return 0;

}



