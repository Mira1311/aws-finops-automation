import boto3
from mypy_boto3_ec2 import EC2Client
import logging

logging.basicConfig(
    filename='cost_check.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)

PRICING = {'t2.micro': 0.0116, 't3.micro': 0.0104} #USD/h
def calculate_price():
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')
    total_t2_micro_instances = 1 #Just for test, because I used free AWS so i only have t3.micro instances!
    total_t3_micro_instances = 0 

    response = ec2.describe_instances()

    for reservation in response.get("Reservations",[]):
        for instance in reservation.get("Instances",[]):
            if instance.get("InstanceType") == "t2.micro":
                total_t2_micro_instances +=1
            elif instance.get("InstanceType") == "t3.micro":
                total_t3_micro_instances +=1

    price_t2_micro = total_t2_micro_instances * PRICING['t2.micro']
    price_t3_micro = total_t3_micro_instances * PRICING['t3.micro']
    total = price_t2_micro + price_t3_micro
    logging.info(f"Turned off {total_t2_micro_instances} t2.micro, {total_t3_micro_instances} t3.micro, estimated saved cost: ${total}/night ")

if __name__ == "__main__":
    calculate_price()
        