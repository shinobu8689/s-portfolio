#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

int main() {
    int row = 3, col = 2, rc = row * col;

    int* vacancyList = (int*) malloc(row*col*sizeof(int));
	for (int i = 0; i < rc; i++) vacancyList[i] = 5;

    vacancyList[2] = 2;

    for (int i = 0; i < rc; i++){
            printf("%d ",vacancyList[i] );
    }
}