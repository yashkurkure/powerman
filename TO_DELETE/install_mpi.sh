#!/bin/bash
#
# Install OpenMPI

cd /pbsusers

curl -sO https://www.mpich.org/static/downloads/4.2.0rc2/mpich-4.2.0rc2.tar.gz

tar xfz mpich-4.2.0rc2.tar.gz

mkdir /pbsusers/mpich-install

mkdir /opt/mpich

cd /opt/mpich

sudo apt install gfortran

/pbsusers/mpich-4.2.0rc2/configure -prefix=/pbsusers/mpich-install 2>&1 | tee c.txt

make 2>&1 | tee m.txt

make install |& tee mi.txt