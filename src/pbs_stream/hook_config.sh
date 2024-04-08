/opt/pbs/bin/qmgr -c 'create hook redis_hook'
/opt/pbs/bin/qmgr -c 'import hook redis_hook application/x-python default ./redis_hook.py'
/opt/pbs/bin/qmgr -c 'set hook redis_hook event = "queuejob,runjob,execjob_end"'
/opt/pbs/bin/qmgr -c 'set hook redis_hook debug = True'