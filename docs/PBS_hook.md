# Creating PBS Hooks

This document provides an extension of the setup in [Starting a cluster with OpenPBS on Cloudlab](/docs/PBS_Cloudlab.md) by enabling PBS hooks.

## Configuration script

```
sudo su
cd /local/repository
./qmgr_hook_config.sh
```

## Sample hook description

The configuration scripts set up a [sample hook](/sample_hook.py) to be triggered at the following pbs events:

> queuejob,runjob,execjob_begin,execjob_end

At each event the hook records the event type, timestamp and any the job id. The information is saved to `/pbsusers/sample_hook.out`.
