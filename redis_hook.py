import sys

# Import packages external to pbs, required for redis import
sys.path.append('/usr/local/lib/python3.8/dist-packages')
import pbs
import os
import time
import redis
e = pbs.event()
try:

    # Information to collect 
    event_type = ''
    event_code = e.type
    job_name = e.job.Job_Name

    # Find the event type
    if e.type is pbs.QUEUEJOB:
        event_type = 'q'
        job_name = str(pbs.event().job.Submit_arguments)
        job_name = job_name.split('</jsdl-hpcpa:Argument><jsdl-hpcpa:Argument>')[1].split(',')[0].split('=')[1]
        pbs.event().job.Job_Name = job_name
    elif e.type is pbs.RUNJOB:
        event_type = 'r'
    elif e.type is pbs.EXECJOB_BEGIN:
        event_type = 'mom_r'
    elif e.type is pbs.EXECJOB_END:
        event_type = 'mom_e'
    else:
        event_type = 'unknown'

    # Insert data into redis stream
    r = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)
    r.xadd(
        "redis-hook",
        { "job_id": f"{job_name}", "event_type": event_type, "event_code": event_code},
    )

    # accept the event
    pbs.event().accept() 
except SystemExit:
    pass 
except:
    pbs.event().reject_msg = f'{e.hook_name} hook failed with {sys.exc_info()[:2]}'
    pbs.event().reject("%s hook failed with %s. Please contact Admin" % (pbs.event().hook_name, sys.exc_info()[:2]))