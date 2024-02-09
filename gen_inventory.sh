#!/bin/bash
#
# Usage: ansible_gen_inventory.sh <number of worker nodes>
#
# Ansible test: 
# ANSIBLE_HOST_KEY_CHECKING=False ansible -i temp workernodes -m ping

# Specify the number of nodes as a argument to the script
numnodes=$1

# Username to configure ssh access for
username=$2

# Check if atleast 1 worker node
if ((numnodes < 1)); then
echo "Number of worker nodes should be atleast 1"
exit 1
fi

# Generate the ansible inventory
echo "# This file is autogenerated"
echo "# Local host - head node"
echo "[headnode]"
echo "127.0.0.1"
echo "# Variables for head node"
echo "[headnode:vars]"
echo "numworkernodes=$numnodes"
echo "ansible_user=root"
echo "ansible_private_key_file=/root/.ssh/id_rsa"
echo "ansible_host_key_checking=False"
echo "username"=$username
echo ""

echo "# Worker nodes"
echo "[workernodes]"
for ((i=0; i<numnodes; i++)); do
workerhostname=$(hostname | sed "s/head/node$i/")
workercanonicalname=$(nslookup $workerhostname | grep Name | awk '{print $2}')
echo $workerhostname
done

echo ""

echo "# Login nodes"
echo "[loginnodes]"
loginhostname=$(hostname | sed "s/head/login/")
logincanonicalname=$(nslookup $loginhostname | grep Name | awk '{print $2}')
echo $loginhostname

echo ""

echo "# All non-head nodes"
echo "[multi:children]"
echo "workernodes"
echo "loginnodes"
echo "# Variables for all nodes"
echo "[multi:vars]"
echo "ansible_user=root"
echo "ansible_private_key_file=/root/.ssh/id_rsa"
echo "ansible_host_key_checking=False"
serverhostname=$(hostname)
servercanonicalname=$(nslookup $serverhostname | grep Name | awk '{print $2}')
echo "servercanonicalname=$servercanonicalname"
echo "username"=$username

echo "# All nodes"
echo "[multi:allnodes]"
echo "workernodes"
echo "loginnodes"
echo "headnode"
echo "# Variables for all nodes"
echo "[multi:vars]"
echo "ansible_user=root"
echo "ansible_private_key_file=/root/.ssh/id_rsa"
echo "ansible_host_key_checking=False"
serverhostname=$(hostname)
servercanonicalname=$(nslookup $serverhostname | grep Name | awk '{print $2}')
echo "servercanonicalname=$servercanonicalname"
echo "serverhostname=$serverhostname"
echo "username"=$username