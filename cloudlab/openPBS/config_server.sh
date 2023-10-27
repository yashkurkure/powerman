#!/bin/bas
# Run as root

echo "PBS_EXEC=/opt/pbs
PBS_SERVER=head.openpbs-install.schedulingpower.emulab.netx
PBS_START_SERVER=1
PBS_START_SCHED=1
PBS_START_COMM=1
PBS_START_MOM=0
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf


# Start
mkdir -p /var/spool/pbs/datastore
chown -R postgres:postgres /var/spool/pbs/datastore

# Start postgresql service
pg_ctlcluster 12 main start

PBS_DATA_SERVICE_USER=postgres; sudo systemctl start pbs

qmgr -c  "create node node0.openpbs-install.schedulingpower.emulab.net"
qmgr -c  "create node node1.openpbs-install.schedulingpower.emulab.net"
qmgr -c  "create queue testq queue_type=e,enabled=t,started=t"