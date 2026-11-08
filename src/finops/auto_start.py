import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def auto_start_instances_stopped_by_bot(region_name='ap-southeast-1'):
    """
    Scans for and starts EC2 instances that were previously stopped by FinOpsBot.
    Designed to be imported and executed by main.py.
    """
    logging.info(f"Starting to scan for instances stopped by FinOpsBot in {region_name}...")
    print(f"[INFO] Scanning for stopped instances by FinOpsBot in {region_name}...")

    try:
        ec2: EC2Client = boto3.client('ec2', region_name=region_name)
        
        # Server-side filtering to optimize performance
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['stopped']},
                {'Name': 'tag:StoppedBy', 'Values': ['FinOpsBot']}
            ]
        )
        
        instances_found = False

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances_found = True
                instance_id = instance.get("InstanceId")

                # 1. Start the instance
                ec2.start_instances(InstanceIds=[instance_id])

                # 2. Remove the 'StoppedBy' tag to prevent duplicate processing later
                ec2.delete_tags(
                    Resources=[instance_id],
                    Tags=[{'Key': 'StoppedBy'}]
                )

                success_msg = f"Successfully turned on {instance_id} and removed 'StoppedBy' tag."
                logging.info(success_msg)
                print(f"[SUCCESS] {success_msg}")

        if not instances_found:
            logging.info("No instances found that were stopped by FinOpsBot.")
            print("[INFO] No instances found that were stopped by FinOpsBot.")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response['Error']['Message']}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
        
    except Exception as e:
        logging.error(f"System Error: {e}")
        print(f"[ERROR] System Error: {e}")

# This block is only for local manual testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    auto_start_instances_stopped_by_bot()