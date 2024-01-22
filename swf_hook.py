import pbs
import sys
import os
'''
Contents of SWF row:

1. Job Number -- a counter field, starting from 1.
2. Submit Time -- in seconds. The earliest time the log refers to is zero, and is usually the submittal time of the first job. The lines in the log are sorted by ascending submittal times. It makes sense for jobs to also be numbered in this order.
3. Wait Time -- in seconds. The difference between the job's submit time and the time at which it actually began to run. Naturally, this is only relevant to real logs, not to models.
4. Run Time -- in seconds. The wall clock time the job was running (end time minus start time).
We decided to use "wait time" and "run time" instead of the equivalent "start time" and "end time" because they are directly attributable to the scheduler and application, and are more suitable for models where only the run time is relevant.
Note that when values are rounded to an integral number of seconds (as often happens in logs) a run time of 0 is possible and means the job ran for less than 0.5 seconds. On the other hand it is permissable to use floating point values for time fields.
5. Number of Allocated Processors -- an integer. In most cases this is also the number of processors the job uses; if the job does not use all of them, we typically don't know about it.
6. Average CPU Time Used -- both user and system, in seconds. This is the average over all processors of the CPU time used, and may therefore be smaller than the wall clock runtime. If a log contains the total CPU time used by all the processors, it is divided by the number of allocated processors to derive the average.
7. Used Memory -- in kilobytes. This is again the average per processor.
8. Requested Number of Processors.
9. Requested Time. This can be either runtime (measured in wallclock seconds), or average CPU time per processor (also in seconds) -- the exact meaning is determined by a header comment. In many logs this field is used for the user runtime estimate (or upper bound) used in backfilling. If a log contains a request for total CPU time, it is divided by the number of requested processors.
10. Requested Memory (again kilobytes per processor).
11. Status 1 if the job was completed, 0 if it failed, and 5 if cancelled. If information about chekcpointing or swapping is included, other values are also possible. See usage note below. This field is meaningless for models, so would be -1.
12. User ID -- a natural number, between one and the number of different users.
13. Group ID -- a natural number, between one and the number of different groups. Some systems control resource usage by groups rather than by individual users.
14. Executable (Application) Number -- a natural number, between one and the number of different applications appearing in the workload. in some logs, this might represent a script file used to run jobs rather than the executable directly; this should be noted in a header comment.
15. Queue Number -- a natural number, between one and the number of different queues in the system. The nature of the system's queues should be explained in a header comment. This field is where batch and interactive jobs should be differentiated: we suggest the convention of denoting interactive jobs by 0.
16. Partition Number -- a natural number, between one and the number of different partitions in the systems. The nature of the system's partitions should be explained in a header comment. For example, it is possible to use partition numbers to identify which machine in a cluster was used.
17. Preceding Job Number -- this is the number of a previous job in the workload, such that the current job can only start after the termination of this preceding job. Together with the next field, this allows the workload to include feedback as described below.
18. Think Time from Preceding Job -- this is the number of seconds that should elapse between the termination of the preceding job and the submittal of this one.


Example:
0 1    2     3    4   5  6   7  8     9   10  11  12   13 14 15 16 17
1 0000 11464 4000 40  -1 -1  40 4000  -1  1   17  17   -1 -1 -1 -1 -1

CQSim:
'id':int(temp_dataList[0]),\
'submit':self.density*(float(temp_dataList[1])-min_sub)+temp_start,\
'wait':float(temp_dataList[2]),\
'run':float(temp_dataList[3]),\
'usedProc':int(temp_dataList[4]),\
'usedAveCPU':float(temp_dataList[5]),\
'usedMem':float(temp_dataList[6]),\
'reqProc':int(temp_dataList[7]),\
'reqTime':float(temp_dataList[8]),\
'reqMem':float(temp_dataList[9]),\
'status':int(temp_dataList[10]),\
'userID':int(temp_dataList[11]),\
'groupID':int(temp_dataList[12]),\
'num_exe':int(temp_dataList[13]),\
'num_queue':int(temp_dataList[14]),\
'num_part':int(temp_dataList[15]),\
'num_pre':int(temp_dataList[16]),\
'thinkTime':int(temp_dataList[17]),\

'''

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