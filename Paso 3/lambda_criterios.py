import json

def lambda_handler(event, context):
    # TODO implement
    if event:
        for record in event['Records']:
            print("ID: " + record['Sns']['Message'])
