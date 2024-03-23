#!/bin/bash

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/nfs.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/openpbs.yml