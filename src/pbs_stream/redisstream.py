from src.base_types.event_producer import *
from src.pbs_stream.types import PBSEvent
import redis

class RedisStream(EventProducer):

    def __init__(self, stream_name):
        super().__init__()
        self.stream_name = stream_name
        self.last_id = '$'
        self.conn = redis.Redis(host='head.testbed.schedulingpower.emulab.net', port=6379, decode_responses=True)

    def getEvent(self) -> list[PBSEvent]:
        super().getEvent()
        latest = self.conn.xread({self.stream_name: self.last_id}, None, 0)[0]
        stream_data = latest[1]
        events : list[PBSEvent] = []
        for data in stream_data:
            redis_id = data[0]
            e = self.process_redis_entry(data)
            events.append(e)
            self.last_id = redis_id
        return events

    
    def process_redis_entry(self, data) -> PBSEvent:
        # TODO: Process the redis entry
        return None
