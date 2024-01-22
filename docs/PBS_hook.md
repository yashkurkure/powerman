# Sample commands to create hooks

```
create hook swf_hook
import hook swf_hook application/x-python default ./swf_hook.py
set hook swf_hook event = "queuejob,runjob"
set hook swf_hook debug = True
```