#!/bin/bash
#
# Usage: ./pbs_config_user.sh <username> <ssh-key.pub>
#
#
# Creates a user as a part of the pbsusers group.
# Creates a ssh-key pair that can be used to login through the login node.
# NOTE: Must be run with root.

username=$1
sshkey=$2

# Create the user accross the cluster
echo "[USERADD] Adding user to cluster..."
useradd -m $username
ansible -i inventory multi -a "useradd -m $username"

echo "[USERMOD] Adding user to group pbsusers..."
usermod -aG pbsusers $username
ansible -i inventory multi -a "usermod -aG pbsusers $username"

# Add ssh key to user's home on the login node
echo "[SSH-KEY] Adding public key to login node..."
ansible -i inventory loginnodes -a "mkdir -p /home/$username/.ssh"
ansible -i inventory loginnodes -m lineinfile -a "path=/home/$username/.ssh/authorized_keys line='$sshkey' create=yes"