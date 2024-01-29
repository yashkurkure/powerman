/opt/pbs/bin/qmgr -c 'create hook swf_hook'
/opt/pbs/bin/qmgr -c 'import hook swf_hook application/x-python default ./swf_hook.py'
/opt/pbs/bin/qmgr -c 'set hook swf_hook event = "queuejob,runjob,execjob_begin,execjob_end"'
/opt/pbs/bin/qmgr -c 'set hook swf_hook debug = True'