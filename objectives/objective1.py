import argparse 
import boto3
import os 

def download_logs(aws_profile: str, s3_bucket: str, local_dir:str) -> int:
    """
    Description: Connects to S3 using the given AWS profile and download files from the given bucket 
    :param aws_profile: str: name of AWS profile to use for connecting to AWS. The profile should exist in credentials or config files 
    in the AWS folder
    :param s3_bucket: str: The bucket on S3 containing files to be downloaded  
    :param local_dir: str: Directory where files are downloaded 
    return: int: Number of files downloaded  
    """
    files_downloaded = 0 
    try:
        # Set up a session using the given profile 
        session = boto3.session.Session(profile_name=aws_profile)
        s3 = session.resource('s3')  
        
        # Create an instance of S3 Bucket 
        bucket = s3.Bucket(s3_bucket) 
        objects = bucket.objects.all()

        # create a local directory by the same name as the S3 bucket name to store the downloaded files
        if not os.path.exists(local_dir): 
            os.makedirs(local_dir)
        
        # Download the files in this bucket 
        for obj in objects:
            filename = obj.key.split('/')[-1]
            filepath = os.path.join(local_dir, filename)
            bucket.download_file(obj.key, filepath)
            files_downloaded += 1 
    except Exception as e:  
        print(e)

    return files_downloaded                  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", required=True, help="AWS credentials profile to use")
    parser.add_argument("-b", "--bucket", required=True, help="Name of S3 Bucket")
    parser.add_argument("-d", "--local_dir", required=True, 
                            help="Name of Directory where files will be downloaded. If directory does not exist it will be created"
                        )

    args = vars(parser.parse_args())
    profile = args.get('profile')
    bucket = args.get('bucket')
    directory = args.get('local_dir')
    
    print(f'Number of files downloaded -> {download_logs(profile, bucket, directory)}')
    