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
echo "[SERVER - ANSIBLE] Generating inventory..."
./ansible_gen_inventory.sh $numnodes > inventory

# Configure the worker nodes using ansible
echo "[SERVER - ANSIBLE] Configuring worker nodes..."
ansible-playbook -i inventory pbs_config_workernodes.yml

# Update the config for the server
echo "[SERVER - PBS] Configuring /etc/pbs.conf..."
serverhostname=$(hostname)
servercanonicalname=$(nslookup $serverhostname | grep Name | awk '{print $2}')
echo "PBS_EXEC=/opt/pbs
PBS_SERVER=$serverhostname
PBS_START_SERVER=1
PBS_START_SCHED=1
PBS_START_COMM=1
PBS_START_MOM=0
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf


# Update postgres user permissions for pbs directories
echo "[SERVER - PBS] Configuring postgresql..."
mkdir -p /var/spool/pbs/datastore
chown -R postgres:postgres /var/spool/pbs/datastore

# Start postgresql service
echo "[SERVER - PBS] Starting postgresql..."
pg_ctlcluster 12 main start

# Start the pbs service
echo "[SERVER - PBS] Starting pbs service..."
# NOTE: postgres is the default user that is used by postgresql-12.
PBS_DATA_SERVICE_USER=postgres; sudo systemctl start pbs

# Add nodes to pbs
echo "[SERVER - PBS] QMGR - Creating nodes..."
for ((i=0; i<numnodes; i++)); do
        workerhostname=$(hostname | sed "s/head/node$i/")
        workercanonicalname=$(nslookup $workerhostname | grep Name | awk '{print $2}')
        echo "[SERVER - PBS] QMGR - Adding node: $workerhostname"
        qmgr -c  "create node $workerhostname"
done

# Configure login nodes using ansible
echo "[SERVER - ANSIBLE] Configuring login nodes..."
ansible-playbook -i inventory pbs_config_loginnodes.yml

# Configure the pbsusers group
echo "[SERVER - ANSIBLE] Configuring pbsusers group..."
./pbs_config_group.sh