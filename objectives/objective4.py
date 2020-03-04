import argparse 
import json
import pandas as pd 
from utils import check_ip_address
from utils import get_permissions_for_role
from utils import get_aws_ips

def identify_credential_theft(input_file: str, aws_profile: str, event_name: str = None) -> None: 
    """
    Description: This function looks through the events in a CloudTrail event log and identifies events caused using stolen credentials. 
    :param input_file: str: file containing CloudTrail logs 
    :param aws_profile: str: account whose credentials are not known but can be accessed using another IAM role
    :param event_name: str: CloudTrail event type, if provided only logs for this event type are going to be analyzed. 
    :return: None 
    """
    data_to_process = pd.read_csv(input_file)
    if event_name:
        data_to_process = data_to_process[data_to_process['eventName']==event_name]

    # For credential theft, we only look at events not originating from AWS's own services. 
    data_to_process = data_to_process[data_to_process['userIdentityType'] != 'AWSService']

    data_to_process = data_to_process[(data_to_process['userIdentityType'] != 'AWSAccount') & 
                                        (data_to_process['userIdentityAccountId'] != 'ANONYMOUS_PRINCIPAL')]

    all_aws_ip_addresses = get_aws_ips('ip-ranges.json')

    suspected_credential_theft = []   
    for index, row in data_to_process.iterrows(): 
        # Only look at events with userIdentityType AssumedRole as described here 
        # https://netflixtechblog.com/netflix-cloud-security-detecting-credential-compromise-in-aws-9493d6fd373a. 
        if row['userIdentityType'] == 'AssumedRole': 
            # Extract role name from USerIdentity.arn. 
            # NOTE - The ARN format for user identities of type AssumedRoles is 
            # arn:aws:sts::653711331788:assumed-role/level3/d190d14a-2404-45d6-9113-4eda22d7f2c7
            role = row['userIdentityArn'].split(':')
            role_name = role[-1].split("/")[1]
            permitted_services = get_permissions_for_role(aws_profile, role_name)

            is_aws_ip = check_ip_address(all_aws_ip_addresses, row['sourceIPAddress'])

            for service in permitted_services:
                if 'amazonaws.com' in service and not is_aws_ip:
                    suspected_credential_theft.append((row['sourceIPAddress'], role_name))      
    
    if suspected_credential_theft:
        for theft in suspected_credential_theft:
            print(f'Suspected credential theft from IP Address {theft[0]} using role {theft[1]} for {event_name if event_name else "multiple events in log"}')
    else:
        print(f'No credential thefts identified  in  CloudTrail logs for {event_name if event_name else "multiple events in log"}')        
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify crdential theft from CloudTrail logs')
    parser.add_argument("-i", "--input_file", required=True, help="input file containing Cloudtrail logs")
    parser.add_argument("-p", "--profile", required=True, help="AWS credentials profile to use")
    parser.add_argument("-e", "--event", required=False, help="Event name as captured by CloudTrail. If absent, all events in log are scanned")
    
    args = vars(parser.parse_args())
    input_file = args.get('input_file')
    profile = args.get('profile')
    event_name = args.get('event')
    
    identify_credential_theft(input_file, profile, event_name)    