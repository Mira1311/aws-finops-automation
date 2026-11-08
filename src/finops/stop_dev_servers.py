import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def hunt_and_stop_dev_servers(region_name='ap-southeast-1'):
    """
    Scans for running EC2 instances with the 'Environment: dev' tag
    and automatically stops them to reduce infrastructure costs.
    Designed to be imported and executed by main.py.
    """
    logging.info(f"Scanning for running 'dev' instances in {region_name}...")
    print(f"[INFO] 1. Scanning AWS System in {region_name} for running 'dev' instances...")
    
    try:
        ec2_client: EC2Client = boto3.client('ec2', region_name=region_name)
        
        # Optimization: Using Server-side filtering instead of Client-side loops
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:Environment', 'Values': ['dev']}
            ]
        )
        
        target_instances = [] # A list which represents instances that need to be stopped

        # Extract instance IDs from the filtered response
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance.get("InstanceId")
                target_instances.append(instance_id)
                
                msg = f"Detected running dev instance incurring costs: {instance_id}"
                logging.warning(msg)
                print(f"  [WARNING] {msg}")

        print("-" * 50)
        
        # Send stop command if any instances are found
        if target_instances:
            print(f"[INFO] 2. Action decided: Turning off {len(target_instances)} instances.")
            logging.info(f"Sending stop signal to {len(target_instances)} dev instances.")
            
            ec2_client.stop_instances(InstanceIds=target_instances)
            
            success_msg = f"Sent stop signal successfully for: {target_instances}"
            logging.info(success_msg)
            print(f"[SUCCESS] {success_msg}")
        else:
            ok_msg = "System optimal. No running dev instances found."
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
    hunt_and_stop_dev_servers()