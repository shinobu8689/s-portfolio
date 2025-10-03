ALL: mpi

evsystem: mpi.c
	mpicc mpi.c  -o mpi

run:	// i represent the amount of nodes + base station, adapts to 64 processes but depends on the cores on the devices
	mpirun -np i mpi -fopenmp

clean :
	/bin/rm -f baseStnLog.txt *.o
	/bin/rm -f baseStnCommLog.txt *.o
	/bin/rm -f nodeXCommLog.txt *.o
	// X represent the node ranks, the number of files depends on the number of process
