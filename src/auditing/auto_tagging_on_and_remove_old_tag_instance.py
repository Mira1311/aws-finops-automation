import boto3
from mypy_boto3_ec2 import EC2Client
import logging
from botocore.exceptions import ClientError
from datetime import datetime
logging.basicConfig(
    filename='auto_tagging_turned_on_instances.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S' )

def auto_tagging_on_instances(instance_id):
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')

    try:
        ec2.start_instances(InstanceIds=[instance_id])
        ec2.delete_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'StoppedBy'},
                {'Key': 'StopDate'}
            ]
        )
        ec2.create_tags(
            Resources=[instance_id],
            Tags = [
                {
                    'Key': 'StartedBy',
                    'Value': 'FinOpsBot'
                },
                {
                    'Key': 'StartDate',
                    "Value": current_time
                }
            ]
        )
        logging.info(f"Successfully started and tagged into this {instance_id}.")
    except ClientError as e:
        logging.error(f"Error came from AWS API: {e.response['Error']['Message']}")
    except Exception as e:
        logging.error(f"System error : {e}")

if __name__ == "__main__":
    auto_tagging_on_instances("i-0e01a67ad87b5bf4")