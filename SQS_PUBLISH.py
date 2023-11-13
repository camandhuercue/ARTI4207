import boto3
client = boto3.client('sqs', region_name='us-east-1')
response = client.send_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/661717879436/ARTI4207-SQS', MessageBody='{"Mensaje": "Pruebas"}')
print(response)
