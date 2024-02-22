import redis
import json
import os

swf_lines = []
qstat = {}
location = '/pbsusers/log.swf'

def process_stream_entry(data):
    # TODO: Process to SWF formats
    redis_id = data[0]
    timestamp_ms = int(redis_id.split('-')[0])
    timestamp_s = int(timestamp_ms/1000)
    # job_id = data[1]['job_id']
    event_type = data[1]['event_type']
    # event_code = data[1]['event_code']
    json_data = json.loads(data[1]['json_data'])
    id = int(data[1]['job_id'].split('.')[1])

    """
    queuejob -> 0, 1*, 7*, 8*, 9, 11, 12, 13, 14, 15, 
    runjob,execjob_begin -> 2, 3
    execjob_end ->  4, 5, 6, 10, 16?, 17?
    """
    if event_type == 'q':
        # Parameters to record
        submit = timestamp_s
        reqProc = json_data['reqProc']
        reqTime = json_data['reqTime']
        reqMem = -1
        # reqMem = json_data['']
        qstat[id] = {
            'id':id,
            'submit': submit,
            'reqProc': reqProc,
            'reqTime': reqTime,
            'reqMem': reqMem,
        }
        write_swf_json(qstat[id])
        # print(json_data)
    elif event_type == 'r':
        # Parameters to record
        # wait = timestamp_s - submit
        qstat[id]['wait'] = timestamp_s - qstat[id]['submit']
        write_swf_json(qstat[id])
        # print(json_data)
    elif event_type == 'mom_r':
        # Parameters to record
        # none
        # print(json_data)
        pass
    elif event_type == 'mom_e':
        # Parameters to record
        # run = timestamp_s - submit - wait
        # usedProc
        # usedAveCPU
        # usedMem
        # status
        if id in qstat:
            write_swf_json(qstat[id])
            del qstat[id]
        # print(json_data)
        pass
    else:
        # print('!!unknown')
        # print(json_data)
        pass
    pass

def parse_args():
    """
    Parse the args.
    """
    import argparse
    # print("----Args----")
    parser = argparse.ArgumentParser(description="Argument Parser")

    parser.add_argument("-s", "--redis_stream", type=str, default="redis-hook",
                        help="Redis stream name (default: 15)")

    args = parser.parse_args()
    # print("Redis stream:", args.redis_stream)
    # print("----Args----")
    return args

def write_swf_json(j):
    print(json.dumps(j))


def create_swf_entry(
        job_num,     # 0 
        submit_time,    # 1
        wait_time,      # 2
        run_time,       # 3
        num_proc,       # 4
        avg_cpu_time,   # 5
        mem_usage,      # 6
        req_num_p,      # 7 same as # 4
        req_time,       # 8
        req_mem,        # 9
        job_status,     # 10
        user_id,        # 11
        group_id,       # 12
        executable,     # 13
        queue_num,      # 14
        partition_num,  # 15
        preceding_job_num,  #16
        think_time      #17
):
    return [
        job_num,     # 0 
        submit_time,    # 1
        wait_time,      # 2
        run_time,       # 3
        num_proc,       # 4
        avg_cpu_time,   # 5
        mem_usage,      # 6
        req_num_p,      # 7 same as # 4
        req_time,       # 8
        req_mem,        # 9
        job_status,     # 10
        user_id,        # 11
        group_id,       # 12
        executable,     # 13
        queue_num,      # 14
        partition_num,  # 15
        preceding_job_num,  #16
        think_time      #17
    ]

def create_swf_json(
        job_num,     # 0 
        submit_time,    # 1
        wait_time,      # 2
        run_time,       # 3
        num_proc,       # 4
        avg_cpu_time,   # 5
        mem_usage,      # 6
        req_num_p,      # 7 same as # 4
        req_time,       # 8
        req_mem,        # 9
        job_status,     # 10
        user_id,        # 11
        group_id,       # 12
        executable,     # 13
        queue_num,      # 14
        partition_num,  # 15
        preceding_job_num,  #16
        think_time      #17
):
    return {
	'id':job_num,
	'submit': submit_time,
    'reqProc': num_proc,
	'reqTime': req_time,
	'reqMem': req_mem,
	'wait': wait_time,
	'run': run_time,
	'usedProc': num_proc,
	'status': job_status,
	}

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
        # print(f'** New In Stream **')
        stream_name = latest[0]
        stream_data = latest[1]
        for data in stream_data:
            redis_id = data[0]
            job_id = data[1]['job_id']
            event_type = data[1]['event_type']
            event_code = data[1]['event_code']
            # print(f'{redis_id}\t{job_id}\t{event_type}\t{event_code}')
            process_stream_entry(data)
            last_id = redis_id
        # print(f'*******************')

# 1 1641021254 52645 10849 128 -1 -1 128 10800 -1 0 -1 -1 -1 -1 -1 -1 0
