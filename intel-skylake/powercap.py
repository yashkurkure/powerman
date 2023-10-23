import time
import sys
import os
import subprocess

if os.geteuid() == 0:
    print("We're root!")
else:
    print("We're not root.")
    subprocess.call(['sudo', 'python3', *sys.argv])
    sys.exit()


# sudo stress --cpu 8 --timeout 20
f = open("/sys/class/powercap/intel-rapl/intel-rapl:0/constraint_0_power_limit_uw", "w+")
print('Setting power cap to 25W')
f.write('25000000')
f.close()

time.sleep(10)

f = open("/sys/class/powercap/intel-rapl/intel-rapl:0/constraint_0_power_limit_uw", "w+")
print('Setting power cap back to 45W')
f.write('45000000')
f.close()
