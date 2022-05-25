from time import gmtime, strftime
import subprocess
from pathlib import Path
import os

PARENT_FOLDER = Path("C://dev")
USER_PROFILE = Path.home()
TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-dev-cell'
gost_dev = PARENT_FOLDER / "gost-dev-cell"
gost_dev.mkdir(parents=True, exist_ok=True)
arch_p = PARENT_FOLDER / "archive"  
arch_p.mkdir(parents=True, exist_ok=True)
aws = USER_PROFILE / '.aws'
aws.mkdir(parents=True, exist_ok=True)

file_path = f'{USER_PROFILE}\\.aws\\config'
if os.path.exists(file_path):
    print('Config file already exists')
else:
    # create a file
    with open(file_path, 'w') as fp:
        # uncomment if you want empty file
        fp.write('[profile dev]\n')
        fp.write('sso_start_url = https://start.us-gov-home.awsapps.com/directory/gost-smx-com\n')
        fp.write('sso_region = us-gov-west-1\n')
        fp.write('sso_account_id = 033426607440\n')
        fp.write('sso_role_name = SSO_GOSTAnalyst_dt\n')
        fp.write('region = us-gov-west-1\n')
        fp.write('output = json\n')

print("Directories have been created in C:\\\\dev. Drop your CSV in the appropriate folder for upload.")

# choice = input("Configure SSO (1) | Login (2): ")

# if choice == "1":
#     sso_config = ["aws", "configure", "sso"]
#     sso_config = " ".join(sso_config)
#     result = subprocess.run(sso_config)
#     profile_name = input("Enter profile name to login as: ")
#     sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
#     sso_login = " ".join(sso_login)
#     result = subprocess.run(sso_login)
# else:
profile_name = input("Enter profile name to login as: ")
sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
sso_login = " ".join(sso_login)
result = subprocess.run(sso_login)

RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27): ")
RFI_num = "RFI" + RFI_num

for dir_p in [gost_dev]:
  for path in dir_p.glob("*.csv"): # path is cob/filename.csv
    new_path = str(path).replace(" ", "")
    os.rename(path, new_path)

for dir_p in [gost_dev]:
  bucket_dir = dir_p.name
  for path in dir_p.glob("*.csv"):  # path is cob/filename.csv
    # append RFI_num and date to the original file name
    new_filename = (path.stem+"_"+RFI_num+"_"+TIMENOW+".csv")
    # Send file w/ RFI_num & date to S3 
    dest = bucket_root + "/" + bucket_dir + "/" + new_filename   
    cmd = ["aws", "s3", "cp", str(path), str(dest), "--profile", f"{profile_name}", "--region", "us-gov-west-1", "--debug"]
    cmd = " ".join(cmd)
    result = subprocess.run(cmd)
  
    if not result.returncode:
      print("Upload Successful!")
      # Delete file once successfull upload to S3
      os.remove(path)
      print(f"{path} deleted.")
    else:
      print("Error running:  ", cmd)

input("Press any key to exit.")
      