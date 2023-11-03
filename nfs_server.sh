#!/bin/bash
# Must be run with root permissions

# Create NFS directory
mkdir -p /exports/backup
mkdir -p /exports/documents

# Install NFS server
apt install -y nfs-kernel-server

# Check the status - should be active(exited)
systemctl status nfs-kernel-server

# Backup the original exports file
mv /etc/exports /etc/exports.orig

# Write paths of dirs to share to /etc/exports
echo "/exports/backup 10.10.1.0/255.255.255.0(rw,no_subtree_check)" >> /etc/exports
echo "/exports/documents 10.10.1.0/255.255.255.0(rw,no_subtree_check)" >> /etc/exports

# Restart the nfs server to apply changes
systemctl restart nfs-kernel-server

# Create some test files
echo "Hello from $(hostname)" >> /exports/backup/test1.txt
echo "Hello from $(hostname)" >> /exports/documents/test2.txt



