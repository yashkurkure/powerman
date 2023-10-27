#!/bin/bash

# Install openPBS on Ubuntu 20.04
sudo apt update
sudo apt-get -y install expat libedit2 postgresql python3 postgresql-contrib sendmail-bin \
      sudo tcl tk libical3 postgresql-server-dev-all

sudo apt-get -y install /local/repository/cloudlab/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb

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