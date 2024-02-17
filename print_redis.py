import redis


swf_lines = []

def process_stream_entry(data):
    # TODO: Process to SWF formats
    swf_entry = {
	'id':1,
	'submit': 1641021254,
    'reqProc': 128,
	'reqTime': 10800,
	'reqMem': -1,

	'wait': 52645,

	'run': 10849,
	'usedProc': 128,
	'usedAveCPU': -1,
	'usedMem': -1,
	'status': 0,

	'userID': -1,
	'groupID': -1,
	'num_exe': -1,
	'num_queue': -1,
	'num_part': -1,
	'num_pre': -1,
	'thinkTime': 0,
	}
    redis_id = data[0]
    job_id = data[1]['job_id']
    event_type = data[1]['event_type']
    event_code = data[1]['event_code']

    """
    queuejob -> 0, 1*, 7*, 8*, 9, 11, 12, 13, 14, 15, 
    runjob,execjob_begin -> 2, 3
    execjob_end ->  4, 5, 6, 10, 16?, 17?
    """
    if event_type == 'q':
        # Parameters to record
        # id
        # submit
        # reqProc
        # reqTime
        # reqMem

        pass
    elif event_type == 'r':
        # Parameters to record
        # wait
        pass
    elif event_type == 'mom_r':
        # Parameters to record
        # none
        pass
    elif event_type == 'mom_e':
        # Parameters to record
        # run
        # usedProc
        # usedAveCPU
        # usedMem
        # status
        pass
    else:
        print('unknown')
        pass
    pass

def parse_args():
    """
    Parse the args.
    """
    import argparse
    print("----Args----")
    parser = argparse.ArgumentParser(description="Argument Parser")

    parser.add_argument("-s", "--redis_stream", type=str, default="redis-hook",
                        help="Redis stream name (default: 15)")

    args = parser.parse_args()
    print("Redis stream:", args.redis_stream)
    print("----Args----")
    return args


if __name__ == "__main__":
    args = parse_args()
    stream_name = args.redis_stream

    # TODO: update hostname for cloudlab
    r = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)
    last_id = '$'

    # List to the stream
    while True:

        # Wait for new entry
        latest = r.xread({stream_name: last_id}, None, 0)[0]
        print(f'** New In Stream **')
        stream_name = latest[0]
        stream_data = latest[1]
        for data in stream_data:
            process_stream_entry(data)
            redis_id = data[0]
            job_id = data[1]['job_id']
            event_type = data[1]['event_type']
            event_code = data[1]['event_code']
            print(f'{redis_id}\t{job_id}\t{event_type}\t{event_code}')
            last_id = redis_id
        print(f'*******************')

# 1 1641021254 52645 10849 128 -1 -1 128 10800 -1 0 -1 -1 -1 -1 -1 -1 0
# def create_swf_entry(
#         job_num,     # 0 
#         submit_time,    # 1
#         wait_time,      # 2
#         run_time,       # 3
#         num_proc,       # 4
#         avg_cpu_time=-1,   # 5
#         mem_usage=-1,      # 6
#         req_num_p,      # 7 same as # 4
#         req_time,       # 8
#         req_mem=-1,        # 9
#         job_status,     # 10
#         user_id,        # 11
#         group_id,       # 12
#         executable=-1,     # 13
#         queue_num=-1,      # 14
#         partition_num=-1,  # 15
#         preceding_job_num=-1,  #16
#         think_time=-1          #17
# ):
#     pass