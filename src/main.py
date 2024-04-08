import os
import argparse
from src.base_types import types
from util import *

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
        print('Capture state...')
        # timestamp, node_list, job_list = capture_state_pbs()
        # state = State(timestamp = timestamp, node_list= node_list, job_list= job_list)

