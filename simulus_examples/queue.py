import simulus
import random as rand
from random import seed, expovariate
seed(123)

def job(idx, node, duration):
    node.acquire()
    print("%g, %g: job(%d) gains access to node" % (sim.now,calc_uti(),idx))
    sim.sleep(duration)
    print("%g, %g: job(%d) releases node" % (sim.now,calc_uti(),idx))
    node.release()

def submit(i, num_resources, duration, queue_resource):
    queue_resource.acquire()
    job_was_run = False
    print("%g, %g: job(%d) submit requesting (%d) nodes" % (sim.now, calc_uti(),i, num_resources))
    avail_nodes = []
    for node in nodes:
        if node.num_in_service() == 0:
            avail_nodes.append(node)
    if len(avail_nodes) >= num_resources:
        print("%g, %g: job(%d) run on (%d) nodes" % (sim.now,calc_uti(),i, num_resources))
        for j in range(0 , num_resources):
            sim.process(job, i, avail_nodes[j], duration)
        job_was_run = True
    queue_resource.release()
    if not job_was_run:
        sim.sleep(1)
        sim.process(submit, i, num_resources, duration, queue_resource)

def user_submit_random(queue_resource):

    for i in range(1, 3):
        sim.sleep(expovariate(1))
        num_nodes_req = rand.randint(7, 10)
        duration = 5
        sim.process(submit, i, num_nodes_req, duration, queue_resource)

def calc_uti():
    avail_nodes = []
    for node in nodes:
        if node.num_in_service() == 0:
            avail_nodes.append(node)
    return len(nodes) - len(avail_nodes)


sim = simulus.simulator()

# 10 Nodes
nodes = [sim.resource(capacity=1) for i in range(0, 10)]
queue_resource = sim.resource(capacity=1)

# Instantiate the process
sim.process(user_submit_random, queue_resource)

# Run for 10 seconds
sim.run(1000)