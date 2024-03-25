#!/bin/bash
# Must be run with root permissions

SERVER="10.10.1.1"

# Install NFS Client
apt install -y nfs-common

# List the mounts available on the server
showmount --exports $SERVER

# Create mount points
mkdir -p /mnt/nfs/backup
mkdir -p /mnt/nfs/documents

# Mount the NFS export
mount $SERVER:/exports/backup /mnt/nfs/backup
mount $SERVER:/exports/documents /mnt/nfs/documents

# Check for the test files
ls -l /mnt/nfs/backup
ls -l /mnt/nfs/documents

# Check the contents
cat /mnt/nfs/backup/test1.txt
cat /mnt/nfs/documents/test2.txt