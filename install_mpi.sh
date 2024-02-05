#!/bin/bash
#
# Install OpenMPI

curl -sO https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.1.tar.bz2
bzip2 -d openmpi-5.0.1.tar.bz2
tar -xvf openmpi-5.0.1.tar
cd openmpi-5.0.1
export LD_LIBRARY_PATH=/opt/pbs/lib:$LD_LIBRARY_PATH  
export LDFLAGS="-L /opt/pbs/lib -lpbs -lpthread -lcrypto"
./configure --prefix=/opt/openmpi --with-tm=/opt/pbs --enable-mpi-interface-warning --enable-shared --enable-static 
make; make install