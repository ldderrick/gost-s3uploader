# **gost-s3uploader**
This program will setup directories for file upload to the S3 gost-internal-upload bucket in the GOST PROD environment.

Select ***option 1*** if this is your first time running the program. You will configure your SSO and create a profile. Once you have configured SSO you can select ***option 2*** to login with the created profile. 

When running option 1 - aws configure sso, you will be<br> prompted to input the SSO configuration information below.

## **Example config file**
[profile yourProfileName]<br>
**sso_start_url**= https://start.us-gov-home.awsapps.com/directory/gost-smx-com<br>
**sso_region** = us-gov-west-1 (If you have multiple accounts you will be prompted to select the appropriate account)<br> 
**sso_account_id** = 033426607440 (Account id will populate when you select the account)<br>
**sso_role_name** = SSO-OperationsAdmin (Enter role name that is easy to remember and is asw the account)<br>
**region** = us-gov-west-1<br>
**output** = json<br>

## **Example credentials file**
[devadmin]<br>
aws_access_key_id=*your access key*<br>
aws_secret_access_key=*your secret key*<br>
aws_session_token=*your session token*

## **Example 

**Dependencies**<br>
Python 3.9<br>
AWS CLIv2

***Requirements***<br>
from time import gmtime, strftime<br>
import shutil<br>
import subprocess<br>
from pathlib import Path<br>



