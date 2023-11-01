#!/bin/bash
#
# Usage: ./pbs_config_group.sh
#
# Creates a group "pbsusers" for users using pbs.
# These users also get ssh access to the login nodes.

groupadd pbsusers

ansible -i inventory multi -a "groupadd pbsusers"