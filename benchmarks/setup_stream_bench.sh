#!/bin/bash
#
# Script to setup NAS Parallel Benchmark Hybrid.

# Extract the files for the benchmark into NFS directory
tar -xvf /local/repository/benchmarks/NPB3.4.2-MZ.tar -C /pbsusers

# Build MPI + OMP Hybrid
cp /pbsusers/NPB3.4.2-MZ/NPB3.4-MZ-MPI/config/make.def.template /pbsusers/NPB3.4.2-MZ/NPB3.4-MZ-MPI/config/make.def

echo "sp-mz	S
lu-mz	S
bt-mz	S
sp-mz	W
lu-mz	W
bt-mz	W
sp-mz	A
lu-mz	A
bt-mz	A
sp-mz	B
lu-mz	B
bt-mz	B
sp-mz	C
lu-mz	C
bt-mz	C
sp-mz	D
lu-mz	D
bt-mz	D" > /pbsusers/NPB3.4.2-MZ/NPB3.4-MZ-MPI/config/suite.def

cd /pbsusers/NPB3.4.2-MZ/NPB3.4-MZ-MPI/ && make suite