/*
	Yash Kurkure
	NetId - ykurku2
	CS494 - Introduction to HPC 
	Assignment 01
	03/06/2023
		
	I certify that this is my own work and where appropriate an extension of the starter code provided for the assignment.
*/
#include <stdio.h>
#include<string.h>
#include <omp.h>
#include <iostream>
#include<cstdlib>
#include<unistd.h> //sleep

// Contains the options set by the command line arguments.
struct options{
	// if true it appends to the file, false prints everything.
	bool silent_mode;

	// amount of work
	unsigned int work;
};

void work_task();
int omp_thread_count();
void parseArgs(int, char** , options&);
double run_scaling_study(unsigned int work);

// Main
int main(int argc, char* argv[]) {

	options op;
	parseArgs(argc, argv, op);

	// Report amount of work assigned.
	unsigned int work = op.work;;
	if (!op.silent_mode) std::cout << "Assigned work\t" << work << std::endl;

	// Report amount of threads being used.
	int thread_count = omp_thread_count();
	if (!op.silent_mode) std::cout << "Thread Count\t" << thread_count << std::endl;

	for(int i = 1; i <= 25; i++){
		double time = run_scaling_study(work);
		if(i == 25){
			if ( op.silent_mode) std::cout << time <<std::endl;
			continue;
		}
		if ( op.silent_mode) std::cout << time <<"\t";
		if (!op.silent_mode) std::cout << "Time Taken\t"<<time<<std::endl;
	}
	return 0;
}

/*
Run the scaling study.
Retuns the time in seconds required to run the experiment.
*/
double run_scaling_study(unsigned int work) {
	double start;
	double end;
	start = omp_get_wtime();
	#pragma omp parallel
	{
		#pragma omp for 
		for(unsigned int i = 0; i < work ; i++){
			work_task();
		}
	}
	end = omp_get_wtime();
	return end - start;
}


/*
Parse the command line arguments.
*/
void parseArgs(int argc, char* argv[], options& op){

	if(argc < 2){
		std::cout << "Usage: scaling_study [<number>] [<silent option: -s>]"<<std::endl;
		exit(0);
	}
	if(argc == 3){

		if(strcmp(argv[2], "-s") == 0){
			op.silent_mode = true;
		}
	}
	op.work = atoi(argv[1]);
}


/*
Simulates unit amount of work performed in 1 millisecond.
*/
void work_task() {
	// sleep 1 millisecond
	usleep(1000);
}

/*
Counts the number of openmp threads.
*/
int omp_thread_count() {
	int n = 0;
	#pragma omp parallel reduction(+:n)
	n += 1;
	return n;
}
