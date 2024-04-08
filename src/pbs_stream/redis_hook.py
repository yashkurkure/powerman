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
    if e.type is pbs.HOOK_EVENT_QUEUEJOB:
        event_type = 'queuejob'
        # Parameters to record
        _job_id = -1
        _nodes = int(j.Resource_List["nodes"].split(':ppn=')[0])
        _ppn = int(j.Resource_List["nodes"].split(':ppn=')[1])
        _walltime = j.Resource_List["walltime"]

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
        json_data['walltime'] = _walltime
        json_data['nodes'] = _nodes
        json_data['ppn'] = _ppn

    elif e.type == pbs.HOOK_EVENT_RUNJOB:
        event_type = 'runjob'
        # Parameters to record
        # TODO : record the node(s) to be run on

    elif e.type == pbs.HOOK_EVENT_EXECJOB_BEGIN:
        event_type = 'execjob_begin'
        # mom_name = pbs.get_local_nodename()
        json_data['mom_name'] = 'mom'
        # Parameters to record
        pass

    elif e.type == pbs.HOOK_EVENT_EXECJOB_END:
        event_type = 'execjob_end'
        # mom_name = pbs.get_local_nodename()
        json_data['mom_name'] = 'mom'
        # Parameters to record
        pass
    else:
        event_type = 'unknown'

    # Insert data into redis stream
    r.xadd(
        "pbs-hook-events",
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
