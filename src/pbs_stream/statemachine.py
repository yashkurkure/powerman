from base_types.statemachine import *
from pbs_stream.types import *

class StreamEvaluator(StateMachine):
    def __init__(self):
        super().__init__()
    
    def evaluate(self, s: PBSState, e: PBSEvent) -> State :
        super().evaluate(s, e)
        if type(e) is JobQueue:
            s.job_list.append(e.job)
            s.job_dict[e.job.id] = e.job
            s.queued_jobs.append(e.job.id)
            pass
        elif type(e) is JobRun:
            s.get_job_obj(e.job_id).rtime = e.rtime
            s.get_job_obj(e.job_id).allocated_nodes = e.allocated_nodes
            s.queued_jobs.remove(e.job_id)
            s.running_jobs.append(e.job_id)
            pass
        
        elif type(e) is JobMoMBegin:
            j = s.get_job_obj(e.job_id)
            s.get_job_obj(e.job_id).allocated_nodes[e.mom_name] = j.ppn

        elif type(e) is JobEnd:
            s.get_job_obj(e.job_id).etime = e.etime
            del s.get_job_obj(e.job_id).allocated_nodes[e.mom_name]

            if len(s.get_job_obj(e.job_id).allocated_nodes) == 0:
                s.running_jobs.remove(e.job_id)
                s.completed_jobs.append(e.job_id)
        
        return s
    
    def evaluate_metrics(self, s: PBSState) -> dict:
        
        # Resource utlization
        cpus_in_use = 0
        for job_id in s.running_jobs:
            cpus_in_use += s.get_job_obj(job_id).cpus
        total_cpus = 0
        for node in s.node_list:
            total_cpus += node.cpus
        
        s.resource_utilization = cpus_in_use/total_cpus
        return {'resource-utilization' : s.resource_utilization}
        
