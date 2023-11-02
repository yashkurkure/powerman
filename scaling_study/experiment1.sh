#!/bin/bash

# Using more threads than available cores
qsub -N work_100_6 -F "100 6 experiment1" runme.pbs
qsub -N work_1000_6 -F "1000 6 experiment1" runme.pbs
qsub -N work_10000_6 -F "10000 6 experiment1" runme.pbs
qsub -N work_100000_6 -F "100000 6 experiment1" runme.pbs