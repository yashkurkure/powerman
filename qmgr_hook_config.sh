/opt/pbs/bin/qmgr -c 'create hook sample_hook'
/opt/pbs/bin/qmgr -c 'import hook sample_hook application/x-python default ./sample_hook.py'
/opt/pbs/bin/qmgr -c 'set hook sample_hook event = "queuejob,runjob,execjob_begin,execjob_end"'
/opt/pbs/bin/qmgr -c 'set hook sample_hook debug = True'