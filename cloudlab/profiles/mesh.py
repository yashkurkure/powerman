"""A fully connected mesh using multiplexed best effort links. Since most nodes have a small number of
physical interfaces, we must set the links to use vlan ecapsulation over the physical link. On your
nodes, each one of the links will be implemented using a vlan network device. 

Instructions:
Log into your node, use `sudo` to poke around.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Array of nodes
nodes = []

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

pc.defineParameter("N", "Number of nodes",
                   portal.ParameterType.INTEGER, 4)
pc.defineParameter("phystype",  "Optional physical node type (d710, etc)",
                   portal.ParameterType.STRING, "")
params = pc.bindParameters()

# Create all the nodes.
for i in range(0, params.N):
    node = request.RawPC("node%d" % (i + 1))
    if params.phystype != "":
        node.hardware_type = params.phystype
        pass
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD'
    nodes.append(node)
    pass

# Create all the links.
for i in range(0, params.N - 1):
    for j in range(i + 1, params.N):
        nodeA = nodes[i]
        nodeB = nodes[j]

        iface1 = nodeA.addInterface()
        iface2 = nodeB.addInterface()
        link   = request.Link()
        link.addInterface(iface1)
        link.addInterface(iface2)
        link.best_effort = True
        link.link_multiplexing = True
        pass
    pass

pc.printRequestRSpec(request)