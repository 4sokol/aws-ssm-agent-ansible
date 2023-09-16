# aws-ssm-agent-ansible

The goal is to automatically deploy the AWS Systems Manager (SSM) Agent on a mix of Windows and Linux EC2 instances using Ansible.

1. Inventory file (file name 'hosts')
This file lists all the EC2 instances you want to manage with Ansible. In this inventory, you should include information about the instance type, IP address, OS type (Windows or Linux), and SSH keys if applicable. For Windows instances, you may need additional information such as the username used for WinRM.
There are different ways how to structure the instances info, IP or DNS could be used. Official link: https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
By default, inventory file is located in /etc/ansible/hosts

2. Ansible Playbook (file 'ssm-agent.yml')
This Playbook performs the following steps:

- Determine the OS of the instance (RHEL, SLES, CentOS, Debian, Ubuntu).
- Check if the SSM Agent is already installed.
- Install the SSM Agent if it's not installed (using package managers: yum, apt, zypper).

This playbook does the following:

For Linux instances, it checks the OS distribution and whether the SSM Agent is already installed using the ssm-agent status command. If not installed, it installs the SSM Agent.
For Windows instances, it checks if the SSM Agent is already installed using Get-Service, and if not installed, it installs the SSM Agent.

3. Run the Playbook (from the instance with installed 'ansible' package): use the command 'ansible-playbook' to execute the playbook against the inventory file, e.g:

ansible-playbook ssm-agent.yml -i /etc/ansible/hosts

4. Q&A
- Question: is that possible to automatically recognize all hosts & OS on all the EC2 instances which exist in Public Cloud Environment?

Answer: Recognizing the Hosts and operating systems on all EC2 instances without specifying it in the inventory file can be a bit challenging because Ansible generally relies on the information available in the inventory to determine how to communicate with and manage the hosts.
However, there is an option to use Dynamic Inventory (https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html). Dynamic Inventory could be achieved in 2 ways: additional Plugin or Inventory Scripts (in Python most often).
Basically, inventory Script retrieves the instance information directly from AWS and then sets the appropriate OS information as host variables in the inventory. This script can determine the OS based on instance names, tags, or any other criteria you define.

Here is an example of what a dynamic inventory script might look like (Python with the boto3 library for AWS) (file 'dynamic_inventory.py')
