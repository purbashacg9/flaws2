"""
This file contains utility functions used in the scripts in this folder 
"""
import boto3 
import ipaddress
import json
import os 


def get_aws_ips(aws_ips_filename:str) -> object: 
    """
    Given a file with a list of AWS IP addresses , return the IPv4 address ranges belonging to AWS. 
    NOTE - This method is for getting AWS IP addresses from the file available at 
    https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
    :param aws_ips_filename: str: filename of the file containing the AWS IP ranges 
    :return: list: Returns list of IP address ranges belonging to all Amazon services   
    """
    filename = os.path.join('.', aws_ips_filename)
    with open(filename) as aws_ips_file:
        ip_data = json.load(aws_ips_file) 
    
    # Get the IPV4 prefixes
    ip_prefixes = ip_data.get('prefixes')

    # As specified here - https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-download
    # Specify AMAZON to get all IP address ranges. 
    all_aws_ip_addresses = [prefix.get('ip_prefix') for prefix in ip_prefixes if prefix.get('service')=='AMAZON']
    return all_aws_ip_addresses


def check_ip_address(aws_addresses: object, ip_address_to_check: str) -> bool:
    """
    Description: Given a list of IP address ranges beloging to AWS, this function checks if the given ip address belongs to AWS. 
    :param aws_addresses:list: List of IP Address CIDR ranges belonging to AWS
    :param ip_address_to_check:str: IP address 
    :return:bool: True if ip_address_to_check belongs to range of AWS IP addresses. 
    """
    for aws_address in aws_addresses:
        if ipaddress.ip_address(ip_address_to_check) in ipaddress.ip_network(aws_address): 
            return True
    return False 

def get_permissions_for_role(aws_profile: str, role_name: str) -> object:
    """
    Description: Given a role name and a AWS profile, find the AWS services permitted to assume that role.  
    :param aws_profile: str: AWS profile name
    :param role_name: str: Role name in the ARN of the event 
    :return: list: Return names of AWS services allowed to assume the role specified under role_name  
    """
    permitted_services = []
    session = boto3.session.Session(profile_name=aws_profile)
    iam = session.client('iam')
    response = iam.get_role(RoleName=role_name)   
    role_policy = response.get('Role').get('AssumeRolePolicyDocument')
    if role_policy: 
        policy_statements = role_policy.get('Statement')
        if policy_statements: 
            permitted_services = [statement.get("Principal").get("Service") for statement in policy_statements 
                                    if statement.get("Action") == "sts:AssumeRole" and statement.get("Effect") == "Allow"
                                ]
    return permitted_services


def get_repository_policy(aws_profile: str, repository: str) -> object:
    """
    Description: Find repository policy for a given docker repository in AWS ECR.  
    :param aws_profile: str: AWS profile name 
    :param repository: str: Name of a repository in ECR  
    :return: list: Return permissions for given repository  
    """
    repository_policy = [] 
    session = boto3.session.Session(profile_name=aws_profile)
    ecr = session.client('ecr')
    response = ecr.get_repository_policy(repositoryName=repository)   
    policy_text = json.loads(response.get('policyText'))
    if policy_text:
        policy_statements = policy_text.get('Statement')
        if policy_statements: 
            repository_policy = [policy.get('Principal') for policy in policy_statements]
    return repository_policy
