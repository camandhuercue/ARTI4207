import boto3

class aws_utils:
    def s3_upload(self, path, bucket, dest):
        s3 = boto3.client('s3')
        s3.upload_file(path, bucket, dest)

    def sqs_publish(self, url, message):
        client = boto3.client('sqs', region_name='us-east-1')
        response = client.send_message(QueueUrl=url, MessageBody=message)
        print(response)
