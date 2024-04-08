import os
import argparse
from base_types.types import *
from util import *
from pbs_stream.types import *
from pbs_stream.statemachine import *
from pbs_stream.redisstream import *
from pbs_stream.utils import capture_state_pbs

def parse_args():
    """
    Parse command line args
    """
    parser = argparse.ArgumentParser(description="Argument Parser")
    parser.add_argument('-C', '--capture_state', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    if args.capture_state:
        # Get the state from pbs
        state = capture_state_pbs()
        print('[Captured PBS State]---------------------------------------')

        # Create the event producer, in this case it is a redis stream
        event_stream = RedisStream(stream_name='pbs-hook-events')
        print('[Connected to Redis]---------------------------------------')

        # Create the state machine, in this case we just evaluate the events as is
        # In the case of a smiulation, the evaluator will contain code for the 
        # scheduling policy / algorithm
        stream_evaluator = StreamEvaluator()

        # Loop the stream
        while True:
            new_events = event_stream.getEvent()
            for event in new_events:
                print("[Event]---------------------------------------------")
                state = stream_evaluator.evaluate(state, event)
                metrics = stream_evaluator.evaluate_metrics(state)
                print("----------------------------------------------------")
                print(metrics)

