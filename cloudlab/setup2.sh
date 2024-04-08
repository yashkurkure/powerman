#!/bin/bash

/local/repository/benchmarks/setup_stream_bench.sh
python3 /local/repository/benchmarks/jobtracegen.py -nt 1 -nj 5 -ad 10 -C /pbsusers -nr 2-4 -ppnr 1-4 -ompr 1-4