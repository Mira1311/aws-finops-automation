import boto3
from mypy_boto3_ec2 import EC2Client
import logging
from botocore.exceptions import ClientError
import argparse

logging.basicConfig(
    filename='auto_stop_testing.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)
def auto_stop_instance_dry_run(instance_id, is_dry_run):
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')

    try:
        response = ec2.stop_instances(
            InstanceIds=[instance_id],
            DryRun=is_dry_run
        )
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')

        if error_code == 'DryRunOperation':
            logging.info(f"Successfully! You have enough IAM permission to stop that instances: {instance_id}")
        elif error_code == "UnauthorizedOperation":
            logging.error(f"Failed! You dont have enough IAM permission to stop that instance.")
        else:
            logging.info(f"Error: {e}")

if __name__ == "__main__":
    #Initiate parser to read argument from CLI
    parser = argparse.ArgumentParser(description="Script Stop EC2 Instance")

    #Define --dry-run flags
    # Action= 'store-true' here meant if have this flag, args.dry_run = True, w/o it will be False
    parser.add_argument('--dry-run', action='store_true')

    #parser for instance-id from CLI to make it more flexible
    parser.add_argument('--instance-id', required = True) 

    #Parse all arguments which entered by user/dev
    args = parser.parse_args()

    #Call the function with all the parser take from CLI
    auto_stop_instance_dry_run(args.instance_id, args.dry_run)   