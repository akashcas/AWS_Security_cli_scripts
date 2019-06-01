import datetime
import dateutil
from dateutil import parser
import boto
environment=['prod','dev']
for env in environment:
	from boto import iam
	conn=iam.connect_to_region('ap-southeast-1',profile_name=env)
	users=conn.get_all_users()
	timeLimit=datetime.datetime.now() - datetime.timedelta(days=90)

	print "----------------------------------------------------------"
	print "Users Having 90 days old IAM keys in "+env+" AWS account:"
	print "----------------------------------------------------------"
	print "\n"
	for user in users.list_users_response.users:
		accessKeys=conn.get_all_access_keys(user_name=user['user_name'])
		for keysCreatedDate in accessKeys.list_access_keys_response.list_access_keys_result.access_key_metadata:
			if (keysCreatedDate['status'] == 'Active'):
				if parser.parse(keysCreatedDate['create_date']).date() <= timeLimit.date():
					print " "+user['user_name']
	print "\n"
