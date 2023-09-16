#!/usr/bin/env python

import boto3

# Initialize the AWS client
ec2 = boto3.client('ec2')

# Fetch EC2 instances with specific tags
response = ec2.describe_instances(
    Filters=[
        {'Name': 'tag:Environment', 'Values': ['Production']},
        # Add more filters as needed
    ]
)

# Initialize an empty inventory
inventory = {
    'all': {
        'children': {
            'linux': {
                'hosts': []
            },
            'windows': {
                'hosts': []
            }
        }
    }
}

# Loop through instances and categorize them by OS
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        os = instance.get('Tags', {}).get('OS', 'Unknown')
        if os.lower() == 'linux':
            inventory['all']['children']['linux']['hosts'].append(instance['PrivateIpAddress'])
        elif os.lower() == 'windows':
            inventory['all']['children']['windows']['hosts'].append(instance['PrivateIpAddress'])

# Print the inventory in JSON format
import json
print(json.dumps(inventory))
