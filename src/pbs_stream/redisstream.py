from src.base_types.event_producer import *
from src.pbs_stream.types import *
import redis
from src.pbs_stream.utils import walltime_to_seconds

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
            e = self._process_redis_entry(data)
            events.append(e)
            self.last_id = redis_id
        return events

    
    def _process_redis_entry(self, data) -> PBSEvent:
        import json
        redis_id = data[0]
        job_id = data[1]['job_id']
        timestamp_ms = int(redis_id.split('-')[0])
        timestamp = int(timestamp_ms/1000)
        event_type = data[1]['event_type']
        json_data = json.loads(data[1]['json_data'])
        
        if event_type == PBSEvent.EVENT_TYPE_QUEUEJOB:
            j = PBSJob(
                id = job_id,
                nodes = json_data['nodes'],
                ppn = json_data['ppn'],
                walltime = walltime_to_seconds(json_data['walltime']),
                exec_path='',
                qtime=timestamp
            )
            return JobQueue(timestamp=timestamp, job=j)
        elif event_type == PBSEvent.EVENT_TYPE_RUNJOB:
            return JobRun(
                timestamp=timestamp,
                job_id=job_id,
                rtime=timestamp
            )
        elif event_type == PBSEvent.EVENT_TYPE_EXECJOB_BEGIN:
            return JobMoMBegin(
                timestamp=timestamp,
                job_id=job_id,
                rtime=timestamp,
                mom_name=json_data['mom_name']
            )
        elif event_type == PBSEvent.EVENT_TYPE_EXECJOB_END:
            return JobEnd(
                timestamp=timestamp,
                job_id=job_id,
                etime=timestamp,
                mom_name=json_data['mom_name']
            )
        else:
            return None
