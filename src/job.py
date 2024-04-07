class Job:
    def __init__(self, 
                 id, 
                 nodes,
                 ppn,
                 walltime,
                 exec_path,
                 qtime,
                 rtime = -1,
                 pbs_state = 'Q'

                 ):
        self.id       = id
        self.exec_path = exec_path
        self.ppn    = ppn
        self.nodes = nodes
        self.walltime   = walltime
        self.qtime = qtime,
        self.rtime = rtime,
        self.pbs_state = pbs_state