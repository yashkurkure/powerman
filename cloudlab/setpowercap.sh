#!/bin/bash
# NOTE: Must be executed as root
# Usage Example: setpowercap.sh 0.25 to set 25% powercap

# Get the command line argument and store it in the 'cap' variable
cap=$1

# Get the number of RAPL zones 
num_zones=$(powercap-info intel-rapl --nzones)

# Check if the user provided a cap argument
if [[ -z "$cap" ]]; then
    echo "Error: Please provide a power cap value as a command line argument."
    exit 1
fi

# Loop over the RAPL zones (0 to num_zones - 1)
for i in $(seq 0 $((num_zones-1))); do
    # Read the current maximum power limit for the zone
    echo $i

    max_power=$(cat /sys/class/powercap/intel-rapl/intel-rapl:$i/constraint_1_max_power_uw)
    echo $max_power

    # Calculate the new power constraint
    power_constraint_float=$(echo "$max_power * $cap" | bc)

    # Convert to integer (round down for safety)
    power_constraint=$(printf '%.*f\n' 0 $power_constraint_float) 

    echo $power_constraint

    # Apply the new power constraint
    powercap-set intel-rapl -z $i -c 1 -l $power_constraint

done