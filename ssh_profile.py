"""An example demonstrating how to control the installation of an ssh
private and public pair for the root user such that root can ssh without a
password to other nodes in your experiment. 

Instructions:
When you experiment starts, login to `node1` and then do: `sudo ssh root@node2`
Notice though, that you cannot login from `node2` to `node1` as root since the
private key is not installed on node2.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
# Create two raw "PC" nodes
node1 = request.RawPC("node1")
node2 = request.RawPC("node2")

# Install a private/public key on node1
node1.installRootKeys(True, True)
# One node2, just the public key
node2.installRootKeys(False, True) 

# Or disable all keys on all nodes.
#request.disableRootKeys()

# Create interfaces for each node.
iface1 = node1.addInterface("if1")
iface2 = node2.addInterface("if2")

# Create a link with the type of LAN.
link = request.LAN("link")

# Add both node interfaces to the link.
link.addInterface(iface1)
link.addInterface(iface2)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)