import redis
import json
import os


if __name__ == "__main__":
    stream_name = 'pbs-hook-events'
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
            redis_id = data[0]
            job_id = data[1]['job_id']
            event_type = data[1]['event_type']
            event_code = data[1]['event_code']
            print(f'{redis_id}\t{job_id}\t{event_type}\t{event_code}')
            last_id = redis_id
        print(f'*******************')
