#!/bin/bash

# Install openPBS on Ubuntu 20.04
sudo apt update
sudo apt -y install expat libedit2 postgresql python3 postgresql-contrib sendmail-bin \
      sudo tcl tk libical3 postgresql-server-dev-all

sudo apt -y install /local/repository/cloudlab/openPBS/openpbs_23.06.06.ubuntu_20.04/openpbs_server.deb

# Install Ansible
sudo apt -y install software-properties-common
sudo add-apt-repository --y --update ppa:ansible/ansible
sudo apt -y install ansible