from jinja2 import Template
'''
This script generates job traces based on the following paper with a 
few modifications:

N. Kumbhare, A. Marathe, A. Akoglu, H. J. Siegel, G. Abdulla and S. Hariri, 
"A Value-Oriented Job Scheduling Approach for Power-Constrained and 
Oversubscribed HPC Systems," in IEEE Transactions on Parallel and Distributed 
Systems, vol. 31, no. 6, pp. 1419-1433, 1 June 2020, 
doi: 10.1109/TPDS.2020.2967373.

The script creates 15 unique workload traces. Each trace is composed of 60 jobs 
in the order of their arrival time. In all the traces, we use an inter-arrival 
duration of 200 seconds between consecutive job. 

It randomly select the range for possible node configurations for each job while
ensuring that its maximum node count does not exceed the system size. The paper
randomly chooses the range of OpenMP thread count in between 8 and 24.

For the walltime the paper estimates the job execution time on an intermediate 
node count (geometric mean of the maximum and minimum nodes requested by the 
job).(TODO: what does this mean??)

TODO: what walltime to use for each job? for now randomly select between 0.5, 1
and 1.5 hrs. Some jobs might fail to complete in the specified time due to this.

The job workloads are Multi-zone versions of NPB (NPB-MZ) that are designed to 
exploit multiple levels of parallelism in applications and to test the 
effectiveness of multi-level and hybrid parallelization paradigms and tools. 

There are three types of benchmark problems derived from single-zone 
pseudo applications of NPB:

* BT-MZ, Block Tri-diagonal solver
uneven-size zones within a problem class, increased number of zones as problem 
class grows

* SP-MZ, Scalar Penta-diagonal solver
even-size zones within a problem class, increased number of zones as 
problem class grows

* LU-MZ, Lower-Upper Gauss-Seidel solver
even-size zones within a problem class, a fixed number of zones for all 
problem classes

-----------------------------------------------------------------
Class   Number of Zones     Aggregate Grid    Memory Requirement
      BT-MZ&SP-MZ  LU-MZ      (Gx*Gy*Gz)          (approx.)
-----------------------------------------------------------------
 S       2 x 2     4 x 4      24 x 24 x 6             1 MB
 W       4 x 4     4 x 4      64 x 64 x 8             6 MB
 A       4 x 4     4 x 4     128 x 128 x 16          50 MB
 B       8 x 8     4 x 4     304 x 208 x 17         200 MB
 C      16 x 16    4 x 4     480 x 320 x 28         0.8 GB
 D      32 x 32    4 x 4    1632 x 1216 x 34       12.8 GB
 E      64 x 64    4 x 4    4224 x 3456 x 92        250 GB
 F     128 x 128   4 x 4   12032 x 8960 x 250       5.0 TB
-----------------------------------------------------------------

The paper uses a sampling range for the problem size between class C and class 
E with a memory footprint between 0.8 and 250 GB for the above problems. This
script does the same but between class S and class D.
'''



job_template = """
#!/bin/bash
#PBS -l nodes={{ nodes }}:ppn={{ ppn }}
#PBS -l walltime={{ walltime }}
#PBS -q {{ queue_name }}
#PBS -o {{ output_file }}
#PBS -e {{ error_file }}

cd $PBS_O_WORKDIR
export P4_RSHCOMMAND=/opt/pbs/bin/pbs_tmrsh
export OMP_NUM_THREADS={{ OMP_NUM_THREADS }}

mpirun {{executable path}}

"""

arrival_delta = 200
num_traces = 15
jobs_per_trace = 60
omp_thread_counts = [ i for i in range(8, 25) ]
node_counts = [i for i in range(1, 25) ]
walltimes = ['00:30:00', '01:00:00', '01:30:00']
problem_classes = ['S', 'W', 'A', 'B', 'C', 'D']
benchmark_path = '/pbsusers/NPB3.4.2/NPB3.4-MPI/bin/'
problems = ['bt-mz','lu-mz','sp-mz']