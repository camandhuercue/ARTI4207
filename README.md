# ARTI4207 - PoC

El objetivo de la siguiente documentación es dar una guia paso a paso de la creación de la PoC de la segunda entrega del proyecto de ARTI4207.

Para esta PoC utilizaremos la siguiente ruta para probar los ASR propuestos. 

![Arquitectura Propuesta para la PoC](https://github.com/camandhuercue/ARTI4207/blob/main/Arquitecturas%20Cloud%20-%20PoC%20-%20AWS.jpeg "Arquitectura propuesta para la PoC")

Los servicios a utilizar son los siguientes:

- AWS Batch
- AWS Fargate
- AWS Elastic Container Registry
- AWS SQS
- AWS Lambda
- AWS DynamoDB
- AWS IAM
- AWS S3

## 1 - Creación de Políticas y Roles

Para el acceso entre servicios y determinar de manera correcta los privilegios de acceso de cada uno, se crearán las siguientes Políticas:

- ARTI4207-ECR: Acceso a crear una nueva imagen en el repositorio.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ecr:PutImage",
            "Resource": "*"
        }
    ]
}
```

- ARTI4207-SQS: Acceso a crear un nuevo mensaje en la cola de SQS.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sqs:SendMessage",
            "Resource": "*"
        }
    ]
}
```

- ARTI4207-S3
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "*"
        }
    ]
}
```

## 2 - Creación de Repositorio en ECR

## 3 - Creaicón de Máquina de Despliegue

## 4 - Creación de SQS

## 5 - Creación de Lambda

## 6 - Creación de Tabla de DynamoDB

## 7 - Creación de Bucket S3
