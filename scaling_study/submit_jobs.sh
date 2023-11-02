#!/bin/bash

qsub -N work_100_4 -F "100 4 out" runme.pbs
qsub -N work_1000_4 -F "1000 4 out" runme.pbs
qsub -N work_10000_4 -F "10000 4 out" runme.pbs
qsub -N work_100000_4 -F "100000 4 out" runme.pbs
