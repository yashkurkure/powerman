#!/bin/bash

# Install openPBS on Ubuntu 20.04
sudo apt update
sudo apt-get -y install expat libedit2 postgresql python3 postgresql-contrib sendmail-bin \
      sudo tcl tk libical3 postgresql-server-dev-all

sudo apt-get -y install /local/repository/cloudlab/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_execution.deb
