import json
import boto3
import sys
import hashlib

BUCKET = "arti4207-poc-2023"
TOPIC = "arn:aws:sns:us-east-1:661717879436:ARTI4207-topico"
DYNAMO = "ARTI4207-Dynamo"

def get_object(bucket, obj):
    client = boto3.client('s3')
    data = client.get_object(Bucket=bucket, Key=obj)

    return data['Body'].read()
    
def publish_topic(topic, message):
    client = boto3.client('sns')
    response = client.publish(TopicArn=topic, Message=message)

def put_item_table(table, item):
    client = boto3.client('dynamodb')
    response = client.put_item(ReturnConsumedCapacity='TOTAL', TableName=table, Item=item)
    print(response)

def lambda_handler(event, context):
    if event:
        batch_item_failures = []
        sqs_batch_response = {}
        print(event["Records"])
        for record in event["Records"]:
            try:
                Object = json.loads(record['body'])
                publish_topic(TOPIC, Object['ID'])
                Bin = get_object(BUCKET, Object['ID'] + "/" + Object['ID'] + ".csv")
                HASH = hashlib.sha256(Bin).hexdigest()
                METADATA = {
                    'HASH': {
                        'S': HASH
                    },
                    'ID':{
                        'S': Object['ID']
                    },
                    'OWNER':{
                        'S': Object['OWNER']
                    },
                    'NAME':{
                        'S': Object['NAME']
                    }
                }
                put_item_table(DYNAMO, METADATA)
                print(METADATA)
            except Exception as e:
                print(str(e))
                batch_item_failures.append({"itemIdentifier": record['messageId']})
        
        sqs_batch_response["batchItemFailures"] = batch_item_failures
        return sqs_batch_response
