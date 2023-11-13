import boto3
s3 = boto3.client('s3')
s3.upload_file('pruebas.txt', 'arti4207-g6-pruebas', 'Algo/pruebas.txt')
