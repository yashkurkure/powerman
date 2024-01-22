import pbs
import sys
import os

e = pbs.event()
etype = pbs.event().type
location = '/pbsusers/hook.swf'

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
    t = 0
    if etype is pbs.QUEUEJOB:
        t = 1
        write_swf(location, 'Queued')
    elif etype is pbs.RUNJOB:
        t = 2
        write_swf(location, 'Run')
    # accept the event
    e.accept() 
except SystemExit:
    pass 
except:
    e.reject("Failed to set job priority")