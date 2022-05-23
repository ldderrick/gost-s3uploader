from time import gmtime, strftime
import shutil
import subprocess
from pathlib import Path


PARENT_FOLDER = Path("C://data")
#cob_p = PARENT_FOLDER / "cobwebs"
media_p = PARENT_FOLDER / "social-media"
adid_p = PARENT_FOLDER / "adid"
arch_p = PARENT_FOLDER / "archive"

#cob_p.mkdir(parents=True, exist_ok=True)     
media_p.mkdir(parents=True, exist_ok=True)
adid_p.mkdir(parents=True, exist_ok=True)    
arch_p.mkdir(parents=True, exist_ok=True)

TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-internal-upload'

choice = input("Configure SSO (1) | Login (2): ")

if choice == "1":
    sso_config = ["aws", "configure", "sso"]
    sso_config = " ".join(sso_config)
    result = subprocess.run(sso_config)
    profile_name = input("Enter profile name to login as: ")
    sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
    sso_login = " ".join(sso_login)
    result = subprocess.run(sso_login)
else:
    profile_name = input("Enter profile name to login as: ")
    sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
    sso_login = " ".join(sso_login)
    result = subprocess.run(sso_login)

print("Directories have been created in C:\\\\data. Drop your CSV in the appropriate folder for upload.")
input("Press enter to continue... ")
RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27): ")
RFI_num = "RFI" + RFI_num

for dir_p in [adid_p, media_p]:
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
      print(f"{new_filename} moved to archive.")
    else:
      print("Error running:  ", cmd)
      # sys.exit(-1)  # ?