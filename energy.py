# Python script to run rapl-read.c at intervals to gather power consumption
import subprocess
import time
import sys
import os
outgraph = sys.argv[1]

start_timestamp = time.time()

def read_rapl():
    f = open("/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj", "r")
    energy_counter1 = int(f.readline())
    f.close()
    f = open("/sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj", "r")
    energy_counter2 = int(f.readline())
    f.close()
    timestamp = time.time()
    return [int(timestamp - start_timestamp), energy_counter1/1000000, energy_counter2/1000000]


x = []
y1 = []
y2 = []

try:
    while True:
        reading = read_rapl()
        time.sleep(1)
        print(reading)
        x.append(reading[0])
        y1.append(reading[1])
        y2.append(reading[2])
except KeyboardInterrupt:
    print('Stoping rapl reads...')

import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(x, y1, color = 'green', marker = 'o', label='Package 1')
plt.ylabel('Energy Consumed(J)')
plt.xlabel('Time(s)')
plt.legend(title = f'Energy(J) vs T')
plt.savefig(f'{outgraph}_package0', dpi=300)


fig = plt.figure()
plt.plot(x, y2, color = 'red', marker = 'x', label='Package 2')
plt.ylabel('Energy Consumed(J)')
plt.xlabel('Time(s)')
plt.legend(title = f'Energy(J) vs T')
plt.savefig(f'{outgraph}_package1', dpi=300)