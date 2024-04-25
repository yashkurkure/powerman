"""
This script generates an Ansible Inventory file for a cluster on cloudlab.
"""
import argparse

def generate(args):
    import socket
    hostname = str(socket.gethostname())
    with open(args.gen_path, 'w+') as f:

        #-- Head Nodes --
        f.write(f'headnode:\n')
        f.write(f'  hosts:\n')
        f.write(f'    localhost:\n')
        #-- Worker Nodes --
        f.write(f'workernodes:\n')
        f.write(f'  hosts:\n')
        for i in range(0, args.number_of_worker_nodes):
            node_name = hostname.replace('head',f'node{i}')
            f.write(f'    {node_name}:\n')
        #-- Login Nodes --
        f.write(f'loginnodes:\n')
        f.write(f'  hosts:\n')
        for i in range(0, args.number_of_login_nodes):
            node_name = hostname.replace('head',f'login{i}')
            f.write(f'    {node_name}:\n')
        #-- Data Nodes --
        f.write(f'datanodes:\n')
        f.write(f'  hosts:\n')
        nfs_node_name = hostname.replace('head',f'data')
        f.write(f'    {nfs_node_name}:\n')
        #-- All variables --
        f.write(f'all:\n')
        f.write(f'  vars:\n')
        f.write(f'    ansible_user: root\n')
        f.write(f'    ansible_private_key_file: /root/.ssh/id_rsa\n')
        f.write(f'    ansible_host_key_checking: False\n')
        f.write(f'    numworkernodes: {args.number_of_worker_nodes}\n')
        f.write(f'    serverhostname: {hostname}\n')
        f.write(f'    nfshostname: {nfs_node_name}\n')
        if 'wisc.cloudlab.us' in hostname:
            f.write('    common_user_group: schedulingpower-\n')
        else:
            f.write('    common_user_group: SchedulingPower\n')
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