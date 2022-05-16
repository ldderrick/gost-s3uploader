import boto3
from botocore.exceptions import ClientError
import os, sys
import shutil
from pathlib import Path
from time import gmtime, strftime
import subprocess
from subprocess import Popen, PIPE
import logging
import botocore.session

print("Configure SSO needs to be run on initial setup. Once the the profile is configured, choose option 2 and enter the profile name you configured on initial setup.")
choice = input("Choose: 1 = Configure SSO | 2 = Login with Profile: ")

if choice == 1:
  sso_config = ["aws", "configure", "sso"]
  sso_config = " ".join(sso_config)
  result = subprocess.run(sso_config)
else:
  profile_name = input("Enter profile name to login as: ")
  sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
  sso_login = " ".join(sso_login)
  result = subprocess.run(sso_login)

TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-dev-cell'
PARENT_FOLDER = Path("C://dev")
    
gost_dev = PARENT_FOLDER / "gost-dev-cell"
gost_dev.mkdir(parents=True, exist_ok=True)
arch_p = PARENT_FOLDER / "archive"  
arch_p.mkdir(parents=True, exist_ok=True)

RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27) ")

for dir_p in [gost_dev]:
  bucket_dir = dir_p.name
  for path in dir_p.glob("*.csv"):  # path is cob/filename.csv
    print(path)
    # append RFI_num and date to the original file name
    new_filename = (path.stem+"_"+RFI_num+"_"+TIMENOW+".csv")
    print(new_filename)  
  
    # Send file w/ RFI_num & date to S3 
    key = bucket_dir + "/" + new_filename
    #print(key)
    dest = bucket_root + "/" + new_filename   
    #print(dest)
    #cmd = ["aws", "s3", "cp", path, dest]
    # abs_path = os.path.abspath(new_filename)
    # print(abs_path)
    cmd = ["aws", "s3", "cp", str(path), str(dest), "--profile", f"{profile_name}", "--region", "us-gov-west-1"]
    #result = subprocess.run(cmd)
    #cmd2 = f"aws s3api put-object --bucket gost-internal-upload --key {key} --body {path}"
    cmd = " ".join(cmd)
    result = subprocess.run(cmd)
  
    if not result.returncode:
      # Move file to archive folder once successfull upload to S3
      print("Upload Successful!")
      shutil.move(path, arch_p / new_filename)
    else:
      print("Error running:  ", cmd)
      #sys.exit(-1)  # ?




