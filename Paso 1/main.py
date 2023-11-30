import urllib.request
import csv
from AWS_UTILS import aws_utils
import os
import json
import time

COUNT = 100
#urllib.request.urlretrieve("https://raw.githubusercontent.com/camandhuercue/ARTI4207/main/DATASET.csv", "DATASET.csv")
urllib.request.urlretrieve("https://www.datos.gov.co/resource/uzcf-b9dh.csv?audience=public&type=dataset", "DATASET.csv")
BUCKET = ''
SQS_URL = ''
SODA = 'https://www.datos.gov.co/resource/{}.csv'

start_time = time.time()
with open('DATASET.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    utils = aws_utils()

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            ID = row[0]
            OWNER = row[3]
            NAME = row[2]
            EMAIL = row[22]
            CATEGORY = row[10]
            line_count += 1
            urllib.request.urlretrieve(SODA.format(ID), ID + '.csv')
            utils.s3_upload(ID + '.csv', BUCKET, ID + '/' + ID + '.csv')
            os.remove(ID + '.csv')
            message = {'ID': ID, 'OWNER': OWNER, 'NAME': NAME, 'EMAIL': EMAIL, 'CATEGORY': CATEGORY}
            MESSAGE = json.dumps(message)
            #print(MESSAGE)
            utils.sqs_publish(SQS_URL, MESSAGE)
        if line_count == (COUNT + 1):
            break

    print(f'Processed {line_count - 1} lines.')
    print("--- %s seconds ---" % (time.time() - start_time))
