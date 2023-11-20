import json
import boto3
import sys
import hashlib

BUCKET = "arti4207-poc-2023"
TOPIC = "arn:aws:sns:us-east-1:661717879436:ARTI4207-topico"
DYNAMO = ""

def get_object(bucket, obj):
    client = boto3.client('s3')
    data = client.get_object(Bucket=bucket, Key=obj)

    return data['Body'].read()
    
def publish_topic(topic, message):
    client = boto3.client('sns')
    response = client.publish(TopicArn=topic, Message=message)

def lambda_handler(event, context):
    if event:
        batch_item_failures = []
        sqs_batch_response = {}
        for record in event["Records"]:
            try:
                publish_topic(TOPIC, Object['ID'])
                Object =  json.loads(record['body'])
                Bin = get_object(BUCKET, Object['ID'] + "/" + Object['ID'] + ".csv")
                HASH = hashlib.sha256(Bin).hexdigest()
                METADATA = {
                    'HASH': HASH,
                    'ID': Object['ID'],
                    'OWNER': Object['OWNER'],
                    'NAME': Object['NAME']
                }
                print(METADATA)
            except Exception as e:
                print(str(e))
                batch_item_failures.append({"itemIdentifier": record['messageId']})
        
        sqs_batch_response["batchItemFailures"] = batch_item_failures
        return sqs_batch_response
