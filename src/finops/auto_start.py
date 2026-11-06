import boto3
from mypy_boto3_ec2 import EC2Client
import logging
from botocore.exceptions import ClientError

logging.basicConfig(
    filename='auto_start_server_stopped_by_bots.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)

def auto_start_instances_stopped_by_bot():
    ec2: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')
    try:
        response = ec2.describe_instances(
            Filters = [
                {'Name': 'instance-state-name', 'Values': ['stopped']},
                {'Name': 'tag:StoppedBy', 'Values': ['FinOpsBot']}
            ]
        )
        instances_found = False

        for reservation in response.get("Reservations",[]):
            for instance in reservation.get("Instances",[]):
                instances_found=True
                instance_id = instance.get("InstanceId")

                ec2.start_instances(InstanceIds=[instance_id])

                ec2.delete_tags(
                    Resources=[instance_id],
                    Tags=[{'Key': 'StoppedBy'}]
                )

                logging.info(f"Successfully turned on {instance_id} and removed 'StoppedBy' tag")
        if not instances_found:
            logging.info("No instances which was stopped by FinOpsBot")

    except ClientError as e:
        logging.error(f"AWS Error: {e}")
    except Exception as e:
        logging.error(f"System Error: {e}")

if __name__ == "__main__":
    auto_start_instances_stopped_by_bot()
