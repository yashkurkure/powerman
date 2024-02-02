import redis

r = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)

stream_results = r.xread(streams={"pbs:hook": 0}, count=100, block=300)
for stream_result in stream_results:
    stream_name = stream_result[0]
    stream_data = stream_result[1]
    for data in stream_data:
        id = data[0]
        t = data[1]['timestamp']
        jid = data[1]['job_id']
        e = data[1]['event_type']
        print(f'{id}\t{t}\t{jid}\t{e}')