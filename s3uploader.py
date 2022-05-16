import boto3
import os, sys
from time import gmtime, strftime
import shutil
import subprocess
from pathlib import Path

print("Select Configure SSO on initial setup. Once the the profile is configured, choose option 2 and enter the profile name you configured on initial setup.")
choice = input("Choose: 1 = Configure SSO | 2 = Login with Profile: ")

if choice == "1":
  sso_config = ["aws", "configure", "sso"]
  sso_config = " ".join(sso_config)
  result = subprocess.run(sso_config)
else:
  profile_name = input("Enter profile name to login as: ")
  sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
  sso_login = " ".join(sso_login)
  result = subprocess.run(sso_login)

TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-internal-upload'
PARENT_FOLDER = Path("D://data")
    
cob_p = PARENT_FOLDER / "cobwebs"
media_p = PARENT_FOLDER / "social-media"
adid_p = PARENT_FOLDER / "adid"
arch_p = PARENT_FOLDER / "archive"

cob_p.mkdir(parents=True, exist_ok=True)     
media_p.mkdir(parents=True, exist_ok=True)
adid_p.mkdir(parents=True, exist_ok=True)    
arch_p.mkdir(parents=True, exist_ok=True)

RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27) ")

for dir_p in [cob_p, adid_p, media_p]:
  bucket_dir = dir_p.name
  for path in dir_p.glob("*.csv"):  # path is cob/filename.csv
  
    # append RFI_num and date to the original file name
    new_filename = (path.stem+"_"+RFI_num+"_"+TIMENOW+".csv")  
  
    # Send file w/ RFI_num & date to S3 
    dest = bucket_root + "/" + bucket_dir + "/" + new_filename   
    cmd = ["aws", "s3", "cp", str(path), str(dest), "--profile", f"{profile_name}", "--region", "us-gov-west-1"]
    cmd = " ".join(cmd)
    result = subprocess.run(cmd)
  
    if not result.returncode:
      print("Upload Successful!")
      # Move file to archive folder once successfull upload to S3
      shutil.move(path, arch_p / new_filename)
    else:
      print("Error running:  ", cmd)
      # sys.exit(-1)  # ?