import time

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