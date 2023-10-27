sudo echo "PBS_EXEC=/opt/pbs
PBS_SERVER=head.openpbs-install.schedulingpower.emulab.net
PBS_START_SERVER=0
PBS_START_SCHED=0
PBS_START_COMM=0
PBS_START_MOM=1
PBS_HOME=/var/spool/pbs
PBS_CORE_LIMIT=unlimited
PBS_SCP=/usr/bin/scp" > /etc/pbs.conf

sudo systemctl start pbs