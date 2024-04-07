import os
import argparse
from node import Node
from job import Job
from util import datetime_to_unix
from util import walltime_to_seconds

def capture_state_pbs():
    import subprocess
    import json
    cmd_pbsnodes= json.loads(subprocess.run(["pbsnodes", "-a", "-F", "json"], capture_output=True, text=True).stdout)
    cmd_qstat= json.loads(subprocess.run(["qstat", "-f", "-F", "json"], capture_output=True, text=True).stdout)

    timestamp = cmd_pbsnodes['timestamp']
    print(timestamp)
    pbsnodes = cmd_pbsnodes['nodes']
    node_list = []
    id = 0
    for node_name in pbsnodes:
        n = Node(id=id,
                name=node_name, 
                cpus= pbsnodes[node_name]['pcpus'],
                online = True)
        id = id + 1
        node_list.append(n)

    timestamp = cmd_qstat['timestamp']
    print(timestamp)
    pbsjobs = cmd_qstat['Jobs']
    job_list = []
    for pbs_job_id in pbsjobs:
        job_id = 'job.' + str(pbs_job_id.split('.')[0])
        job_state = pbsjobs[pbs_job_id]['job_state']
        job_qtime = datetime_to_unix(pbsjobs[pbs_job_id]['qtime'])
        if 'stime' in pbsjobs[pbs_job_id]:
            job_rtime = datetime_to_unix(pbsjobs[pbs_job_id]['stime'])
        else:
            job_rtime = -1
        nodes = pbsjobs[pbs_job_id]['Resource_List']['nodes'].split(':ppn=')[0]
        ppn = pbsjobs[pbs_job_id]['Resource_List']['nodes'].split(':ppn=')[1]
        walltime = walltime_to_seconds(pbsjobs[pbs_job_id]['Resource_List']['walltime'])
        print(f'Job: {job_id}')
        print(f'\tstate: {job_state}')
        print(f'\tqtime: {job_qtime}')
        print(f'\tstime: {job_rtime}')
        print(f'\tnodes: {nodes}')
        print(f'\tppn: {ppn}')
        print(f'\twalltime" {walltime}')
        j = Job(
            id = job_id,
            exec_path= '',
            ppn = ppn,
            nodes = nodes,
            walltime=walltime,
            qtime=job_qtime,
            rtime=job_rtime,
            pbs_state=job_state
        )
        




def parse_args():
    """
    Parse command line args
    """
    parser = argparse.ArgumentParser(description="Argument Parser")
    parser.add_argument('-C', '--capture_state', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    if args.capture_state:
        print('Capture state...')
        capture_state_pbs()

