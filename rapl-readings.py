# Python script to run rapl-read.c at intervals to gather power consumption
import subprocess
import time
import sys

outgraph = sys.argv[1]

def read_rapl():
    args = ("./rapl-read", "-m")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readlines()

    package1_energy = float(output[49].decode().strip().split(':')[1].split('J')[0].strip())
    package2_energy = float(output[53].decode().strip().split(':')[1].split('J')[0].strip())
    timestamp = time.time()
    return [timestamp, package1_energy, package2_energy]

x = []
y1 = []
y2 = []

try:
    while True:
        reading = read_rapl()
        x.append(reading[0])
        y1.append(reading[1])
        y2.append(reading[2])
except KeyboardInterrupt:
    print('Stoping rapl reads...')

import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(x, y1, color = 'green', marker = 'o', label='Package 1')
plt.plot(x, y2, color = 'red', marker = 'x', label='Package 2')
plt.ylabel('Energy(J)')
plt.xlabel('Unix Time(s)')
plt.legend(title = f'Energy(J) vs T')
plt.savefig(f'{outgraph}', dpi=300)