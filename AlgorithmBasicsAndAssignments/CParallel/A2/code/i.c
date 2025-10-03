#include "mpi.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

// ?
// do{ pragma openMP for loop } while true; counter value of sleep awake do things


#define qM 10
#define qN 3

void appendQ(int time, int node, int vacancy, int q[qM][qN]){
    for (int i = qM-1; i > 0; i-- ) {
        q[i][0] = q[i - 1][0];
        q[i][1] = q[i - 1][1];
		q[i][2] = q[i - 1][2];
    }
    q[0][0] = time;
    q[0][1] = node;
	q[0][2] = vacancy;
}


int main(int argc, char *argv[]){
	int rank, size;
	int i;
	MPI_Status status;
	MPI_Request req;
	struct timespec timeStamp;

	MPI_Init(&argc, &argv);	// &argc: amount of process + base station
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	if(size < 2){
		printf("Please run with 2 processes.\n");
		fflush(stdout);
		MPI_Finalize();
		return 0;
	}
	
	srand(rank);

	// determine can it form a grid
	int row = 0, col = 0;
	if ((size - 1) % 5 == 0) {
		row = (size - 1) / 5;
		col = 5;
	} else if ((size - 1) % 3 == 0) {
		row = (size - 1) / 3;
		col = 3;
	} else if ((size - 1) % 2 == 0) {
		row = (size - 1) / 2;
		col = 2;
	} else {
		printf("Number of process not capable to form a grid.\n");
		fflush(stdout);
		MPI_Finalize();
		return 0;
	}

	// network map for search adj nodes
	int rc = row*col;
	int networkMap[row][col];
	int count = 1;
	for (int i = 0; i < row; i++){		
		for (int j = 0; j < col; j++){
			networkMap[i][j] = count;
			count++;
		}
	}



	if(rank == 0){	// base station
		
		int time = 0;
		
		int type = 0;		
		int sec = 0;
		int vacancy = 0, recvVacancy = 0;
		// -1: acknowledge
		// 0: updateReport
		// 1: adj request
		// 2: adj response 
		// 3: alert request
		// 4: alert response 
		// 5: terminate message

		int totalRevdAlerts = 0, totalRepliedAlert = 0, totalUpdate = 0, totalMsgSent = 0, recvTotalMsg = 0;
		int msgCommAdj = 0;

		int needExtraInfo = false;

		char buffer[16];	// pack into multi value into buffer
		int position = 0;

		int totalRuntime = 10;

		int q[qM][qN] = {0};	// keep at most totalRuntime record, of time, node, vacancy

		// need change for dynamic
		int vacancyList[64] = {0}; 
		int pendingResponse[64] = {0};


		int adjVacancyLst[4] = {0};
		int suggestNode = -1;

		int mapX = 0, mapY = 0;	// find location of self inside networkMap for adj nodes

		FILE *pFile = fopen("baseStnLog.txt", "w");
		FILE *commF = fopen("baseStnCommLog.txt", "w");

		printf("GRID:\n");
		fprintf(pFile, "GRID:\n");

		for (int i = 0; i < row; i++){		
			for (int j = 0; j < col; j++){
				printf("%d  ", networkMap[i][j]);
				fprintf(pFile, "%d  ", networkMap[i][j]);
			}
			fprintf(pFile, "\n");
			printf("\n");
		}

		fprintf(pFile, "\n");
		printf("\n");
		printf("T\tSRC\tSD/RV\tTYPE\t\tDEST\tINF\n======================================================================\n");
		fprintf(pFile, "T\tSRC\tSD/RV\tTYPE\t\tDEST\tINF\n======================================================================\n");

		fprintf(commF, "SYS_T\tSRC\tSD/RV\tTYPE\t\t\tDEST\tCPU_T\n======================================================================\n");

		#pragma omp parallel 
		do {
			time++;
			type = -1;

			
			if (time % 5 == 0) {
			// rece and unpack, get message type
				for (int i = 1; i < size; i++) {
					position = 0;
					MPI_Recv(&buffer, 16, MPI_PACKED, i, 0, MPI_COMM_WORLD, &status);
					MPI_Unpack(&buffer, 16, &position, &type, 1, MPI_INT, MPI_COMM_WORLD);
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					fprintf(commF, "%d\tBASE\tRV <-\tUPDATE\t\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					// received update report

					if (type == 0) {
						MPI_Unpack(&buffer, 16, &position, &sec, 1, MPI_INT, MPI_COMM_WORLD);
						MPI_Unpack(&buffer, 16, &position, &recvVacancy, 1, MPI_INT, MPI_COMM_WORLD);
						printf("%d\tBase\trecv\tUPDATE\t\tN%d\tvacancy: %d\n", sec, i, recvVacancy);
						fprintf(pFile, "%d\tBase\trecv\tUPDATE\t\tN%d\tvacancy: %d\n", sec, i, recvVacancy);
						appendQ(sec, i, recvVacancy, q);	// update local q
						totalUpdate++;
					}
				}
			}

			// receive alert report
			for (int i = 1; i < size; i++) {
				position = 0;
				MPI_Recv(&buffer, 16, MPI_PACKED, i, 0, MPI_COMM_WORLD, &status);
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				MPI_Unpack(&buffer, 16, &position, &type, 1, MPI_INT, MPI_COMM_WORLD);
				if (type == 3) {
					fprintf(commF, "%d\tBASE\tRV <-\tALERT\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					MPI_Unpack(&buffer, 16, &position, &msgCommAdj , 1, MPI_INT, MPI_COMM_WORLD);
					printf("%d\tBase\trecv\tALERT\t\tN%d\tmsg_exchanged: %d\n", time, i, msgCommAdj );
					fprintf(pFile, "%d\tBase\trecv\tALERT\t\tN%d\tmsg_exchanged: %d\n", time, i, msgCommAdj );
					totalRevdAlerts++;
					pendingResponse[i] = 1;
					needExtraInfo = true;
				}	
			}
			
			if (needExtraInfo) {type = 3;} else {type = -1;}
			// ask for vacancy of where node that without problem
			for (int i = 1; i <= rc; i++) {
				if (pendingResponse[i] == 0) {
					MPI_Send(&type, 1, MPI_INT, i, 0, MPI_COMM_WORLD); totalMsgSent++;
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					if (type == 3) { 
						fprintf(commF, "%d\tBASE\tSD ->\tALERT_ENQ\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
						printf("%d\tBase\tsend\tENQUIRY\t\tN%d\n", time, i); 
						fprintf(pFile, "%d\tBase\tsend\tENQUIRY\t\tN%d\n", time, i);
					}
					if (needExtraInfo) {
						MPI_Recv(&recvVacancy, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
						clock_gettime(CLOCK_MONOTONIC, &timeStamp);
						fprintf(commF, "%d\tBASE\tRV <-\tALERT_ENQ\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
						printf("%d\tBase\trecv\tEN_RESPONSE\tN%d\tvacancy: %d\n", time, i, recvVacancy);
						fprintf(pFile, "%d\tBase\trecv\tEN_RESPONSE\tN%d\tvacancy: %d\n", time, i, recvVacancy);
						vacancyList[i] = recvVacancy;
					}
				}
			}


			if (needExtraInfo){ // search nearest nodes
				
				for (int i = 0; i < row; i++) {
					for (int j = 0; j < col; j++) {
						if (networkMap[i][j] == rank) {
							mapX = i;
							mapY = j;
						}
					}
				}
				if (mapX > 0) {
					if ((mapY > 0) && (vacancyList[networkMap[mapX-1][mapX-1]] > 0)) 			suggestNode = networkMap[mapX-1][mapX-1];
					if ((mapY > (col - 1)) && (vacancyList[networkMap[mapX-1][mapX-1]] > 0)) 	suggestNode = networkMap[mapX-1][mapX+1];
				}
				if (mapX > (row - 1)) {
					if ((mapY > 0) && (vacancyList[networkMap[mapX+1][mapX-1]] > 0)) 			suggestNode = networkMap[mapX+1][mapX-1];
					if ((mapY > (col - 1)) && (vacancyList[networkMap[mapX+1][mapX+1]] > 0)) 	suggestNode = networkMap[mapX+1][mapX+1];
				}

				if (suggestNode < 1) {	// if no suitable node found within the corners node
					for (int i = 0; i < rc; i++) if (vacancyList[i] > 0) suggestNode = i;	// nodes are far enough so pick one
				} 
			}
			
			// answer full node query
			for (int i = 1; i <= rc; i++) {
				if (pendingResponse[i] == 1) {
					position = 0;
					MPI_Pack(&suggestNode, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
					MPI_Pack(&vacancyList[suggestNode], 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
					MPI_Send(buffer, position, MPI_PACKED, i, 0, MPI_COMM_WORLD); totalMsgSent++;
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					fprintf(commF, "%d\tBASE\tSD ->\tALERT_ANS\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					if (suggestNode > 1) {
						printf("%d\tBase\tsend\tAL_RESPONSE\tN%d\tsuggestNode: %d\tvacancy: %d\n", time, i, suggestNode, vacancyList[suggestNode]);
						fprintf(pFile, "%d\tBase\tsend\tAL_RESPONSE\tN%d\tsuggestNode: %d\tvacancy: %d\n", time, i, suggestNode, vacancyList[suggestNode]);
					} else {
						printf("%d\tBase\tsend\tAL_RESPONSE\tN%d\tNo suggestable nodes\n", time, i);
						fprintf(pFile, "%d\tBase\tsend\tAL_RESPONSE\tN%d\tNo suggestable nodes\n", time, i);
					}
					totalRepliedAlert++;
				}
			}


			// reset value for each sec
			for (int i = 0; i <= rc; i++) pendingResponse[i] = 0;
			needExtraInfo = false;
			suggestNode = -1;


			// send terminate message (if end)
			if (time == totalRuntime) { type = 5; } else { type = -1; }
			for (int i = 1; i < size; i++) {
				MPI_Send(&type, 1, MPI_INT, i, 0, MPI_COMM_WORLD); totalMsgSent++;
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				if (type == 5) { 
					fprintf(commF, "%d\tBASE\tSD ->\tTERMINATE\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					printf("%d\tBase\tsend\tTERMINATE\tN%d\n", time, i);
					fprintf(pFile, "%d\tBase\tsend\tTERMINATE\tN%d\n", time, i);
					MPI_Recv(&recvTotalMsg, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &status);
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					fprintf(commF, "%d\tBASE\tRV <-\tTOTAL_MSG\t\tN%d\t%lld.%.9ld\n", time, i, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					printf("%d\tBase\trecv\tTOTAL_MSG\tN%d\t%d\n", time, i, recvTotalMsg);
					fprintf(pFile, "%d\tBase\trecv\tTOTAL_MSG\tN%d\t%d\n", time, i, recvTotalMsg);
					totalMsgSent = totalMsgSent + recvTotalMsg;
				}
			}

			fflush(stdout);

		} while ( time < totalRuntime ); // unloop when self terminated
		
		printf("Base Terminates.\n\tTotalRunTime:%d\n\ttotalRevdAlerts:%d\n\ttotalRepliedAlert:%d\n\ttotalUpdate:%d\n\tignoredMessage:%d\n\ttotalMsgSent:%d\n", totalRuntime, totalRevdAlerts, totalRepliedAlert, totalUpdate, totalMsgSent - totalUpdate - totalRevdAlerts - totalRepliedAlert,totalMsgSent);
		fprintf(pFile, "Base Terminates.\n\tTotalRunTime:%d\n\ttotalRevdAlerts:%d\n\ttotalRepliedAlert:%d\n\ttotalUpdate:%d\n\tignoredMessage:%d\n\ttotalMsgSent:%d\n", totalRuntime, totalRevdAlerts, totalRepliedAlert, totalUpdate, totalMsgSent - totalUpdate - totalRevdAlerts - totalRepliedAlert,totalMsgSent);

		fclose(pFile);
		fclose(commF);









	} else {	// nodes

		int mapX = 0, mapY = 0;	// find location of self inside networkMap for adj nodes
		for (int i = 0; i < row; i++) {
			for (int j = 0; j < col; j++) {
				if (networkMap[i][j] == rank) {
					mapX = i;
					mapY = j;
				}
			}
		}

		int adjNodes[4] = {0};	// search and store adj nodes - [up, down, left, right]
		if (mapX > 0) 			adjNodes[0] = networkMap[mapX - 1][mapY];
		if (mapX < (row - 1)) 	adjNodes[1] = networkMap[mapX + 1][mapY];
		if (mapY > 0) 			adjNodes[2] = networkMap[mapX][mapY - 1];
		if (mapY < (col - 1)) 	adjNodes[3] = networkMap[mapX ][mapY+ 1];
		

		int time = 0;
		int type = 0, recvType = -1;		
		int vacancy = 5, sdVacancy = 0, recvVacancy = 0;
		// type, time, fromNode, vacancy
		// 0: updateReport
		// 1: adj request
		// 2: adj response 
		// 3: alert request
		// 4: alert response 
		// 5: terminate message
		// [] * fixed size array size

		int targetRank = 0;
		int haveAdjVacancy = false;
		int msgCommAdj = 0;
		int totalMsgSent = 0;

		char buffer[16];
		int position = 0;
		
		int waitList[4] = {0};	// [up, down, left, right]
		int q[qM][qN] = {0};	// keep at most totalRuntime record, of time, node, vacancy
		int recvNode = -1;

		char fileName[50];
		sprintf(fileName, "node%dCommLog.txt",rank);
		FILE *nodeLog = fopen(fileName, "w");

		fprintf(nodeLog, "Node: %d, ADJ_NODES: [", rank);
		for (int i = 0; i < 4; i++) fprintf(nodeLog, "%d ", adjNodes[i]);
		fprintf(nodeLog, "]\n");
		fprintf(nodeLog, "SYS_T\tSRC\tSD/RV\tTYPE\t\tDEST\tCPU_T\n======================================================================\n");
		
		#pragma omp parallel
		do {
			time++;

			vacancy = rand() % (5 + 1 - 0) + 0;
			if (vacancy > 5) vacancy = 5;
			if (vacancy < 0) vacancy = 0;

			// send port availability queue every 2 sec
			if (time % 5 == 0) {
				type = 0;	// update report -> base	
				appendQ(time, rank, vacancy, q);	// update local q

				position = 0;
				MPI_Pack(&type, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
				MPI_Pack(&time, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
				MPI_Pack(&vacancy, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
				MPI_Send(buffer, position, MPI_PACKED, 0, 0, MPI_COMM_WORLD); totalMsgSent++;
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				fprintf(nodeLog, "%d\tN%d\tSD ->\tUPDATE\t\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);

			}

			// if ((rank == 3 && time == 3) || (rank == 5 && time == 8)) {vacancy = 0;} else {vacancy = 5;}
			// if ( time == 8 && (rank == 3 || rank == 5 || rank == 6) ) {vacancy = 0;}


			type = -1;	// default send IGNORE, if full then ask adj
			if (vacancy == 0) {	
				printf("%d\tN%d\tvacancy: 0\n", time, rank);
				fprintf(nodeLog, "%d\tN%d\tvacancy: 0\n", time, rank);
				type = 1;
			}
		
			// send regular request to 4 adj directions 	1 if full, -1 if not full
			for (int i = 0; i < 4; i++) {
				targetRank = adjNodes[i];
				if (targetRank != 0) {
					MPI_Send(&type, 1, MPI_INT, targetRank, 0, MPI_COMM_WORLD); totalMsgSent++;
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					if (type == 1) fprintf(nodeLog, "%d\tN%d\tSD ->\tADJ_ENQ\t\tN%d\t%lld.%.9ld\n", time, rank, targetRank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					MPI_Recv(&recvType, 1, MPI_INT, targetRank, 0, MPI_COMM_WORLD, &status);
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					msgCommAdj = msgCommAdj + 2;
					if (recvType == 1) {
						waitList[i] = targetRank;	// mark who need response
						fprintf(nodeLog, "%d\tN%d\tRV <-\tADJ_ENQ\t\tN%d\t%lld.%.9ld\n", time, rank, targetRank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					}  
				}
			} 


			// send vacancy of self to who asked
			for (int i = 0; i < 4; i++) {
				if (waitList[i] > 0) {	// send response to who need it following the list
					position = 0;
					type = 2;
					sdVacancy = vacancy;
					MPI_Pack(&type, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
					MPI_Pack(&sdVacancy, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
					MPI_Send(buffer, position, MPI_PACKED, waitList[i], 0, MPI_COMM_WORLD); totalMsgSent++;
					clock_gettime(CLOCK_MONOTONIC, &timeStamp);
					fprintf(nodeLog, "%d\tN%d\tSD ->\tADJ_ANS\t\tN%d\t%lld.%.9ld\n", time, rank, waitList[i], (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
				}
			}

			type = -1;
			// receive from all adj nodes if it is the node who send req
			if (vacancy == 0) { 
				for (int i = 0; i < 4; i++) {
					position = 0;
					targetRank = adjNodes[i];
					if (adjNodes[i] > 0) {
						MPI_Recv(&buffer, 16, MPI_PACKED, targetRank, 0, MPI_COMM_WORLD, &status);
						clock_gettime(CLOCK_MONOTONIC, &timeStamp);
						fprintf(nodeLog, "%d\tN%d\tRV <-\tADJ_ANS\t\tN%d\t%lld.%.9ld\n", time, rank, targetRank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
						MPI_Unpack(&buffer, 16, &position, &recvType, 1, MPI_INT, MPI_COMM_WORLD);
						MPI_Unpack(&buffer, 16, &position, &recvVacancy, 1, MPI_INT, MPI_COMM_WORLD);
						printf("%d\tN%d\trecv\tN%d\tvacancy: %d\n", time, rank, targetRank, recvVacancy);
						if (recvVacancy > 0) {	haveAdjVacancy = true;	}
						msgCommAdj = msgCommAdj + 2;
					}
				}
				if (!haveAdjVacancy) {	// if adj node is full set type alert
					fprintf(nodeLog, "%d\tN%d\thave no ADJ vacancy node\n", time, rank);
					type = 3;
				}
		
			}


			
			//regular slot inform ALERT , -1 ignore , 3 alert
			position = 0;
			MPI_Pack(&type, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
			MPI_Pack(&msgCommAdj, 1, MPI_INT, buffer, 16, &position, MPI_COMM_WORLD);
			MPI_Send(buffer, position, MPI_PACKED, 0, 0, MPI_COMM_WORLD); totalMsgSent++;
			clock_gettime(CLOCK_MONOTONIC, &timeStamp);
			

			if (type == 3) {	// node w/ vacancy 0 wait for response
				fprintf(nodeLog, "%d\tN%d\tSD ->\tALERT\t\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
				position = 0;
				MPI_Recv(&buffer, 16, MPI_PACKED, 0, 0, MPI_COMM_WORLD, &status);
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				fprintf(nodeLog, "%d\tN%d\tRV <-\tAL_ENQ\t\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
				MPI_Unpack(&buffer, 16, &position, &recvNode, 1, MPI_INT, MPI_COMM_WORLD);
				MPI_Unpack(&buffer, 16, &position, &recvVacancy, 1, MPI_INT, MPI_COMM_WORLD);
				//printf("N%d revd w/ n%dv%d\n", rank, recvNode, recvVacancy);
			} else {			// node w/o issue send enquires if asked
				MPI_Recv(&recvType, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				
				if (recvType == 3) {
					fprintf(nodeLog, "%d\tN%d\tRV <-\tAL_ANS\t\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					MPI_Send(&vacancy, 1, MPI_INT, 0, 0, MPI_COMM_WORLD); totalMsgSent++;
					fprintf(nodeLog, "%d\tN%d\tSD ->\tAL_ANS\t\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
					}
			}


			// reset value for each sec
			memset(waitList, 0, sizeof waitList);
			msgCommAdj = 0; msgCommAdj;
			haveAdjVacancy = false;
			recvNode = -1;

			// recv terminate message
			MPI_Recv(&type, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
			clock_gettime(CLOCK_MONOTONIC, &timeStamp);
			
			if (type == 5) {
				fprintf(nodeLog, "%d\tN%d\tRV <-\tTERMINATE\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);
				totalMsgSent++;
				MPI_Send(&totalMsgSent, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
				clock_gettime(CLOCK_MONOTONIC, &timeStamp);
				fprintf(nodeLog, "%d\tN%d\tSD ->\tTOTAL_MSG\tBASE\t%lld.%.9ld\n", time, rank, (long long)timeStamp.tv_sec, timeStamp.tv_nsec);

				printf("N%d Terminates.\n", rank);
				break;
			}

		} while ( true ); // unloop when self terminated

		fclose(nodeLog);
	}

	

	MPI_Finalize();
	return 0;
}
