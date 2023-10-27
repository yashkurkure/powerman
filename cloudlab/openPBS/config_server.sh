#!/bin/bash
sudo echo "PBS_EXEC=/opt/pbs
PBS_SERVER=$(hostname)
PBS_START_SERVER=1
PBS_START_SCHED=1
PBS_START_COMM=1
PBS_START_MOM=0
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf


# Start
sudo mkdir -p /var/spool/pbs/datastore
sudo chown -R postgres:postgres /var/spool/pbs/datastore

# Start postgresql service
# sudo systemctl start postgresql
sudo pg_ctlcluster 12 main start

PBS_DATA_SERVICE_USER=postgres; sudo systemctl start pbs