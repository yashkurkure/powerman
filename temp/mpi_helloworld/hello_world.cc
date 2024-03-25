#include <mpi.h>
#include <iostream>

using namespace std;

int main(int argc, char** argv) {


	int rank, size;
	

	/**
	MPI_Init() must be called before any other MPI functions can be called.
	It should be called once.
	On exit from this routine, all process will have a copy of the
	agument list.
	*/
	MPI_Init(&argc, &argv);


	/**
	# MPI Communicators

		Communicator is an internal MPI object. MPI programs are made up of
		communicating processes where each process has its own address space
		containing its own attributes such as rank, size, argv, argc, etc.

		MPI provides functions to interact with the communicator.

		Some more details:-
			The default communicator is MPI_COMM_WORLD. All processes are its members and
			its size is the number of processes in it. Each process possesses a rank within
			it. It is an ordered list of processes.

			More than one communicators can exist where each process can belong to more than
			one of them. In each communicator a process will have its own uniuque rank.
		
	*/



	/**
	MPI_Comm_rank(MPI_Comm comm, int *rank) determines the rank of the calling process in the communicator.

	- comm is the communicator group which is being querried for the rank of the current process.
	- Returns the rank of the calling process in the group underlying the comm.
	*/
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);



	/**
	MPI_Comm_size(MPI_Comm comm, int *size) determines the size of the group associated with a communicator.

	- This will determine the size of the group associated with a communicator comm.
	- Returns an integer number of processes in the group underlying comm executing the program.
	- Imp: comm is the communicator group whose size is being queried. The result is stored at *size.

	*/
	MPI_Comm_size(MPI_COMM_WORLD, &size);



	cout << "Hello world from process " << rank << " of " << size << "!" << endl;



	/**
	MPI_Finalize() cleans up and terminates the MPI execution enviornment.

	All MPI processes must call this before exiting.
	It need not be the last executable statement or even in main.
	Must be called at some point foloowing the last call to any other MPI function.
	*/
	MPI_Finalize();
	
	return 0;
}