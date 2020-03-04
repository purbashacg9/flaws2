# Purpose 
The purpose of this project is to build a set of scripts to accomplish scenarios described in the objectives in the defender track of [flaws2.cloud](http://flaws2.cloud/) game. The game involves a sequence of objectives in an information security scenario in AWS, but those objectives include common tasks that are relevant for data engineers as well. 

Each script takes in command line arguments to make it usable with different parameters (e.g. buckets, roles names).


# Setup 
1. Create a virtual environment in the location where you want to run the scripts 
``` python -m venv flaws2 ```

2. Install dependencies given in requirements. txt 
``` pip install -r requirements.txt ``` 

3. Set up credentials for the 'Security' account and Target accounts in your local AWS configuration and credentials files. These are available in the [objective 1](http://flaws2.cloud/defender.htm) and [objective 2](http://flaws2.cloud/defender2.htm) of the defender track. 

# Running scripts 
Each python file in the objectives folder accomplishes the tasks given in the Defender track in the flaws2.cloud 
training game. EAch file also accepts command line arguments that can be viewed by typing -h after the program like so 
python3 objectives/objective1.py -h 

1. Objective 1 - Download CloudTrail Logs  
``` 
python3 objectives/objective1.py
usage: objective1.py [-h] -p PROFILE -b BUCKET -d LOCAL_DIR 
```
Example command - `python3 objectives/objective1.py -p security -b flaws2-logs -d logs `

2. Objective 2 - Access the target account 
```
python3 objectives/objective2.py -h
usage: objective2.py [-h] -p PROFILE
```

3. Objective 3 - Use jq
```
python3 objectives/objective3.py
usage: objective3.py [-h] -d LOCAL_DIR -f FILE_FORMAT -o OUTPUT_FILE
```  
- LOCAL_DIR: location where logs are stored  
- FILE_FORMAT: format of logs to combine  
- OUTPUT_FILE: File name for the combined file  

Example command - ` python3 objectives/objective3.py -d logs -f .json.gz -o output-Mar4.csv `

4. Objective 4 - Identify credential theft 
```
python3 objectives/objective4.py
usage: objective4.py [-h] -i INPUT_FILE -p PROFILE [-e EVENT] 
``` 
Example Command - ` python3 objectives/objective4.py -i output-full.csv -e ListBuckets -p target_security `

5. Objective 5 - Identify the public resource 
```
python3 objectives/objective5.py
usage: objective5.py [-h] -i INPUT_FILE -p PROFILE -e EVENT
``` 
Example Command - ` python3 objectives/objective5.py -i output-Mar4.csv -e ListImages -p target_security `





