from time import gmtime, strftime
import subprocess
from pathlib import Path
import os
import glob


def make_dirs():
    global imagery_download, imagery_upload
    aws = USER_PROFILE / '.aws'
    aws.mkdir(parents=True, exist_ok=True)
    imagery_upload = PARENT_FOLDER / 'imagery-uploads'
    imagery_upload.mkdir(parents=True, exist_ok=True)
    imagery_download =  PARENT_FOLDER / 'imagery-downloads'
    imagery_download.mkdir(parents=True, exist_ok=True)

def aws_config_file():
    file_path = f'{USER_PROFILE}\\.aws\\config'
    if os.path.exists(file_path):
        with open(file_path) as fp:
            if 'sso_role_name = SSO-GOSTAnalyst' in fp.read():
                print('Analyst profile found')
            else:
                with open(file_path, 'a') as fp:
                    # writing config file with GOSTAnalyst role and ID. Only allows PUT to S3.
                    fp.write('\n[profile analyst]\n')
                    fp.write('sso_start_url = https://start.us-gov-home.awsapps.com/directory/gost-smx-com\n')
                    fp.write('sso_region = us-gov-west-1\n')
                    fp.write('sso_account_id = 501979927634\n')
                    fp.write('sso_role_name = SSO-GOSTAnalyst\n')
                    fp.write('region = us-gov-west-1\n')
                    fp.write('output = json\n')
    else:
        print("Creating config file...")
        with open(file_path, 'w') as fp:
            # writing config file with GOSTAnalyst role and ID. Only allows PUT to S3.
            fp.write('[profile analyst]\n')
            fp.write('sso_start_url = https://start.us-gov-home.awsapps.com/directory/gost-smx-com\n')
            fp.write('sso_region = us-gov-west-1\n')
            fp.write('sso_account_id = 501979927634\n')
            fp.write('sso_role_name = SSO-GOSTAnalyst\n')
            fp.write('region = us-gov-west-1\n')
            fp.write('output = json\n')

def list_bucket():
    list_cmd = ["aws", "s3", "ls", f"{bucket_root}", "--profile", f"{profile_name}"]
    result = subprocess.run(list_cmd)

    if not result.returncode:
        print(result)
    else:
        print("Error running list command: " + str(result.returncode))
        
def send_to_s3():
    for dir_p in [imagery_upload]:
        #bucket_dir = dir_p.name
        for path in dir_p.glob("*.zip"): # path is cob/filename.csv
            # append RFI_num and date to the original file name
            new_filename = (path.stem+".zip")
            # Send file w/ RFI_num & date to S3 
            dest = bucket_root + "/" + new_filename #+ bucket_dir + "/"
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

def download_images():
    file_to_dload = input("\nEnter file name to download: ")
    source = f's3://gost-prod-imint/{file_to_dload}'
    
    dload_cmd = ["aws", "s3", "cp", str(source), f"{imagery_download}", "--profile", f"{profile_name}", "--region", "us-gov-west-1", "--debug"]
    result = subprocess.run(dload_cmd)

    if not result.returncode:
        print("\nDownload Successful!\n")
    else:
        print("\nError downloading file\n", str(result.returncode))

if __name__ == '__main__':
    PARENT_FOLDER = Path("C://s3-imagery")
    USER_PROFILE = Path.home()
    TIMENOW=strftime("%Y-%m-%d",gmtime())
    bucket_root='s3://gost-prod-imint'

    make_dirs()
    aws_config_file()

    profile_name = "analyst" 
    sso_login = ["aws", "sso", "login", "--profile", f"{profile_name}"]
    result = subprocess.run(sso_login)

    print("\nDirectories have been created in C:\\\\s3-imagery. Drop your files in the UPLOAD folder before proceeding.\n")

    print("Select option 1, 2, 3 or q...")
    print('1 = List Files in Bucket')
    print('2 = Upload Image')
    print('3 = Download Image')
    print('q = Quit')

    while True:
        option = input('\nEnter option...\n')
        if option == '1':
            list_bucket()
        elif option == '2':
            # rfs = input("\nWhat is the RFS Number? (e.g. RFS 00027, Enter 27): \n")
            # RFS_num = "RFS" + rfs
            send_to_s3()
        elif option == '3':
            download_images()
        elif option == 'q':
            break
        else:
            print("\nInvalid option. Choose an option from the list.")
            print('1 = List Files in Bucket')
            print('2 = Upload Image')
            print('3 = Download Image')
            print('q = Quit')


    

 