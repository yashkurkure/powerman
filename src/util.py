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