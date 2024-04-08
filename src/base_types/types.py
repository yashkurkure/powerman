class Node:
    def __init__(self, id, name, cpus, online):
        self.id       = id
        self.name     = name
        self.cpus    = cpus
        self.online    = online

class Job:
    def __init__(self, 
                 id, 
                 nodes : int,
                 ppn: int,
                 walltime: int,
                 exec_path,
                 qtime : int,
                 rtime : int = -1,
                 etime : int = -1,
                 allocated_nodes = None
                 ):
        self.id       = id
        self.exec_path = exec_path
        self.ppn    = ppn
        self.nodes = nodes
        self.walltime   = walltime
        self.qtime = qtime,
        self.rtime = rtime,
        self.etime = etime,
        self.allocated_nodes = allocated_nodes

class Event:
    def __init__(self, timestamp: int, event_type, description):
        self.event_type = event_type
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
        return f"Event Type: {self.type}\nDescription: {self.description}"
    
class State:
    def __init__(self, timestamp: int, node_list : list[Node], job_list : list[Job]):
        self.timestamp = timestamp
        self.node_list = node_list
        self.job_list = job_list
        self.queued_jobs = []
        self.running_jobs = []
        self.completed_jobs = []
        self._job_dict : dict[int, Job] = {}
        for job in job_list:
            self._job_dict[job.id] = job

    def get_job_obj(self, job_id):
        return self._job_dict[job_id]

    def get_jobs_on_node(self, node_id):
        query_result = {}
        for job_id in self.running_jobs:
            nodes = self.get_nodes_for_job(job_id)
            if node_id in nodes:
                query_result[job_id] = nodes[node_id]
        return query_result

    def get_nodes_for_job(self, job_id):
        if job_id in self.running_jobs:
            return self.get_job_obj(job_id).allocated_nodes
