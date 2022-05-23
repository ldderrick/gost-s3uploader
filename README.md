# **gost-s3uploader**

If this is your first time running the program, enter 1 to configure SSO and create a profile (***see example config file below***). You will only configure SSO on the initial run. Afterwards, enter 2 to login with that profile.<br>

If you want to check your upload, click on the link below. You will only be able to access the 'gost-internal-upload' bucket and read objects in the bucket.<br>

**s3://gost-internal-upload**: https://console.amazonaws-us-gov.com/s3/buckets/gost-internal-upload?region=us-gov-west-1<br>

## **Example config file**
[profile yourProfileName]<br>
**sso_start_url**= https://start.us-gov-home.awsapps.com/directory/gost-smx-com<br>
**sso_region** = us-gov-west-1 ***(You will be prompted to select an account, if you have multiple.)***<br> 
**sso_account_id** = 501979927634_SSO-GOSTAnalyst ***(Account id will populate when you select the account)***<br>
**sso_role_name** = SSO-GOSTAnalyst ***(Enter role name that is easy to remember and is asw the account)***<br>
**region** = us-gov-west-1<br>
**output** = json<br>

## **Initial Setup w/ "aws configure sso"**
1. Enter "1"  to configure SSO.
2. Enter the ***sso_start_url*** and ***sso_region*** information from the ***Example config file***.
3. After you set ***sso_region***, your default browser will pop-up asking you to log in, or if you're already logged in, confirm authorization. 
4. Complete configure sso by entering the remaining information from the example config file.

## **Login w/ "aws sso login --profile"**
1. Enter "2" to login with the profile you configured in the Initial Setup.
2. Enter profile name from the Initial Setup.
3. Your defualt browser will pop-up asking you to log in or confirm authorization.









