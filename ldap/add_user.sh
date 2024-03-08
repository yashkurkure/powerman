#!/bin/bash

# 1. Get user details
read -p "Enter username: " username
read -p "Enter gid: " gid
read -sp "Enter password: " password

# 2. Hash password (SSHA method recommended)
hashed_password=$(slappasswd -s "$password")

# 3. Create an LDIF file for the user
cat << EOF > user.ldif
dn: uid=$username,ou=users,dc=emulab,dc=net
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: $username 
sn: $username 
uid: $username
uidNumber: $(expr $(id -u) + 1000)  # Find next available UID
gidNumber: $gid
homeDirectory: /pbsusers/$username
userPassword: $hashed_password

EOF