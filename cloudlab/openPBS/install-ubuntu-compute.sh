#!/bin/bash

# Install openPBS on Ubuntu 20.04
sudo apt update
sudo apt-get -y install gcc make libtool libhwloc-dev libx11-dev \
      libxt-dev libedit-dev libical-dev ncurses-dev perl \
      postgresql-server-dev-all python-dev tcl-dev tk-dev swig \
      libexpat-dev libssl-dev libxext-dev libxft-dev autoconf \
      automake
sudo apt-get -y install expat libedit2 postgresql python sendmail-bin \
      sudo tcl tk libical1a

sudo apt-get -y install /local/repository/cloudlab/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_execution.deb

sudo echo "PBS_EXEC=/opt/pbs
PBS_SERVER=head
PBS_START_SERVER=0
PBS_START_SCHED=0
PBS_START_COMM=0
PBS_START_MOM=1
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf

sudo systemctl start pbs


