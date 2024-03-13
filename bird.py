import paramiko
import time
import ansible.inventory.manager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor

# Configuration (modify as needed)
INVENTORY_PATH = '/local/auto.inventory'
TARGET_FILE = '/local/node_info'
CHECK_INTERVAL = 5  # Seconds

# Load Ansible inventory
loader = DataLoader()
inventory = ansible.inventory.manager.InventoryManager(loader=loader, sources=[INVENTORY_PATH])
worker_hosts = inventory.get_groups_dict()['workernodes']
print(worker_hosts)

# Create a simple playbook
playbook = [
    {'hosts': 'workernodes',
     'tasks': [
         {'name': 'Check for file existence',
          'stat': {
              'path': TARGET_FILE
          },
          'register': 'file_check'
         }
     ]
    }
]

# Run the playbook using Ansible Playbook Executor
pbex = PlaybookExecutor(playbooks=playbook, inventory=inventory)
results = pbex.run()

# Analyze results
all_hosts_have_file = True
for host, result in results.stats.items():
    if not result['ok'] or not result['changed'] or not result['ansible_facts']['file_check']['stat']['exists']:
        print(f"Host {host} does not have the file {TARGET_FILE}")
        all_hosts_have_file = False
        break  # You can stop checking if one host fails

if all_hosts_have_file:
    print(f"All hosts in group {TARGET_FILE} have the file {TARGET_FILE}")