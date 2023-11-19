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
			"Action": [
				"ecr:CompleteLayerUpload",
				"ecr:GetAuthorizationToken",
				"ecr:UploadLayerPart",
				"ecr:InitiateLayerUpload",
				"ecr:BatchCheckLayerAvailability",
				"ecr:PutImage"
			],
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

- ARTI4207-S3: Con esta política podemos leer y crear objetos en los buckets de S3
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

**NOTA** Tener presente que es recomendable especificar los recursos a los que la política tendrá permisos, para no dejarlos a todos (*)

Ahora se procede a crear los roles que se asignarán a los distintos servicios a utilizar, con esto brindamos los accesos necesarios para su utilziación. Para lograr este objetivo crearemos los siguientes roles:

- ARTI4207-EC2: Este rol se asignará a la máquina de EC2 que utilicemos para desplegar el contenedor en el repositorio de AWS. Se asigna la política ARTI4207-ECR:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
- ARTI4207-ECS: Este rol se asignará a los recursos de Fargate que se utilizarán para correr los Jobs de AWS Batch y permitirá al contenedor acceder a SQS y S3 con las políticas ARTI4207-SQS y ARTI4207-S3:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "ecs-tasks.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

## 2 - Creación de Repositorio en ECR

Para crear un nuevo repositorio, en la consola de AWS buscamos "Elastic Container Registry" > Repositories > Create repository. El repositorio lo crearemos "Privado" y como nombre ponemos "arti4207-repo". Con la creación del nuevo repositorio podemos obtener la URI en la cual alojaremos la imagen de docker que se desplegará en el proceso Batch. La URI es parecida a la que se observa a continuación.

{id}.dkr.ecr.us-east-1.amazonaws.com/arti4207-repo

Esta URI la utilizaremos en los pasos posteriores.

## 3 - Creación de SQS

Para crear una cola, en la consola de AWS buscamos el servicio SQS, una vez allí damos click en "Create queue". Como opciones ponemos lo siguiente:

- Nombre: ARTI4207-SQS
- Tipo: standar
- Deshabilitamos el cifrado (Esto es para la PoC por lo que no hay necesidad de utilizar el cifrado)

Una vez creada la cola, copiamos la URL asignada, ya que la utilizaremos posteriormente. Un ejemplo se observa a continación:

https://sqs.us-east-1.amazonaws.com/{ID}/ARTI4207-SQS

## 4 - Creación de Bucket S3

En la consola de AWS, buscamos el servicio de S3 y creamos un nuevo bucket. Para nuestro caso, se crea uno llamado "arti4207-poc-2023", dejamos el restante de opciones por defecto.

## 5 - Creaicón de Máquina de Despliegue

Con la finalidad de poder crear la imagen de docker que utilizaremos para descargar los datos y almecenarlos en S3 y notificar porteriormente a la cola de SQS, se necesita una instancia donde crearemos la imagen y la subiremos al repositorio creado anteriormente. Para esto, nos dirigimos al servicio de EC2 en la consola de AWS y creamos una nueva instancia con las siguientes características:

- Tipo de máquina: t2.medium
- OS: Ubuntu.
- EBS: 10GB
- IAM instance profile: ARTI4207-EC2
- Se debe de considerar el acceso desde redes de internet y las llaver para acceso por SSH.

Posterior a la creación de la nueva instancia, procedemos a instalar Docker en el OS. Para esto seguimos el proceso indicado en el sitio oficial de Docker (https://docs.docker.com/engine/install/ubuntu/).

Una vez instalado el servicio en el sistema operativo procedemos a descargar del presente git los archivos ubicados en la carpeta "Paso 1" donde encontraremos:

- Dockerfile: Este archivo nos ayudará a crear la imagen de Docker con base Debian y copiando los archivos Python necesarios para descargar los dataset usando SODA API.
- main.py: Este archivo contiene la lógica para descargar los dataset desde SODA API del MINTIC.
- AWS_UTILS.py: Este archivo contiene el uso del SDK de AWS para utilizar los servicios de S3 y SQS.

A continuación mostramos los comandos para la creación de 

```
git clone https://github.com/camandhuercue/ARTI4207.git
cd ARTI4207/Paso\ 1/
```

Modificamos el archivo main.py, específicamente las variables "BUCKET" y "SQS_URL". Un ejemplo se muestra a continuación:

```
BUCKET = 'arti4207-poc-2023'
SQS_URL = 'https://sqs.us-east-1.amazonaws.com/{ID}/ARTI4207-SQS'
```

Posterior a esto, ejecutamos el siguiente comando:

```
sudo docker build . 
```

una vez creada la imagen, procedemos a subirla a AWS ECR con los siguientes comandos:

```
sudo apt-get install awscli -y
aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin {ID}.dkr.ecr.us-east-1.amazonaws.com
```

No debe de generar ningún error. Posterior a esto, procedemos a ekecutar el siguiete comando para extraer el ID de la imagen de docker

```
sudo docker images
```

Con el ID de la imagen, ejecutamos los siguientes comandos:
```
sudo docker tag 120746be79fb {ID}.dkr.ecr.us-east-1.amazonaws.com/arti4207-repo:arti4207_image
sudo docker push {ID}.dkr.ecr.us-east-1.amazonaws.com/arti4207-repo:arti4207_image
```

Una vez finalizado el proceso, nos dirigimos al servicio de ECR y copiamos la URL de la imagen, la utilizaremos posteriormente para la configuraicón de AWS Batch. Un ejemplo se puede observar a continuación:

{ID}.dkr.ecr.us-east-1.amazonaws.com/arti4207-repo:arti4207_image

## 6 - Creación de AWS Batch



## 7 - Creación de Tabla de DynamoDB

## 8 - Creación de Lambda

## 9 - Creación de Tópico
