#!/bin/bash
#
# Usage: create_worker_inventory.sh <number of worker nodes>
#
# Ansible test: 
# ANSIBLE_HOST_KEY_CHECKING=False ansible -i temp workernodes -m ping

# Specify the number of nodes as a argument to the script
numnodes=$1

# Check if atleast 1 worker node
if ((numnodes < 1)); then
        echo "Number of worker nodes should be atleast 1"
        exit 1
fi

# Generate the ansible inventory
echo "[workernodes]"
for ((i=0; i<numnodes; i++)); do
            echo "$(hostname | sed "s/head/node$i/")"
done
echo "[workernodes:vars]"
echo "ansible_user=root"
echo "ansible_host_key_checking=False"