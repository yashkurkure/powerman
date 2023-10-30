"""Creates a cluster with 1 login node, 1 head node and N worker nodes in a lan.
All nodes run Ubuntu 20.04 with OpenPBS 23.06.06.

Instructions:
Wait for the experiment to start, and then log into node0 [head node] to manage cluster.
To login as a user of the cluster, log into node1 [login node] as user0.
"""


# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Variable number of nodes.
pc.defineParameter("workerNodeCount", "Number of Worker Nodes", portal.ParameterType.INTEGER, 1,
                   longDescription="Specify atleast 1 worker node")

# Pick your OS.
imageList = [('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04')]

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList,
                   longDescription="Using Ubuntu 20.04")

# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Optional physical node type",
                   portal.ParameterType.STRING, "",
                   longDescription="Specify a single physical node type (pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")

# Optionally create XEN VMs instead of allocating bare metal nodes.
pc.defineParameter("useVMs",  "Use XEN VMs",
                   portal.ParameterType.BOOLEAN, False,
                   longDescription="Create XEN VMs instead of allocating bare metal nodes.")

# Optionally start X11 VNC server.
pc.defineParameter("startVNC",  "Start X11 VNC on your nodes",
                   portal.ParameterType.BOOLEAN, False,
                   longDescription="Start X11 VNC server on your nodes. There will be " +
                   "a menu option in the node context menu to start a browser based VNC " +
                   "client. Works really well, give it a try!")

# Optional link speed, normally the resource mapper will choose for you based on node availability
pc.defineParameter("linkSpeed", "Link Speed",portal.ParameterType.INTEGER, 0,
                   [(0,"Any"),(100000,"100Mb/s"),(1000000,"1Gb/s"),(10000000,"10Gb/s"),(25000000,"25Gb/s"),(100000000,"100Gb/s")],
                   advanced=True,
                   longDescription="A specific link speed to use for your lan. Normally the resource " +
                   "mapper will choose for you based on node availability and the optional physical type.")
                   
# For very large lans you might to tell the resource mapper to override the bandwidth constraints
# and treat it a "best-effort"
pc.defineParameter("bestEffort",  "Best Effort", portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="For very large lans, you might get an error saying 'not enough bandwidth.' " +
                    "This options tells the resource mapper to ignore bandwidth and assume you know what you " +
                    "are doing, just give me the lan I ask for (if enough nodes are available).")
                    
# Sometimes you want all of nodes on the same switch, Note that this option can make it impossible
# for your experiment to map.
pc.defineParameter("sameSwitch",  "No Interswitch Links", portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="Sometimes you want all the nodes connected to the same switch. " +
                    "This option will ask the resource mapper to do that, although it might make " +
                    "it imppossible to find a solution. Do not use this unless you are sure you need it!")

# Optional ephemeral blockstore
pc.defineParameter("tempFileSystemSize", "Temporary Filesystem Size",
                   portal.ParameterType.INTEGER, 0,advanced=True,
                   longDescription="The size in GB of a temporary file system to mount on each of your " +
                   "nodes. Temporary means that they are deleted when your experiment is terminated. " +
                   "The images provided by the system have small root partitions, so use this option " +
                   "if you expect you will need more space to build your software packages or store " +
                   "temporary files.")
                   
# Instead of a size, ask for all available space. 
pc.defineParameter("tempFileSystemMax",  "Temp Filesystem Max Space",
                    portal.ParameterType.BOOLEAN, False,
                    advanced=True,
                    longDescription="Instead of specifying a size for your temporary filesystem, " +
                    "check this box to allocate all available disk space. Leave the size above as zero.")

pc.defineParameter("tempFileSystemMount", "Temporary Filesystem Mount Point",
                   portal.ParameterType.STRING,"/mydata",advanced=True,
                   longDescription="Mount the temporary file system at this mount point; in general you " +
                   "you do not need to change this, but we provide the option just in case your software " +
                   "is finicky.")

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()


# Check parameter validity.
if params.workerNodeCount < 1:
    pc.reportError(portal.ParameterError("You must choose at least 1 worker node.", ["workerNodeCount"]))

wokrerNodeCount = params.workerNodeCount
loginNodeCount = 1
headNodeCount = 1
nodeCount = wokrerNodeCount + loginNodeCount + headNodeCount

if params.tempFileSystemSize < 0 or params.tempFileSystemSize > 200:
    pc.reportError(portal.ParameterError("Please specify a size greater then zero and " +
                                         "less then 200GB", ["tempFileSystemSize"]))

if params.phystype != "":
    tokens = params.phystype.split(",")
    if len(tokens) != 1:
        pc.reportError(portal.ParameterError("Only a single type is allowed", ["phystype"]))

pc.verifyParameters()

# Create link/lan.
lan = request.LAN()

# LAN paremeters
if params.bestEffort:
        lan.best_effort = True
elif params.linkSpeed > 0:
    lan.bandwidth = params.linkSpeed
if params.sameSwitch:
    lan.setNoInterSwitchLinks()

head_nodes = [0]
head_nodes_i = []
login_nodes = [1]
login_nodes_i = []
worker_nodes = [i for i in range(2, nodeCount)]
worker_nodes_i = []
# Process nodes, adding to lan.
for i in range(nodeCount):
       
    # Setup head node
    if i in head_nodes:
        name = "head"
        if params.useVMs:
            node = request.XenVM(name + '_vm')
        else:
            node = request.RawPC(name)

        head_nodes_i.append(node)
        # Install a private/public key
        node.installRootKeys(True, True)

        # Install OpenPBS Server
        node.addService(rspec.Execute(shell="bash", command="/local/repository/cloudlab/openPBS/install-ubuntu-server.sh"))
        pass

    # Setup login node
    if i in login_nodes:
        name = "login"
        if params.useVMs:
            node = request.XenVM(name + '_vm')
        else:
            node = request.RawPC(name)
        login_nodes_i.append(node)

        # Install public key of head node
        node.installRootKeys(False, True)

        # Install OpenPBS Client
        node.addService(rspec.Execute(shell="bash", command="/local/repository/cloudlab/openPBS/install-ubuntu-client.sh"))
        pass

    # Setup worker node
    if i in worker_nodes:
        name = "node" + str(i-2)
        if params.useVMs:
            node = request.XenVM(name + '_vm')
        else:
            node = request.RawPC(name)
        worker_nodes_i.append(node)

        # Install public key of head node
        node.installRootKeys(False, True)
        
        # Install OpenPBS MOM
        node.addService(rspec.Execute(shell="bash", command="/local/repository/cloudlab/openPBS/install-ubuntu-compute.sh"))
        pass


    if params.osImage and params.osImage != "default":
        node.disk_image = params.osImage
        pass
    
    # Add to lan
    iface = node.addInterface("eth1")
    lan.addInterface(iface)

    # Optional hardware type.
    if params.phystype != "":
        node.hardware_type = params.phystype
        pass
    
    # Optional Blockstore
    if params.tempFileSystemSize > 0 or params.tempFileSystemMax:
        bs = node.Blockstore(name + "-bs", params.tempFileSystemMount)
        if params.tempFileSystemMax:
            bs.size = "0GB"
        else:
            bs.size = str(params.tempFileSystemSize) + "GB"
            pass
        bs.placement = "any"
        pass
    #
    # Install and start X11 VNC. Calling this informs the Portal that you want a VNC
    # option in the node context menu to create a browser VNC client.
    #
    # If you prefer to start the VNC server yourself (on port 5901) then add nostart=True. 
    #
    if params.startVNC:
        node.startVNC()
        pass
    pass

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)