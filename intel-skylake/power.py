# Python script to run rapl-read.c at intervals to gather power consumption
import subprocess
import time
import sys
import os
outgraph = sys.argv[1]
num_packages = int(sys.argv[2])

start_timestamp = time.time()

def read_rapl():

    t0 = timestamp = time.time()
    f = open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r")
    energy_counter1_0 = int(f.readline())
    f.close()

    # f = open("/sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj", "r")
    # energy_counter2_0 = int(f.readline())
    # f.close()

    time.sleep(1)

    t1 = timestamp = time.time()
    f = open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r")
    energy_counter1_1 = int(f.readline())
    f.close()

    #f = open("/sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj", "r")
    #energy_counter2_1 = int(f.readline())
    #f.close()

    power_counter1 = (energy_counter1_1 - energy_counter1_0)/1000000
    #power_counter2 = (energy_counter2_1 - energy_counter2_0)/1000000

    timestamp = time.time()
    return [int(t0 - start_timestamp), power_counter1]


x = []
y1 = []
# y2 = []

try:
    while True:
        reading = read_rapl()
        print(reading)
        x.append(reading[0])
        y1.append(reading[1])
        # y2.append(reading[2])
except KeyboardInterrupt:
    print('Stoping rapl reads...')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(x, y1, color = 'green', marker = 'o', label='Package 1')
# plt.plot(x, y2, color = 'red', marker = 'x', label='Package 2')
plt.ylabel('Power(J/s)')
plt.xlabel('Sample window start time (s)')
plt.legend(title = f'Power(J/s) vs Time')
plt.savefig(f'{outgraph}', dpi=300)
