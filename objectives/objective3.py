import argparse
import pandas as pd 
import os 

def combine_files(local_dir: str, file_format: str, output_file: str) -> None: 
    """
    Description: Reads all files (recursively) in 'local_dir' with format matching 'file_format', combines the files into a CSV.   
    Name of the CSV file is taken from output_file argument. 
    NOTE - Objective3 uses jq for command line parsing. I used pandas to combine the files and extract the columns shown in Objective3. 
    I also save the generated file as CSV in the current folder. 
    :param local_dir: str: Directory containing the files to be combined. This is a relative path from the directory where the script is running. 
    :param file_format: str: Only files of this type are combined for processing
    return: None
    """
    if not os.path.isdir(os.path.join('.',local_dir)): 
        print(f'No matching directory for {local_dir}. Please provide correct directory name and try again.')
        return 
    
    dfs = [] 
    for path, _, files in os.walk(local_dir): 
        for filename in files:
            if filename.endswith(file_format): 
                df = pd.read_json(
                    os.path.join(path,filename), 
                    orient='records', 
                    compression='gzip'
                )
                dfs.append(df)
            else:
                print(f'Skipping file {filename} as it is not in json.gz format') 

    if len(dfs):
        data_for_processing = pd.concat(dfs, ignore_index=True)
        data = [] 
        for _, row in data_for_processing.iterrows():
            desired_data = {}    
            desired_data['eventTime'] = row['Records'].get('eventTime')
            desired_data['sourceIPAddress'] = row['Records'].get('sourceIPAddress')
            desired_data['userIdentityArn'] = row['Records'].get('userIdentity').get('arn')
            desired_data['userIdentityAccountId'] = row['Records'].get('userIdentity').get('accountId')
            desired_data['userIdentityType'] = row['Records'].get('userIdentity').get('type')
            desired_data['eventName'] = row['Records'].get('eventName')
            if row['Records'].get('requestParameters'):
                if row['Records'].get('requestParameters').get('repositoryName'):
                    desired_data['requestParametersRepositoryName'] = row['Records'].get('requestParameters').get('repositoryName')
            data.append(desired_data)

        filtered_data = pd.DataFrame(data=data)
        filtered_data.to_csv(output_file)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine CloudTrail logs and generate a CSV for further analysis')
    parser.add_argument("-d", "--local_dir", required=True, help="Local directory that contains the files downloaded from S3 bucket")
    parser.add_argument("-f", "--file_format", required=True, help="Format of files to combine")
    parser.add_argument("-o", "--output_file", required=True, help="Output file")

    args = vars(parser.parse_args())
    local_dir = args.get('local_dir')
    file_format = args.get('file_format')
    output_file = args.get('output_file')
    
    combine_files(local_dir, file_format, output_file)
