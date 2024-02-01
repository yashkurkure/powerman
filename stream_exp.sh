#!/bin/bash
#
# Usage: post.sh <number of worker nodes>

# Specify the number of nodes as a argument to the script
numnodes=$1

# Check if atleast 1 worker node
if ((numnodes < 1)); then
echo "Number of worker nodes should be atleast 1"
exit 1
fi

./gen_inventory.sh $numnodes > inventory

ansible-playbook -i inventory ./pbs_config.yml

ansible-playbook -i inventory ./nfs_config.yml

cp -r /local/repository/scaling_study /pbsusers/

ansible-playbook -i inventory ./redis_config.yml