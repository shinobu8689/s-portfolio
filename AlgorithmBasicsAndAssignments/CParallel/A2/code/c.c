#include <stdio.h>
 
// M x N matrix
#define M 10
#define N 2

void printQ(int q[M][N]){
	for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            printf("%d ", q[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

void appendQ(int time, int vacancy, int q[M][N]){
    for (int i = M-1; i > 0; i-- ) {
        q[i][0] = q[i - 1][0];
        q[i][1] = q[i - 1][1];
    }
    q[0][0] = time;
    q[0][1] = vacancy;
}

int main(){ // 0 in 4 out

    int q[M][N] = {0};
    printQ(q);

    appendQ(1, 2, q);
    printQ(q);

    appendQ(3, 4, q);
    printQ(q);
    
    return 0;
}