# **gost-s3uploader**
Program to upload files to S3 bucket gost-internal-upload. 

Select ***<font color=veranda>option 1</font>*** if this is your first time running the program. You will configure your SSO and create a profile (***see example config file below***). You will only configure SSO on the initial run. After that you will use ***<font color=veranda>option 2</font>*** to login with that profile. 

## **Initial Setup w/ "aws configure sso"**
1. Enter "1" to configure SSO.
2. Enter the ***<font color=veranda>sso_start_url</font>*** and ***<font color=veranda>sso_region</font>*** information from the ***Example config file***.
3. After you set ***sso_region***, your default browser will pop-up asking you to log in, or if you're already logged in, confirm authorization. 
4. Complete configure sso by entering the remaining information from the example config file.

## **Login w/ "aws sso login --profile"**
1. Enter "2" to login with the profile you configured in the Initial Setup.
2. Enter profile name from the Initial Setup.
3. Your defualt browser will pop-up asking you to log in or confirm authorization.

## **Example config file**
[profile yourProfileName]<br>
**sso_start_url**= https://start.us-gov-home.awsapps.com/directory/gost-smx-com<br>
**sso_region** = us-gov-west-1 ***(If you have multiple accounts you will be prompted to select the appropriate account after sso_region)***<br> 
**sso_account_id** = 501979927634_SSO-GOSTAnalyst ***(Account id will populate when you select the account)***<br>
**sso_role_name** = SSO-GOSTAnalyst ***(Enter role name that is easy to remember and is asw the account)***<br>
**region** = us-gov-west-1<br>
**output** = json<br>

## **Example credentials file**
[SSO-GOSTAnalyst]<br>
**aws_access_key_id**=*your access key*<br>
**aws_secret_access_key**=*your secret key*<br>
**aws_session_token**=*your session token*<br>

## **Requirements**<br>
from time import gmtime, strftime<br>
import shutil<br>
import subprocess<br>
from pathlib import Path<br>



