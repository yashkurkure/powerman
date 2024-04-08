from src.base_types.types import *
from src.pbs_stream.types import *
from src.pbs_stream.statemachine import *
from src.pbs_stream.redisstream import *

# Populate the job list
job_list = []
node_list = []

# Create initial state
state = State(job_list=job_list, node_list=node_list)

# Create the event produced, in this case it is a redis stream
event_stream = RedisStream(stream_name='pbs_hook_events')

# Create the state machine, in this case we just evaluate the events as is
stream_evaluator = StreamEvaluator()

# Loop the stream
while True:
    new_events = event_stream.getEvent()
    for event in new_events:
        state = stream_evaluator.evaluate(state, event)


