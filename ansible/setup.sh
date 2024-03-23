#!/bin/bash


num_login_nodes=$1
num_worker_nodes=$1
inventory_path=$3

# Install Ansible
sudo apt -y install software-properties-common
sudo add-apt-repository --y --update ppa:ansible/ansible
sudo apt -y install ansible

# Generate Ansible Inventory
python3 /local/repository/ansible/inventory.py \
    -nln $num_login_nodes -nwn $num_worker_nodes -C $inventory_path