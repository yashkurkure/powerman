import redis

stream_name = 'redis-hook'
# TODO: update hostname for cloudlab
r = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)
last_id = '$'

while True:

    # Wait for new entry
    latest = r.xread({stream_name: last_id}, None, 0)[0]
    print(f'** New In Stream **')
    stream_name = latest[0]
    stream_data = latest[1]
    for data in stream_data:
        redis_id = data[0]
        job_id = data[1]['job_id']
        event_type = data[1]['event_type']
        event_code = data[1]['event_code']
        print(f'{redis_id}\t{job_id}\t{event_type}\t{event_code}')
        last_id = redis_id
    print(f'*******************')


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