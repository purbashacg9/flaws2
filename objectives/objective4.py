import argparse 
import boto3 
import ipaddress
import json
import pandas as pd 

def check_ip_address(aws_addresses: object, ip_address_to_check: str) -> bool:
    """
    Given a list of IP address ranges beloging to Amazon, this function checks if the ip address specified in ip_address_to_check 
    belongs to Amazon. 
    aws_addresses::list - List of IP Address CIDR ranges belonging to AWS
    ip_address_to_check::str - IP address 
    return:: bool - True if ip_address_to_check is an AWS address. 
    """
    for aws_address in aws_addresses:
        if ipaddress.ip_address(ip_address_to_check) in ipaddress.ip_network(aws_address): 
            return True
    return False 

def identify_credential_theft(input_file: str, event_name: str = None) -> None: 
    #filename = os.path.join()
    data_to_process = pd.read_csv(input_file)
    #print(data_to_process.shape)
    if event_name:
        data_to_process = data_to_process[data_to_process['eventName']==event_name]
    #print(data_to_process.shape)

    with open('ip-ranges.json') as aws_ips_file:
        ip_data = json.load(aws_ips_file) #pd.read_json('ip-ranges.json', orient='')
    
    ip_prefixes = ip_data.get('prefixes')
    #print(ip_prefixes[0])

    aws_ip_df = pd.DataFrame(data=ip_prefixes, columns=['ip_prefix', 'region', 'service'])
    # print(aws_ip_df.head())
    # print(aws_ip_df.shape)
    # As specified here - https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html#aws-ip-download
    # Specify AMAZON to get all IP address ranges. 
    all_aws_ip_addresses = aws_ip_df[aws_ip_df['service']=='AMAZON'].ip_prefix.to_list()
    # print(all_aws_ip_addresses.head())
    # print(all_aws_ip_addresses.shape)

    suspect_ip_addresses = [] 
    suspect_arns = [] 
    for index, row in data_to_process.iterrows(): 
        # Only look at events with userIdentityType AssumedRole as described here 
        # https://netflixtechblog.com/netflix-cloud-security-detecting-credential-compromise-in-aws-9493d6fd373a. 
        # This also filters out the  valid events originating from AWSService or AWSAccount. 
        if row['userIdentityType'] == 'AssumedRole': 
            suspect_ip_addresses.append(row['sourceIPAddress'])
            
            suspect_arns.append(row['userIdentityArn'])



    print(suspect_arns, suspect_ip_addresses)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Identify crdential theft from CloudTrail logs')
    parser.add_argument("-i", "--input_file", required=True, help="input file containing Cloudtrail logs")
    parser.add_argument("-e", "--event", required=False, 
                            help="This is an event name as captured by CloudTrail. Optional, if not provided, all events in the log are scanned"
                        )

    args = vars(parser.parse_args())
    input_file = args.get('input_file')
    event_name = args.get('event')
    
    identify_credential_theft(input_file, event_name)    