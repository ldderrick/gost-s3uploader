from time import gmtime, strftime
import subprocess
from pathlib import Path
import os

PARENT_FOLDER = Path("C://data")
USER_PROFILE = Path.home()
TIMENOW=strftime("%Y%m%d",gmtime())
bucket_root='s3://gost-internal-upload'

ais = PARENT_FOLDER / "ais"
ais.mkdir(parents=True, exist_ok=True) 
media = PARENT_FOLDER / "social-media"
media.mkdir(parents=True, exist_ok=True)
adid = PARENT_FOLDER / "adid"
adid.mkdir(parents=True, exist_ok=True) 
aws = USER_PROFILE / '.aws'
aws.mkdir(parents=True, exist_ok=True)
carbon = PARENT_FOLDER / "carbon_reach"
carbon.mkdir(parents=True, exist_ok=True)
gdelt = PARENT_FOLDER / "gdelt"
gdelt.mkdir(parents=True, exist_ok=True)
hotspot = PARENT_FOLDER / "hotpsot"
hotspot.mkdir(parents=True, exist_ok=True)
genius = PARENT_FOLDER / "import_genius"
genius.mkdir(parents=True, exist_ok=True)
pulse = PARENT_FOLDER / "pulse"
pulse.mkdir(parents=True, exist_ok=True)
sayari = PARENT_FOLDER / "sayari"
sayari.mkdir(parents=True, exist_ok=True)
sm = PARENT_FOLDER / "social_media"
sm.mkdir(parents=True, exist_ok=True)
wind = PARENT_FOLDER / "windward"
wind.mkdir(parents=True, exist_ok=True)
acled = PARENT_FOLDER / "acled"
acled.mkdir(parents=True, exist_ok=True)
gost_dev = PARENT_FOLDER / "gost-dev-cell"
gost_dev.mkdir(parents=True, exist_ok=True)

file_path = f'{USER_PROFILE}\\.aws\\config'
if os.path.exists(file_path):
    print('Config file already exists')
else:
    with open(file_path, 'w') as fp:
        # writing config file with GOSTAnalyst role and ID. Only allows PUT to S3.
        fp.write('[profile analyst]\n')
        fp.write('sso_start_url = https://start.us-gov-home.awsapps.com/directory/gost-smx-com\n')
        fp.write('sso_region = us-gov-west-1\n')
        fp.write('sso_account_id = 501979927634\n')
        fp.write('sso_role_name = SSO-GOSTAnalyst\n')
        fp.write('region = us-gov-west-1\n')
        fp.write('output = json\n')

profile_name = input("Enter profile name to login as: ")
sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
sso_login = " ".join(sso_login)
result = subprocess.run(sso_login)

print("Drop your CSV in the appropriate folder for upload in C\\\\data.")

RFI_num = input("What is the RFI Number? (e.g. RFI 00027, Enter 27): ")
RFI_num = "RFI" + RFI_num

for dir_p in [gost_dev, acled, carbon, gdelt, hotspot, genius, pulse, sayari, sm, wind]:
  for path in dir_p.glob("*.csv"): # path is cob/filename.csv
    new_path = str(path).replace(" ", "_")
    os.rename(path, new_path)

for dir_p in [gost_dev, acled, carbon, gdelt, hotspot, genius, pulse, sayari, sm, wind]:
  bucket_dir = dir_p.name
  for path in dir_p.glob("*.csv"): # path is cob/filename.csv
    # append RFI_num and date to the original file name
    new_filename = (path.stem+"_"+RFI_num+"_"+TIMENOW+".csv")
    # Send file w/ RFI_num & date to S3 
    dest = bucket_root + "/" + bucket_dir + "/" + new_filename 
    cmd = ["aws", "s3", "cp", str(path), str(dest), "--profile", f"{profile_name}", "--region", "us-gov-west-1", "--debug"]
    cmd = " ".join(cmd)
    result = subprocess.run(cmd)
  
    if not result.returncode:
      print("Upload Successful!")
      # Local file is deleted after successful upload.
      os.remove(path)
      print(f"{path} deleted.")
    else:
      print("Error running:  ", cmd)
      

input("Press any key to exit.")