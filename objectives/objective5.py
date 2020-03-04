import argparse 
import pandas as pd 
from utils import get_repository_policy 

def identify_public_resources(input_file: str, aws_profile: str, event_name: str = None) -> object: 
    """
    Description: This function looks through the events in a CloudTrail event log and identifies resources that are public
    :param input_file: str: file containing CloudTrail logs 
    :param aws_profile: str: account whose credentials are not known but can be accessed using another IAM role
    :param event_name: str: CloudTrail event type, if provided only logs for this event type are going to be analyzed. 
    :return: list: List of public resources 
    """
    public_resources, repositories = [], [] 
    data_to_process = pd.read_csv(input_file)
    # Filter data frame by event provided 
    data_to_process = data_to_process[data_to_process['eventName']==event_name]

    # find out repository Names 
    repositories = data_to_process['requestParametersRepositoryName'].dropna().to_list()
    for repository in repositories:
        repository_policy = get_repository_policy(aws_profile, repository)
        if repository_policy: 
            for policy in repository_policy:
                if policy == '*': 
                    public_resources.append(repository)

    return public_resources            
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify public resources in AWS environment')
    parser.add_argument("-i", "--input_file", required=True, help="input file containing Cloudtrail logs")
    parser.add_argument("-p", "--profile", required=True, help="AWS credentials profile to use")
    parser.add_argument("-e", "--event", required=True, help="Event name as captured by CloudTrail.")
    
    args = vars(parser.parse_args())
    input_file = args.get('input_file')
    profile = args.get('profile')
    event_name = args.get('event')
    
    public_resources = identify_public_resources(input_file, profile, event_name)    
    if public_resources: 
        for resource in public_resources:
            print(f'ECR repository {resource} is public')
    else:
        print('No public resources found')        
