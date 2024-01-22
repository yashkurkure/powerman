# Starting PBS on Cloudlab


```
# Login as root on head node
sudo su

# Navigate to cloned repositoty
cd /local/repository/

# Generate ansible inventory
gen_inventory.sh $num_nodes > inventory

# Configure PBS
ansible-playbook -i inventory ./pbs_config.yml

# Configure NFS for common mount point
ansible-playbook -i inventory ./nfs_config.yml

# Copy scaling study files to NFS
cp -r /local/repository/scaling_study /pbsusers/

# Switch to job directory
cd /pbsusers/scaling_study

# Create executables required by the scaling study job
make

# Submit jobs to perform scaling study
./submitjobs.sh
```