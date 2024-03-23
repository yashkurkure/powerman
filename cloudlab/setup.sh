#!/bin/bash
# NOTE: Must be executed as root


ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/nfs.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/openpbs.yml