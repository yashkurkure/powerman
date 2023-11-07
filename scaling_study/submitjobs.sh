#!/bin/bash
# CPU(s):                             8
# Thread(s) per core:                 2
# Avaialable threads = 16 per node

qsub -v ENAME="study",ETHREADS=4,EWORK=100 runme.pbs
qsub -v ENAME="study",ETHREADS=4,EWORK=1000 runme.pbs
qsub -v ENAME="study",ETHREADS=4,EWORK=10000 runme.pbs
qsub -v ENAME="study",ETHREADS=4,EWORK=100000 runme.pbs