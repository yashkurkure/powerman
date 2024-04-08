from src.base_types.types import *
from src.base_types.types import Job, Node

class PBSVNode(Node):
    def __init__(self, id, name, cpus, online):
        super().__init__(id, name, cpus, online)

class PBSJob(Job):
    def __init__(self, 
                 id, 
                 nodes: int, 
                 ppn: int, 
                 walltime: int, 
                 exec_path, 
                 qtime: int, 
                 rtime: int = -1, 
                 etime: int = -1, 
                 allocated_nodes=None
                ):
        super().__init__(id, nodes, ppn, walltime, exec_path, qtime, rtime, etime, allocated_nodes)

class PBSEvent(Event):

    # PBS Event location
    EVENT_LOCATION_SERVER = 'event_location_server'
    EVENT_LOCATION_MOM = 'event_location_mom'

    # PBS Event types
    EVENT_TYPE_QUEUEJOB = 'queuejob'
    EVENT_TYPE_RUNJOB = 'runjob'
    EVENT_TYPE_EXECJOB_END = 'execjob_end'

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
                 job: PBSJob
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
            event_type=PBSEvent.EVENT_TYPE_RUNJOB,
            event_location=PBSEvent.EVENT_LOCATION_SERVER
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.job_id = job_id
        self.rtime = rtime,
        self.allocated_nodes = allocated_nodes

class JobEnd(PBSEvent):
    def __init__(self, 
                 timestamp : int,
                 job_id: int,
                 etime: int,
                 mom_name: str
                ):
        super().__init__(
            timestamp=timestamp,
            event_type=PBSEvent.EVENT_TYPE_EXECJOB_END, 
            event_location=PBSEvent.EVENT_LOCATION_MOM
        )
        self.description = self.description + ':' + self.__class__.__name__
        self.job_id = job_id
        self.etime = etime
        self.mom_name = mom_name

class PBSState(State):
    def __init__(self, timestamp: int, node_list: list[PBSVNode], job_list: list[PBSJob]):
        super().__init__(timestamp, node_list, job_list)
        self.resource_utilization = 0.0
        
        # Cold start preperation
        for job in job_list:
            if job.rtime is not -1:
                self.running_jobs.append(job.id)
            else:
                self.queued_jobs.append(job.id)