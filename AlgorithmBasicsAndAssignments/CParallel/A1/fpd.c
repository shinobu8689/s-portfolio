#include <omp.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <ctype.h>


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
	return total;
}

// for testing manual string input to test
void search(int bitArray[], int V){
    char input[50] = {};
    while (input >= 0) {
		printf("\nSearch - Enter a word: ");
        scanf("%s", &input);
        printf("(%d)  divisionHash w/%d: %d, midSquareHash: %d, digitFoldHash: %d\n",strToInt(input), V, divisionHash(strToInt(input),V), midSquareHash(strToInt(input)), digitFoldHash(strToInt(input)));
		printf("bitArray: %d %d %d\n", bitArray[divisionHash(strToInt(input),V)], bitArray[midSquareHash(strToInt(input))], bitArray[digitFoldHash(strToInt(input))]);
        if (bitArray[divisionHash(strToInt(input), V)] > 0 && bitArray[midSquareHash(strToInt(input))] > 0 && bitArray[digitFoldHash(strToInt(input))] > 0){
            printf("Yes! %s \n", input);
        } else {
            printf("No... %s\n", input);
        }
        printf("//////////////\n");
    }
}

// print bit array
void printBitArray(int *bitArray){
	for (int i = 1; i <= 10000; i++){
		if ((i - 1) % 20 == 0) {printf("%d | ", i);}
		printf("%d ",bitArray[i - 1]);
		if (i % 5 == 0) {printf("  ");}
		if (i % 20 == 0) {printf("\n");}
	}
}

int main(){
    int bitArray[10000] = {0};
    int moduloValue = 9973;					// value to be use as modulo standard.
    
	FILE *fp;
	char word[50] = {};						// character of the same word will be grouped and processed
	char ch;								// temp character for checking
	int selectCount = 0;					// total amount of words in selected txt
	int approxCount = 0;					// count of how many it thinks its included
	int fullWordAmount = 0;					// full word list amount
	char fileName[] = "words_alpha.txt";	// selected word list

	fp = fopen(fileName,"r");
	if (fp == NULL) {
		printf("file does not exist!\n");
		return 1;
	}

	do {
		ch = fgetc(fp);
		if (isalpha(ch) || ch == '-' || ch == '\''){	// its valid if its an alphabet/ - or ' , concatnate it as the same word
			strncat(word, &ch, 1);
		} else if (ch == '\n' || ch == EOF){			// if its \n or EOF, perform hashing to bitArray.
			bitArray[divisionHash(strToInt(word),moduloValue)]++;
        	bitArray[midSquareHash(strToInt(word))]++;
        	bitArray[digitFoldHash(strToInt(word))]++;
			selectCount++;
			memset(word, NULL, sizeof word);			// reset content of word for next
		}
    } while (ch != EOF);	// perform above action until end of file

	fclose(fp);

	// printBitArray(bitArray);

	printf("Arrayed for %d words from %s. \n", selectCount, fileName);
	

	return 0;


	fp = fopen("words_alpha.txt","r");
	if (fp == NULL) {
		printf("file does not exist!\n");
		return 1;
	}

	printf("\nchecking filtered percentage...\n");
	do {
		ch = fgetc(fp);
		if (isalpha(ch) || ch == '-' || ch == '\''){
			strncat(word, &ch, 1);
		} else if (ch == '\n' || ch == EOF){
			if (bitArray[divisionHash(strToInt(word), moduloValue)] > 0 && bitArray[midSquareHash(strToInt(word))] > 0 && bitArray[digitFoldHash(strToInt(word))] > 0){
        		approxCount++;
    		}
			fullWordAmount++;
			memset(word, NULL, sizeof word);
		}
    } while (ch != EOF);

	printf("found %d possibly results within %d entries. (%.2f%%)\n", approxCount, fullWordAmount, (approxCount/(double)fullWordAmount) * 100);
	printf("%d really exists within %d. (%.2f%% is correct.)\n", selectCount, approxCount, ((selectCount/(double)approxCount) * 100));

	fclose(fp);

	return 0;
    
}

/*

performance of this code (not so accurate)

Arrayed for 22 words from words_a.txt. 

checking filtered percentage...
found 9577 possibly results within 370106 entries. (2.59%)
22 really exists within 9577. (0.23% is correct.)

////////////

Arrayed for 98 words from words_a.txt. 

checking filtered percentage...
found 47657 possibly results within 370106 entries. (12.88%)
98 really exists within 47657. (0.21% is correct.)

////////////

Arrayed for 170 words from words_a.txt. 

checking filtered percentage...
found 86529 possibly results within 370106 entries. (23.38%)
170 really exists within 86529. (0.20% is correct.)

*/
