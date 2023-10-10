#!/usr/bin/env bash
echo '[UC] Loading openrc application credential...'
export OS_AUTH_TYPE=v3applicationcredential
export OS_AUTH_URL=https://chi.uc.chameleoncloud.org:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_REGION_NAME="CHI@UC"
export OS_INTERFACE=public
export OS_APPLICATION_CREDENTIAL_ID=844bca757ad14d43bbf35f53a9915824
export OS_APPLICATION_CREDENTIAL_SECRET=power
