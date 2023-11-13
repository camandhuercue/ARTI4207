import urllib.request
import csv
from AWS_UTILS import aws_utils
import os
import json

urllib.request.urlretrieve("https://raw.githubusercontent.com/camandhuercue/ARTI4207/main/DATASET.csv", "DATASET.csv")
BUCKET = ''
SQS_URL = ''
SODA = 'https://www.datos.gov.co/resource/{}.csv'

with open('DATASET.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    utils = aws_utils()

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            ID = row[0]
            OWNER = row[1]
            NAME = row[2]
            line_count += 1
            urllib.request.urlretrieve(SODA.format(ID), ID + '.csv')
            utils.s3_upload(ID + '.csv', BUCKET, ID + '/' + ID + '.csv')
            os.remove(ID + '.csv')
            message = {'ID': ID, 'OWNER': OWNER, 'NAME': NAME}
            MESSAGE = json.dumps(message)
            utils.sqs_publish(SQS_URL, MESSAGE)

    print(f'Processed {line_count} lines.')
