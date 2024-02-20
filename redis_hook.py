import sys

# Import packages external to pbs, required for redis import
sys.path.append('/usr/local/lib/python3.8/dist-packages')
import pbs
import os
import time
import redis
import json
e = pbs.event()
j = e.job
try:
    r = redis.StrictRedis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)
    # Information to collect 
    event_type = ''
    event_code = e.type
    job_name = e.job.Job_Name
    json_data = {}

    # Find the event type
    if e.type is pbs.QUEUEJOB:
        event_type = 'q'
        # Parameters to record
        _job_id = -1
        _nodes = int(j.Resource_List["nodes"].split(':ppn=')[0])
        _ppn = int(j.Resource_List["nodes"].split(':ppn=')[1])
        _reqProc = _nodes * _ppn
        _reqTime = j.Resource_List["walltime"]
        _reqMem =  j.Resource_List["mem"]

        # Job ids - Using counter from Redis
        if r.exists('job_counter'):
            job_counter = r.incr('job_counter')
            job_name = f'job.{job_counter}'
            _job_id = job_counter
        else:
            # Key doesn't exist, create and initialize it to 0
            r.set('job_counter', 0)
            job_name = 'job.0'
            _job_id = 0
        j.Job_Name = job_name
        
        json_data['id'] = _job_id
        json_data['reqProc'] = _reqProc
        json_data['reqMem'] = _reqMem
        json_data['reqTime'] = _reqTime
        json_data['node'] = pbs.get_local_nodename()

    elif e.type == pbs.RUNJOB:
        event_type = 'r'
        # TODO : record the node(s) to be run on
        json_data['id'] = int(job_name.split('.')[1])
        json_data['node'] = pbs.get_local_nodename()
    elif e.type == pbs.EXECJOB_BEGIN:
        event_type = 'mom_r'
        json_data['id'] = int(job_name.split('.')[1])
        json_data['node'] = pbs.get_local_nodename()
    elif e.type == pbs.EXECJOB_END:
        event_type = 'mom_e'
        # Parameters to record
        _usedProc = -1
        _usedAveCPU = -1
        _usedMem = -1
        # 1 if the job was completed, 0 if it failed, and 5 if cancelled
        _status = -1
        json_data['id'] = int(job_name.split('.')[1])
        json_data['usedProc'] = _usedProc
        json_data['usedAveCPU'] = _usedAveCPU
        json_data['usedMem'] = _usedMem
        json_data['status'] = _status
        json_data['node'] = pbs.get_local_nodename()
    else:
        event_type = 'unknown'

    # Insert data into redis stream
    r.xadd(
        "redis-hook",
        { 
            "job_id": f"{job_name}", 
            "event_type": event_type, 
            "event_code": event_code,
            "json_data" : json.dumps(json_data)
        },
    )

    # accept the event
    pbs.event().accept() 
except SystemExit:
    pass 
except:
    pbs.event().reject_msg = f'{e.hook_name} hook failed with {sys.exc_info()[:2]}'
    pbs.event().reject("%s hook failed with %s. Please contact Admin" % (pbs.event().hook_name, sys.exc_info()[:2]))