#!/bin/bash
# NOTE: Must be executed as root

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/nfs.yml

path_server=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb
path_mom=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_execution.deb
path_client=/local/repository/packages/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_client.deb
ansible-playbook \
    -i /local/cluster_inventory.yml \
    --extra-vars "headnode_deb=$path_server workernodes_deb=$path_mom loginnodes_deb=$path_client"\
    /local/repository/ansible/openpbs.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/mpich.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    --extra-vars "username=ykurkure"\
    /local/repository/ansible/ssh.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/pbs_hook_enable.yml

ansible-playbook \
    -i /local/cluster_inventory.yml\
    /local/repository/ansible/redis.yml

/opt/pbs/bin/qmgr -c 'create hook redis_hook'
/opt/pbs/bin/qmgr -c 'import hook redis_hook application/x-python default /local/repository/src/pbs_stream/redis_hook.py'
/opt/pbs/bin/qmgr -c 'set hook redis_hook event = "queuejob,runjob,jobobit,execjob_begin,execjob_end"'
/opt/pbs/bin/qmgr -c 'set hook redis_hook debug = True'

