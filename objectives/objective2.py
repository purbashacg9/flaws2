import argparse 
import boto3
import json


def access_target_account(aws_profile: str) -> None: 
    """
    Access an account through an IAM role
    aws_profile:: str - account whose credentials are not known but can be accessed using another IAM role
    return: None 
    """
    try:
        session = boto3.session.Session(profile_name=aws_profile)
        sts = session.client('sts')
        response = sts.get_caller_identity()
        account = response.get('Account')
        formatted_response = json.dumps(response, indent=4, sort_keys=True)
        print(f'Account details {formatted_response}')

        # View buckets in Target account 
        s3 = session.resource('s3')
        print(f'Buckets in AWS account {account}')
        for bucket in s3.buckets.all(): 
            print(f'Bucket Name : {bucket.name}')
    except Exception as e:  
        print(e)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", required=True, help="AWS credentials profile to use")
    args = vars(parser.parse_args())
    profile = args.get('profile')
    access_target_account(profile)