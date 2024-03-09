import paramiko
import time
import ansible.inventory.manager
from ansible.parsing.dataloader import DataLoader

# Configuration (modify as needed)
INVENTORY_PATH = '/local/auto.inventory'
TARGET_FILE = '/local/node_info'
CHECK_INTERVAL = 5  # Seconds

# Load Ansible inventory
loader = DataLoader()
inventory = ansible.inventory.manager.InventoryManager(loader=loader, sources=[INVENTORY_PATH])
worker_hosts = inventory.get_groups_dict()['workernodes']
print(worker_hosts)

# def check_file_exists(host):
#     """Checks if the target file exists on a remote host."""
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         # Replace with your SSH credentials
#         ssh.connect(host, username='your_username', password='your_password')
#         sftp = ssh.open_sftp()
#         sftp.stat(TARGET_FILE)
#         return True
#     except FileNotFoundError:
#         return False
#     finally:
#         if ssh:
#             ssh.close()

# # Main loop
# while True:
#     all_have_file = True
#     for host in worker_hosts:
#         if not check_file_exists(host):
#             all_have_file = False
#             break  # No need to check other nodes

#     if all_have_file:
#         print("All worker nodes have the file.")
#         break

#     print("Waiting for file... Retrying in", CHECK_INTERVAL, "seconds.")
#     time.sleep(CHECK_INTERVAL)