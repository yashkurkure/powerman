import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

res5 = r.xread(streams={"pbs:hook": 0}, count=100, block=300)
print(
    res5
) 