# NOTE: Ansible must append the server address above
# server = "head.testbed.schedulingpower.emulab.net"
import sys
# Import packages external to pbs, required for redis import
sys.path.append('/usr/local/lib/python3.8/dist-packages')
import pbs
import os
import time
from kafka import KafkaProducer 
import json

# Kafka configuration
conf = {
    'bootstrap_servers': ['head.testbed.schedulingpower.emulab.net:9092'],  # List of servers
    'client_id': 'python-producer',
    # 'batch.num.messages': 1,  # No direct equivalent in kafka-python, but you can control batching with other settings if needed
}

# Create the producer instance
producer = KafkaProducer(**conf)



e = pbs.event()
j = e.job
try:
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
        mom_name = pbs.get_local_nodename()
        json_data['mom_name'] = mom_name
        # Parameters to record
        pass

    elif e.type == pbs.HOOK_EVENT_EXECJOB_END:
        event_type = 'execjob_end'
        mom_name = pbs.get_local_nodename()
        json_data['mom_name'] = mom_name
        # Parameters to record
        pass
    elif e.type == pbs.HOOK_EVENT_JOBOBIT:
        event_type = 'jobobit'

    else:
        event_type = 'unknown'

    producer.send('pbsevents', value=json.dumps(json_data).encode('utf-8'))  # Encode value to bytes
    

    # Uncomment if the hook must wait for the producer to send the message
    # Send the message (using producer.send)
    # future = producer.send('pbsevents', value=json.dumps(json_data).encode('utf-8'))

    # Wait for the message to be acknowledged (optional, but ensures it's sent)
    #record_metadata = future.get(timeout=10)  # Wait up to 10 seconds for acknowledgement


    # accept the event
    pbs.event().accept() 
except SystemExit:
    pass 
except:
    pbs.event().reject_msg = f'{e.hook_name} hook failed with {sys.exc_info()[:2]}'
    pbs.event().reject("%s hook failed with %s. Please contact Admin" % (pbs.event().hook_name, sys.exc_info()[:2]))