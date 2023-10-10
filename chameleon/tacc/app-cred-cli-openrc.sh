#!/usr/bin/env bash

echo '[TACC] Loading openrc application credential...'
export OS_AUTH_TYPE=v3applicationcredential
export OS_AUTH_URL=https://chi.tacc.chameleoncloud.org:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_REGION_NAME="CHI@TACC"
export OS_INTERFACE=public
export OS_APPLICATION_CREDENTIAL_ID=dbe8596073ef4749897b997dc1ee58a7
export OS_APPLICATION_CREDENTIAL_SECRET=power
