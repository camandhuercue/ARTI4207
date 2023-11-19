FROM debian:latest

WORKDIR /workspace
RUN apt-get update && apt-get install python3-boto3 -y

COPY main.py /workspace/
COPY AWS_UTILS.py /workspace/
