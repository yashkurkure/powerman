from src.base_types.types import *
from src.base_types.types import Job, Node

class VNode(Node):
    def __init__(self, id, name, cpus, online):
        super().__init__(id, name, cpus, online)


class PBSEvent(Event):

    # PBS Event location
    EVENT_LOCATION_SERVER = 'event_location_server'
    EVENT_LOCATION_MOM = 'event_location_mom'

    # PBS Event types
    EVENT_TYPE_QUEUEJOB = 'queuejob'
    EVENT_TYPE_RUNJOB = 'runjob'
    EVENT_TYPE_JOBOBIT = 'jobobit'

    def __init__(self, 
                 timestamp: int,
                 event_type: str,
                 event_location: str
                ):
        super().__init__(
            timestamp=timestamp,
            event_type=event_type,
            description=f"BaseEvent"
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.event_location = event_location


class JobQueue(PBSEvent):
    def __init__(self, 
                 timestamp: int,
                 job: Job
                ):
        super().__init__(
            timestamp=timestamp, 
            event_type=PBSEvent.EVENT_TYPE_QUEUEJOB, 
            event_location=PBSEvent.EVENT_LOCATION_SERVER
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.job = job

class JobRun(PBSEvent):
    def __init__(self, 
                 timestamp: int, 
                 job_id: str,
                 rtime: int,
                 allocated_nodes: dict[str, int]
                ):
        super().__init__(
            timestamp=timestamp, 
            event_type=PBSEvent.EVENT_TYPE_RUNJOB
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.job_id = job_id
        self.rtime = rtime,
        self.allocated_nodes = allocated_nodes

class JobEnd(PBSEvent):
    def __init__(self, 
                 timestamp : int,
                 job_id: int,
                 etime: int
                ):
        super().__init__(
            event_type=PBSEvent.EVENT_TYPE_JOBOBIT, 
            timestamp=timestamp
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.job_id = job_id
        self.etime = etime

class PBSState(State):
    def __init__(self, timestamp: int, node_list: list[Node], job_list: list[Job]):
        super().__init__(timestamp, node_list, job_list)
        self.resource_utilization = 0.0