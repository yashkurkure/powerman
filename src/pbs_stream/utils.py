from pbs_stream.types import *
import time
import datetime
def datetime_to_unix(datetime_str):
  """Converts a datetime string of format 'Sun Apr  7 11:24:51 2024' to Unix timestamp in seconds

  Args:
      datetime_str: The datetime string to convert.

  Returns:
      The Unix timestamp in seconds.
  """
  # Parse the datetime string and get the timestamp in seconds since epoch
  timestamp = time.mktime(time.strptime(datetime_str, "%a %b %d %H:%M:%S %Y"))
  return int(timestamp)

def walltime_to_seconds(time_str):
  """Converts a time string of format 'HH:MM:SS' to seconds.

  Args:
      time_str: The time string to convert.

  Returns:
      The time in seconds.
  """
  time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
  return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

import re

def parse_node_info(node_str):
  """
  Parses a string of format "(node0.testbed.schedulingpower.emulab.net:ncpus=1)+(node1.testbed.schedulingpower.emulab.net:ncpus=1)" 
  and outputs a dictionary of hostname : cpus

  Args:
      node_str: A string containing node information

  Returns:
      A dictionary containing node hostnames as keys and cpu counts as values
  """
  node_dict = {}
  for node in re.split(r"\+", node_str):
    hostname, ncpus = re.split(r"\:", node.strip()[1:-1])
    node_dict[hostname] = int(ncpus.split("=")[1])
  return node_dict

def capture_state_pbs():
    import subprocess
    import json
    cmd_pbsnodes= json.loads(subprocess.run(["pbsnodes", "-a", "-F", "json"], capture_output=True, text=True).stdout)
    cmd_qstat= json.loads(subprocess.run(["qstat", "-f", "-F", "json"], capture_output=True, text=True).stdout)

    # parse pbsnodes -a -F json
    timestamp = cmd_pbsnodes['timestamp']
    pbsnodes = cmd_pbsnodes['nodes']
    node_list = []
    id = 0
    for node_name in pbsnodes:
        n = PBSVNode(id=id,
                name=node_name, 
                cpus= pbsnodes[node_name]['pcpus'],
                online = True)
        id = id + 1
        node_list.append(n)

    # parse qsub -f -F json
    timestamp = cmd_qstat['timestamp']
    if 'Jobs' not in cmd_qstat:
       return PBSState(
          timestamp=timestamp, 
          node_list= node_list, 
          job_list=[])
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
        allocated_nodes = None
        if 'exec_vnode' in pbsjobs[pbs_job_id]:
            allocated_nodes = parse_node_info(pbsjobs[pbs_job_id]['exec_vnode'])
        j = PBSJob(
            id = job_id,
            exec_path= '',
            ppn = ppn,
            nodes = nodes,
            walltime=walltime,
            qtime=job_qtime,
            rtime=job_rtime,
            allocated_nodes=allocated_nodes
        )
        job_list.append(j)

    return PBSState(
       timestamp=timestamp, node_list= node_list, job_list=job_list)
