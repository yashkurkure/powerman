# Python script to run rapl-read.c at intervals to gather power consumption
import subprocess
import time

def read_rapl():
    args = ("./rapl-read", "-m")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readlines()

    package1_energy = float(output[49].decode().strip().split(':')[1].split('J')[0].strip())
    package2_energy = float(output[53].decode().strip().split(':')[1].split('J')[0].strip())
    timestamp = time.time()
    return [timestamp, package1_energy, package2_energy]

print(f'Time\t\t\t\t\t\tPackage1\t\t\tPackage2')
while True:
    reading = read_rapl()
    print(f'{reading[0]}\t\t\t\t{reading[1]}\t\t\t{reading[2]}')