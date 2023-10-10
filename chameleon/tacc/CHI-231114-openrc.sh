#!/usr/bin/env bash
export OS_PROJECT_ID="c59062b2d4584745a71b064e576f3019"
export OS_USERNAME="ykurkure@anl.gov"
export OS_PROTOCOL="openid"
export OS_IDENTITY_PROVIDER="chameleon"
export OS_DISCOVERY_ENDPOINT="https://auth.chameleoncloud.org/auth/realms/chameleon/.well-known/openid-configuration"
export OS_CLIENT_ID="keystone-tacc-prod"
export OS_ACCESS_TOKEN_TYPE="access_token"
export OS_CLIENT_SECRET="none"
export OS_REGION_NAME="CHI@TACC"
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi