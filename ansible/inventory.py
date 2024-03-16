"""
This script generates an Ansible Inventory file for a cluster on cloudlab.
"""
import argparse



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