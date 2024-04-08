from pbs_stream.types import *
from pbs_stream.statemachine import *
from pbs_stream.redisstream import *
from pbs_stream.utils import capture_state_pbs

# Get the state from pbs
state = capture_state_pbs()

# Create the event producer, in this case it is a redis stream
event_stream = RedisStream(stream_name='pbs-hook-events')

# Create the state machine, in this case we just evaluate the events as is
# In the case of a smiulation, the evaluator will contain code for the 
# scheduling policy / algorithm
stream_evaluator = StreamEvaluator()

# Loop the stream
while True:
    new_events = event_stream.getEvent()
    for event in new_events:
        state = stream_evaluator.evaluate(state, event)


