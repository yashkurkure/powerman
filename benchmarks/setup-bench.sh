#!/bin/bash
#
# Script to setup NAS Parallel Benchmark.

# Extract the files for the benchmark into NFS directory
tar -xvf /local/repository/benchmarks/NPB3.4.2.tar -C /pbsusers

# Extracted to: /pbsusers/NPB3.4.2

# Build MPI benchmarks
cp /pbsusers/NPB3.4.2/NPB3.4-MPI/config/make.def.template /pbsusers/NPB3.4.2/NPB3.4-MPI/config/make.def

echo "ft	S
mg	S
sp	S
lu	S
bt	S
is	S
ep	S
cg	S
dt	S
ft	W
mg	W
sp	W
lu	W
bt	W
is	W
ep	W
cg	W
dt	W
ft	A
mg	A
sp	A
lu	A
bt	A
is	A
ep	A
cg	A
dt	A" > /pbsusers/NPB3.4.2/NPB3.4-MPI/config/suite.def

cd /pbsusers/NPB3.4.2/NPB3.4-MPI/ && make suite

# Build OpenMP benchmarks
cp /pbsusers/NPB3.4.2/NPB3.4-OMP/config/make.def.template /pbsusers/NPB3.4.2/NPB3.4-OMP/config/make.def

echo "ft	S
mg	S
sp	S
lu	S
bt	S
is	S
ep	S
cg	S
ua	S
ft	W
mg	W
sp	W
lu	W
bt	W
is	W
ep	W
cg	W
ua	W
ft	A
mg	A
sp	A
lu	A
bt	A
is	A
ep	A
cg	A
ua	A" > /pbsusers/NPB3.4.2/NPB3.4-OMP/config/suite.def

cd /pbsusers/NPB3.4.2/NPB3.4-OMP/ && make suite