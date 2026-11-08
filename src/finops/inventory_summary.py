import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def inventory_summary(region_name='ap-southeast-1'):
    """
    Provides a quick summary count of all EC2 instances, 
    grouped by running and stopped states.
    Designed to be imported and executed by main.py.
    """
    logging.info(f"Starting inventory summary check in {region_name}...")
    print(f"[INFO] Starting inventory summary check in {region_name}...")

    try:
        ec2: EC2Client = boto3.client('ec2', region_name=region_name)
        
        total_instances = 0
        running_instances = 0
        stopped_instances = 0

        response = ec2.describe_instances()
        
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                total_instances += 1
                state = instance.get("State", {}).get("Name")
                
                if state == 'running':
                    running_instances += 1
                elif state == 'stopped':
                    stopped_instances += 1
                # Other states like 'pending', 'shutting-down', 'terminated' are counted in total but not running/stopped

        summary_msg = f"Total instances: {total_instances} | Running: {running_instances} | Stopped: {stopped_instances}"
        logging.info(summary_msg)
        print(f"[SUCCESS] {summary_msg}")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response.get('Error', {}).get('Message', str(e))}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
        
    except Exception as e:
        logging.error(f"System Error: {e}")
        print(f"[ERROR] System Error: {e}")

# This block is only for local manual testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    inventory_summary()