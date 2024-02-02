import sys
sys.path.append('/usr/local/lib/python3.8/dist-packages')
import pbs
import os
import time
import redis
e = pbs.event()
timestamp = int(time.time() * 1000)
jid = str(pbs.event().job.Submit_arguments)
if jid:
    jid = jid.split('</jsdl-hpcpa:Argument><jsdl-hpcpa:Argument>')[1]
else:
    jid = 'Not found'
    
etype = pbs.event().type
location = '/pbsusers/sample_hook.out'

def write_swf(location,  content):
    if os.path.exists(location):
        # If the file exists, open it in append mode
        with open(location, 'a') as file:
            file.write(content + '\n')  # Append content to the file
    else:
        # If the file doesn't exist, create it and write to it
        with open(location, 'w') as file:
            file.write(content + '\n')  # Write content to the file

try:
    t = ''
    if etype is pbs.QUEUEJOB:
        t = 'q'
    elif etype is pbs.RUNJOB:
        t = 'r'
    elif etype is pbs.EXECJOB_BEGIN:
        t = 'mom_r'
    elif etype is pbs.EXECJOB_END:
        t = 'mom_e'
    else:
        t = etype

    s = f'{timestamp},{jid},{t}'
    write_swf(location, s)
    r = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)
    res1 = r.xadd(
        "pbs:hook",
        {"timestamp": f"{timestamp}", "job_id": f"{jid}", "event_type": t},
    )

    # accept the event
    e.accept() 
except SystemExit:
    pass 
except:
    pbs.event().reject_msg = f'{e.hook_name} hook failed with {sys.exc_info()[:2]}'
    e.reject("%s hook failed with %s. Please contact Admin" % (e.hook_name, sys.exc_info()[:2]))