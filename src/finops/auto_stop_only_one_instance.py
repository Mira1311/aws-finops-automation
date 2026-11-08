import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client


logging.basicConfig(
    filename='auto_stop.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)
def manage_ec2_instances(instance_ids, region_name ='ap_southeast-1'):
    #Initiate EC2 instance
    ec2: EC2Client = boto3.client('ec2', region_name=region_name)

    try:
        logging.info(f"sending stop signal to instance: {instance_ids}")
        ec2.stop_instances(InstanceIds=instance_ids)
        print("Successfully!")

    except ClientError as e:
        error_code = e.response['Error']['Code']

        if error_code in ['UnauthorizedOperation', 'AccessDenied']:
            logging.error("Error: Server or User is not have IAM roles to execute this task.")
            
        else:
            logging.error(f"Error from AWS API: {e.response['Error']['Message']}")

    except Exception as e:
        logging.error(f"System error or connection: {e}")

if __name__ == "__main__":
    manage_ec2_instances(['i-051ecf9e1058c4295'])