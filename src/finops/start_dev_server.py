import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def hunt_and_start_dev_servers(region_name='ap-southeast-1'):
    """
    Scans for stopped EC2 instances with the 'Environment: dev' tag
    and automatically starts them.
    Designed to be imported and executed by main.py.
    """
    logging.info(f"Scanning for stopped 'dev' instances in {region_name}...")
    print(f"[INFO] 1. Scanning AWS System in {region_name} for stopped 'dev' instances...")
    
    try:
        ec2_client: EC2Client = boto3.client('ec2', region_name=region_name)
        
        # Optimization: Using Server-side filtering instead of Client-side loops
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['stopped']},
                {'Name': 'tag:Environment', 'Values': ['dev']}
            ]
        )
        
        target_instances = [] # A list which represents instances that need to be started

        # Extract instance IDs from the filtered response
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance.get("InstanceId")
                target_instances.append(instance_id)
                
                msg = f"Detected stopped dev instance: {instance_id}"
                logging.warning(msg)
                print(f"  [WARNING] {msg}")

        print("-" * 50)
        
        # Send start command if any instances are found
        if target_instances:
            print(f"[INFO] 2. Action decided: Turning on {len(target_instances)} instances.")
            logging.info(f"Sending start signal to {len(target_instances)} dev instances.")
            
            ec2_client.start_instances(InstanceIds=target_instances)
            
            success_msg = f"Sent start signal to dev instances: {target_instances}"
            logging.info(success_msg)
            print(f"[SUCCESS] {success_msg}")
        else:
            ok_msg = "System optimal. No stopped dev instances found."
            logging.info(ok_msg)
            print(f"[SUCCESS] {ok_msg}")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response.get('Error', {}).get('Message', str(e))}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
        
    except Exception as e:
        logging.error(f"System Error: {e}")
        print(f"[ERROR] System Error: {e}")

# This block allows the script to be tested standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hunt_and_start_dev_servers()