"""
This script generates an Ansible Inventory file for a cluster on cloudlab.
"""
import argparse
from jinja2 import Template

job_template = """
headnodes:
  hosts:
    localhost:
workernodes:
  hosts:
    node0.testbed.schedulingpower.emulab.net:
    node1.testbed.schedulingpower.emulab.net:
    node2.testbed.schedulingpower.emulab.net:
loginnodes:
  hosts:
    login.testbed.schedulingpower.emulab.net:
all:
  vars:
    ansible_user: root
    ansible_private_key_file: /root/.ssh/id_rsa
    ansible_host_key_checking: False
    numworkernodes: 3
    username: ykurkure
    servercanonicalname: pc557.emulab.net
    serverhostname: head.testbed.schedulingpower.emulab.net
"""
template = Template(job_template)

def generate(args):
    import socket
    hostname = str(socket.gethostname())

    print(f'headnode:')
    print(f'\thosts:')
    print(f'\t\tlocalhost:')
    print(f'workernodes:')
    print(f'\thosts:')
    for i in range(0, args.number_of_worker_nodes):
        print(f'\t\t{hostname.replace('head',f'node{i}')}:')
    print(f'loginnodes:')
    for i in range(0, args.number_of_worker_nodes):
        print(f'\t\t{hostname.replace('head',f'login{i}')}:')
    print(f'all:')
    print(f'\tvars:')
    print(f'\t\tansible_user: root')
    print(f'\t\tansible_private_key_file: /root/.ssh/id_rsa')
    print(f'\t\tansible_host_key_checking: False')
    print(f'\t\tnumworkernodes: {args.number_of_worker_nodes}')
    print(f'\t\tserverhostname: {hostname}')

    pass


def parse_args():
    """
    Parse the args.
    """

    print("----Args----")
    parser = argparse.ArgumentParser(description="Argument Parser")

    parser.add_argument("-nln", "--number_of_login_nodes", type=int, default=1,
                        help="Number of login nodes(default: 1)")
    parser.add_argument("-nwn", "--number_of_worker_nodes", type=int, default=1,
                        help="Number of worker nodes (default: 1)")
    parser.add_argument("-sshu", "--ssh_users", type=str, default=None,
                        help="Path to file with a list of usernames")
    args = parser.parse_args()
    print("Number of login nodes:", args.number_of_login_nodes)
    print("Number of worker nodes:", args.number_of_worker_nodes)
    print("SSH Users file:", args.ssh_users)
    print("----Args----")
    return args

if __name__ == "__main__":
    args = parse_args()
    generate(args)