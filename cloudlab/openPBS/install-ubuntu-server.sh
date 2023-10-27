#!/bin/bash

# Install openPBS on Ubuntu 20.04
sudo apt update
sudo apt-get -y expat libedit2 postgresql python3 postgresql-contrib sendmail-bin \
      sudo tcl tk libical3 postgresql-server-dev-all

sudo apt-get -y install /local/repository/cloudlab/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb

# Start postgresql service
sudo systemctl start postgresql

# Start
sudo mkdir -p /var/spool/pbs/datastore
sudo chown -R postgres:postgres /var/spool/pbs/datastore

PBS_DATA_SERVICE_USER=postgres; sudo /etc/init.d/pbs start