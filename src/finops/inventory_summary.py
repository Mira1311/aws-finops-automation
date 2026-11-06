import logging
import boto3
from mypy_boto3_ec2 import EC2Client

logging.basicConfig(
    filename='inventory_summary.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)

def inventory_summary():
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')

    total_instances = 0
    running_instances = 0
    stopped_instances = 0

    response = ec2.describe_instances()
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            total_instances +=1
            if instance.get("State", {}).get("Name") == 'running':
                running_instances +=1
            else:
                stopped_instances +=1

    logging.info(f"All instance: {total_instances} | Running: {running_instances} | Off: {stopped_instances}")

if __name__ == "__main__":
    inventory_summary()