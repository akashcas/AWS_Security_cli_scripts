import os
import json
from subprocess import check_output
import boto
from boto import iam
import boto3

environment=["prod","dev"]
for env in environment:
	cmd="aws iam list-users --profile " +env+" > list_user.json"
	os.system("echo'' > list_user.json")
	os.system(cmd)
	fp = open("list_user.json", "r")
	obj = json.load(fp)
	fp.close()
	a=len(obj["Users"])
	username=[]
	for x in range(a):
		number =len(obj["Users"][x])
		if number == 6 :
			user=obj["Users"][x]["UserName"]
			username.append(user)
	if env == 'prod':
		connection=iam.IAMConnection(profile_name="prod")
		session = boto3.Session(profile_name="prod")
	else:
		from boto import iam
		connection=iam.IAMConnection(profile_name="dev")
		session = boto3.Session(profile_name="dev")
	iam = session.client('iam')
	print"\nUser with MFA Disabled on "+env+" AWS account:"
	for user in username:
		try:
		    response = iam.get_login_profile(UserName=user)
		    mfaDevices = connection.get_all_mfa_devices(user)
		    if not mfaDevices.mfa_devices:
	    		print user
		except Exception, e:
		    if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
		    	pass
