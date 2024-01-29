# Starting a cluster with OpenPBS on Cloudlab

This document descirbes the process to setup the OpenPBS job scheduler on baremetal nodes leased from [Cloudlab](https://www.cloudlab.us/). 

## Cloudlab Setup
From the cloudlab GUI, navigate -  `Experiments > Start Experiment`. This page allows you to select an experiment profile.
Navigate `Change Profile > Search > "OpenPBS" `. You will have access to this profile as long as you are a part of the Scheduling-Power project.

Select `OpenPBS` and fill out the parametrized form for the experiment. This page contains the "setup" parameters that the profile script uses to boot the experiment.


>The cloudlab profile scripts are written using [geni-lib](https://gitlab.flux.utah.edu/emulab/geni-lib) maintained by the [GENI Federation](https://www.geni.net/get-involved/host-a-conference/). 

Next, in the finalize step select the cluster and name the experiment. 

> It was noted that `Emulab` cluster usually has mass amounts of nodes available, you could boot a cluster of upto 102 nodes with 1 head and 1 login. 

Follow with the next few steps, and wait for all nodes to boot up and finish running their startup services.

When the baremental nodes are ready:
<kbd> ![Cloudlab experiment status page](/docs/images/cloudlab_experiment_status_page.png?raw=true)</kbd>

> Here is a list of items the geni-lib script sets up:
> 
> - The parameterized form represented as the 'Profile' on cloudlab.
> - Any packages that need to be installed (OpenPBS/PostgreSQL, etc)
> - This script is also capable of defining various network topologies.

## Post Cloudlab Setup

SSH into the `head` node and perform the following steps:

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

> The post cloudlab setup cannot be moved into the `geni-lib` profile script because OpenPBS configuration is best performed when all nodes have booted up. For now, the project uses ansible to perform all post cloudlab setup. This also helps us to be independent of the cloudlab platform.