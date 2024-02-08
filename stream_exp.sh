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

ansible-playbook -i inventory ./redis_config.yml

ansible-playbook -i inventory ./pbs_hook_enable.yml

/opt/pbs/bin/qmgr -c 'create hook redis_hook'

/opt/pbs/bin/qmgr -c 'import hook redis_hook application/x-python default ./redis_hook.py'

/opt/pbs/bin/qmgr -c 'set hook redis_hook event = "queuejob,runjob,execjob_begin,execjob_end"'

/opt/pbs/bin/qmgr -c 'set hook redis_hook debug = True'

ansible-playbook -i inventory ./mpich_config_pkg.yml