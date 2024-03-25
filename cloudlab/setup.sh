#!/bin/bash
# NOTE: Must be executed as root

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/nfs.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    --extra-vars "\
    headnodes_deb=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb \
    workernodes_deb=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_execution.deb \
    loginnodes_deb=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_client.deb"\
    /local/repository/ansible/openpbs.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/mpich.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    --extra-vars "username=ykurkure groupname=SchedulingPower"\
    /local/repository/ansible/ssh.yml