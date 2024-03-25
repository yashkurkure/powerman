path_server=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb
path_mom=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_execution.deb
path_client=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_client.deb

ansible-playbook \
    -i /local/cluster_inventory.yml \
    --extra-vars "headnode_deb=$path_server workernodes_deb=$path_mom loginnodes_deb=$path_client"\
    /local/repository/ansible/openpbs.yml