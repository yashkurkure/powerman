#!/bin/bash
# Run this script as root.
# This script should be run on the head node.
#
#
# Usage: ./pbs_config.sh <num_worker_nodes>
#
#
# ------ Script Args ------
# Specify the number of nodes as a argument to the script
numnodes=$1
# -------------------------

# Generate the ansible inventory file
./ansible_gen_inventory.sh $numnodes > inventory

# Configure the worker nodes using ansible
ansible-playbook -i inventory pbs_config_workernodes.yml

# Update the config for the server
echo "PBS_EXEC=/opt/pbs
PBS_SERVER=head.openpbs-install.schedulingpower.emulab.net
PBS_START_SERVER=1
PBS_START_SCHED=1
PBS_START_COMM=1
PBS_START_MOM=0
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf


# Update postgres user permissions for pbs directories
mkdir -p /var/spool/pbs/datastore
chown -R postgres:postgres /var/spool/pbs/datastore

# Start postgresql service
pg_ctlcluster 12 main start

# Start the pbs service
PBS_DATA_SERVICE_USER=postgres; sudo systemctl start pbs

# Add nodes to pbs
for ((i=0; i<numnodes; i++)); do
qmgr -c  "create node $(hostname | sed "s/head/node$i/").openpbs-install.schedulingpower.emulab.net"
done
qmgr -c  "create queue testq queue_type=e,enabled=t,started=t"

