#!/bin/bash

# 1. Update and upgrade the system
# sudo apt update && sudo apt upgrade -y

# 2. Install OpenLDAP packages
sudo apt install slapd ldap-utils -y

# 3. Reconfigure slapd (OpenLDAP server)
sudo dpkg-reconfigure slapd

# During reconfiguration, provide the following:
# * Omit OpenLDAP server configuration?  -> No
# * DNS domain name -> Your domain name (e.g., example.com)
# * Organization name -> Your organization's name 
# * Administrator password -> A secure password for LDAP administration
# * Database backend to use? -> MDB
# * Remove the database when slapd is purged? -> No
# * Move old database? -> Yes
# * Allow LDAPv2 protocol? -> No

# 4. Create a base LDAP structure (adjust domain components as needed)
sudo ldapadd -x -D cn=admin,dc=emulab,dc=net -W -f base.ldif

# Where 'base.ldif' contains:
# dn: dc=example,dc=com
# objectClass: dcObject
# objectClass: organization
# dc: example
# o: Example Organization

# 5. Add organizational units for 'users' and 'groups'
sudo ldapadd -x -D cn=admin,dc=emulab,dc=net -W -f ou.ldif 

# Where 'ou.ldif' contains:
# dn: ou=users,dc=example,dc=com
# objectClass: organizationalUnit
# ou: users

# dn: ou=groups,dc=example,dc=com
# objectClass: organizationalUnit
# ou: groups 