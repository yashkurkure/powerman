#!/bin/bash

# Install openPBS on Cent OS (8, 8 stream?)
dnf install -y dnf-plugins-core
dnf config-manager --set-enabled powertools
dnf install -y gcc make rpm-build libtool hwloc-devel \
      libX11-devel libXt-devel libedit-devel libical-devel \
      ncurses-devel perl postgresql-devel postgresql-contrib python3-devel tcl-devel \
      tk-devel swig expat-devel openssl-devel libXext libXft \
      autoconf automake gcc-c++
yum install -y expat libedit postgresql-server postgresql-contrib python3 \
      sendmail sudo tcl tk libical
tar -xpvf openpbs-20.0.0.tar.gz
cd openpbs-20.0.0 && ./autogen.sh
