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
    with open(args.gen_path, 'w+') as f:
        f.write(f'headnode:\n')
        f.write(f'\thosts:\n')
        f.write(f'\t\tlocalhost:\n')
        f.write(f'workernodes:\n')
        f.write(f'\thosts:\n')
        for i in range(0, args.number_of_worker_nodes):
            node_name = hostname.replace('head',f'node{i}')
            f.write(f'\t\t{node_name}:\n')
        f.write(f'loginnodes:\n')
        f.write(f'\thosts:\n')
        for i in range(0, args.number_of_login_nodes):
            node_name = hostname.replace('head',f'login{i}')
            f.write(f'\t\t{node_name}:\n')
        f.write(f'all:\n')
        f.write(f'\tvars:\n')
        f.write(f'\t\tansible_user: root\n')
        f.write(f'\t\tansible_private_key_file: /root/.ssh/id_rsa\n')
        f.write(f'\t\tansible_host_key_checking: False\n')
        f.write(f'\t\tnumworkernodes: {args.number_of_worker_nodes}\n')
        f.write(f'\t\tserverhostname: {hostname}\n')
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
    parser.add_argument("-C", "--gen_path", type=str, default="inventory.yml",
                        help="Path to traces (default: 'inventory.yml')")
    # TODO: ssh-users shoulw be passed as --extra-vars to the playbook
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