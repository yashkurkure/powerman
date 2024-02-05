#!/bin/bash
#
# Script to setup NAS Parallel Benchmark.

# Extract the files for the benchmark into NFS directory
tar -xvf /local/repository/benchmarks/NPB3.4.2.tar -C /pbsusers
mv /pbsusers/NPB3.4.2 /pbsusers/npb

# Load default configurations for MPI and OMP
