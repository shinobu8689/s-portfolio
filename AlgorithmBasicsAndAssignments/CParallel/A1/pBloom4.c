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
		Param:  key: the integer being hashed
		Return: key % moduloValue
	*/
	int moduloValue = 9973;
    return (key * key) % moduloValue;    
}

int midSquareHash(key){
	/*
		Perform Mid-Square Hashing, square the param key.
		If even, takes the middle 4 digit from it. 
		If odd, take middle 3 digit .
		Param:  key: the integer being hashed
		Return: square: the variable that hashed by calculating the middle one/two digit.
	*/
    int square = key * key;
    int digit = (int) floor(log10(square)) + 1 % 2;
    
	if (digit > 4) {
		if (digit % 2 == 0){
			square = square / pow(10, (digit / 2 - 2));    // remove right side digit
			square -= (square / 10000) * 10000;            // remove left side digit
		} else {
			square = square / pow(10, ((digit - 3) / 2));  // remove right side digit
			square -= (square / 1000) * 1000;              // remove left side digit
		}
	}
    return square;
}

int digitFoldHash(key){
	/*
		Perform Digit-Fold Hashing, make it the power of itself to be larger spread across the array,
		spilt the param value every 4 digit and add them together.
		Param:  key: the interger being hashed
		Return: sum: the hashed value after the calculation.
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
		Param:  *string: the string array to be turned in int
		return: total: sum of all char in string represented in int 
	*/
	int total = 0;
	for (int i = 0; i < strlen(string); i++){
		total += string[i];
	}
	return (int) total;
}

void set_bit_one(int *bitArray, int i) {
	/*
		Set the bitArray of location oi to be 1.
		Param:  
			int *bitArray
			int i: the index of the bitArray 
	*/
    bitArray[i / 8] |= 1 << (i % 8);	// 0 => 1
	/*
		memo of how this works:	let n = 35
		each slot in C is 8 byte
		To know that the slot of that index is in bitArray[i:35 / 8] = bitArray[4]
		To know the bit location of that slot: i:35 % 8 = 3
		the 3rd bit of bitArray[4]. 1 << (i % 8) create a mask of it: 00001000
		bit operation or |= to the current bitArray slot/
	*/
}
 
int get_bit(int *bitArray, int i) {
	/*
		get bit of that slot of the array
		Param:  
			int *bitArray
			int i: the index of the bitArray 
		Return: 0/1 of that bit
	*/
    return 1 & (bitArray[i / 8] >> (i % 8));	// current slot value & and the mask of indexed location
}


#define SIZE (10000)
#define ARRAY_SIZE(x) (x/8+(!!(x%8)))
#define NUM_OF_THREADS 8


void printBitArray(int *bitArray){
	// print givin bit array, below code for formating
	for (int i = 0; i <= (SIZE - 1); i++){
		if ((i) % 100 == 0) { printf("\n%d | ", i); }
		printf("%d", get_bit(bitArray, i));
		if ((i + 1) % 5 == 0) {printf(" ");}
	}
	printf("\n");
}

void WriteToFile(char *pFilename, int *pArray){
	// output the printed bitArray with the formating of printBitArray() as a file
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
	struct timespec start, end;
	double time_taken;
	omp_set_num_threads(NUM_OF_THREADS);

	fp = fopen(fileName,"r");
	if (fp == NULL) {
		printf("file does not exist!\n");
		return 1;
	}

	



	clock_gettime(CLOCK_MONOTONIC, &start); 

	fscanf(fp, "%d", &selectedCount);	// first row get amount of rows
	
	#pragma omp parallel private(i, word, wordInt) shared(bitArray, selectedCount) 
	{
		// local array for each thread
		int localBitArray[ARRAY_SIZE(SIZE + 1)] = { 0 };

		#pragma omp for schedule(static, 500)
		for (i = 0; i < selectedCount; i++){
			fscanf(fp, "%s", &word);		// get line of words
			strtok(word, "\n");				// get rid of new line
			strtok(word, "\r");				// get rid of return the line start
			wordInt = strToInt(word);
			//printf("Iteration %d is processed by %d/%d thread. (into global)\n", i, omp_get_thread_num(), omp_get_num_threads() - 1);
			// 	#pragma omp critical
			set_bit_one(localBitArray, divisionHash(wordInt));	// whatever it has to set to 1 anyway
			set_bit_one(localBitArray, midSquareHash(wordInt));
			set_bit_one(localBitArray, digitFoldHash(wordInt));
		}

		for (int j = 0; j < SIZE; j++){
			//printf("Iteration %d is processed by %d/%d thread. (into global)\n", j, omp_get_thread_num(), omp_get_num_threads() - 1);
			// take from local array to global array
			#pragma omp critical
			if (get_bit(localBitArray, j) == 1) {set_bit_one(bitArray, j);}
		}

	}
	
	// serial: 5.000
	// schedule(dynamic, 500)		schedule(dynamic, 50)		schedule(dynamic, 8)
	// with 2 threads: 14.8452		14.9282						16.3840
	// with 8 threads: 13.8985		13.4471						16.5760
	// schedule(static, 500)		schedule(static, 50)		schedule(static, 8)
	// with 2 threads: 14.9771		14.8501						18.1137
	// with 8 threads: 13.3561		13.7981						16.8955

	clock_gettime(CLOCK_MONOTONIC, &end);

	fclose(fp);

	printf("Arrayed for %d words from %s. \n", selectedCount, fileName);
	

	// calculate the time taken
	time_taken = (end.tv_sec - start.tv_sec) * 1e9; 
    time_taken = (time_taken + (end.tv_nsec - start.tv_nsec)) * 1e-9; 
	printf("Overall time: %lf\n", time_taken);


	printBitArray(bitArray);
	WriteToFile("bitArrayOMP.txt", bitArray);

	return 0;

}



