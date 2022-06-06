import boto3
from botocore.exceptions import ClientError

def get_bucket_lifecycle_of_s3(bucket_name):
   session = boto3.session.Session()
   s3_client = session.client('s3')
   try:
      result = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name,)
   except ClientError as e:
      result = "No Lifecycle"
   except Exception as e:
      raise Exception( "Unexpected error in get_bucket_lifecycle_of_s3 function: " + e.__str__())
   return result

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
  print(bucket.name +" "+str(get_bucket_lifecycle_of_s3(bucket.name)))
