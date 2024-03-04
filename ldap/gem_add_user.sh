#!/bin/bash

# 1. Get user details
read -p "Enter username: " username
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
gidNumber: 1000  # Or any primary group ID
homeDirectory: /home/$username
userPassword: $hashed_password

EOF

# 4. Add the user to LDAP
sudo ldapadd -x -D cn=admin,dc=emulab,dc=net -W -f user.ldif 

# 5. Create the user on the system
sudo useradd -m -d /home/$username -s /bin/bash $username

# 6. Set the user's password
echo -e "$password\n$password" | sudo passwd $username