# Purpose 
The purpose of this project is to build a set of scripts to accomplish scenarios described in the objectives in the defender track of [flaws2.cloud][http://flaws2.cloud/] game. The game involves a sequence of objectives in an information security scenario in AWS, but those objectives include common tasks that are relevant for data engineers as well. 

The program is generalized  so that an end user could use it to discover the same attack if the details (e.g. buckets, roles names) were different.


# Setup 
1. Create a virtual environment in the location where you want to run the scripts 
``` python -m venv flaws2 ```

2. Install dependencies given in requirements. txt 
``` pip install -r requirements.txt ``` 

3. Set up credentials for the 'Security' account and Target accounts in your local AWS configuration and credentials files. These are available in the [objective 1][http://flaws2.cloud/defender.htm] and [objective 2][http://flaws2.cloud/defender2.htm] of the defender track. 

# Running scripts 
Each python file accomplishes the tasks given in the Defender track in the flaws2.cloud 
training game. 



