import logging
from mypy_boto3_ec2 import EC2Client
import boto3

logging.basicConfig(
    filename = "auditor_check.log",
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def tag_auditor():
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')
    print("Scanning the system")

    response = ec2.describe_instances()
    #Because the response nested, so we take infor deeper
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance.get("InstanceId")
            #Flagged
            has_owner = False
            #A loop to find the existance of "owner" tags
            for tags in instance.get("Tags", []):
               if tags.get("Key") == "Owner":
                   has_owner = True
                   break
            #If the instance dont have owner tags, logging into the file
            if (has_owner == False):
                logging.warning(f"WARNING: instance: {instance_id} don't have owner tag")
if __name__ == "__main__":
    tag_auditor()