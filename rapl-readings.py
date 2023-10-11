# Python script to run rapl-read.c at intervals to gather power consumption
import subprocess


def read_rapl():
    
    
    args = ("./rapl-read", "-m")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readlines()

    package1_energy = float(output[49].decode().strip().split(':')[1].split('J')[0].strip())
    package2_energy = float(output[53].decode().strip().split(':')[1].split('J')[0].strip())

    return output

readings = read_rapl()
