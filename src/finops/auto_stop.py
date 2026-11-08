import boto3
import logging
import argparse
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def auto_stop_instance_dry_run(instance_id, is_dry_run, region_name='ap-southeast-1'):
    """
    Attempts to stop an EC2 instance, optionally using DryRun to check IAM permissions.
    Designed to be imported and executed by main.py, or run standalone.
    """
    ec2: EC2Client = boto3.client('ec2', region_name=region_name)

    logging.info(f"Initiating stop sequence for {instance_id} in {region_name}. DryRun: {is_dry_run}")
    print(f"[INFO] Initiating stop sequence for {instance_id}. DryRun: {is_dry_run}")

    try:
        response = ec2.stop_instances(
            InstanceIds=[instance_id],
            DryRun=is_dry_run
        )
        
        # If DryRun is False and the API call succeeds, the code execution reaches here
        success_msg = f"Successfully stopped instance: {instance_id}"
        logging.info(success_msg)
        print(f"[SUCCESS] {success_msg}")

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')

        # AWS returns 'DryRunOperation' if the user has permissions but DryRun was True
        if error_code == 'DryRunOperation':
            msg = f"DryRun successful! You have sufficient IAM permissions to stop instance: {instance_id}"
            logging.info(msg)
            print(f"[SUCCESS] {msg}")
            
        elif error_code == "UnauthorizedOperation":
            msg = f"Failed! You do not have sufficient IAM permissions to stop instance: {instance_id}"
            logging.error(msg)
            print(f"[ERROR] {msg}")
            
        else:
            msg = f"AWS API Error: {e.response.get('Error', {}).get('Message', str(e))}"
            logging.error(msg)
            print(f"[ERROR] {msg}")
            
    except Exception as e:
        logging.error(f"System Error: {e}")
        print(f"[ERROR] System Error: {e}")

# This block is for standalone execution and local testing
if __name__ == "__main__":
    # Local testing logging configuration
    logging.basicConfig(level=logging.INFO)
    
    # Initiate parser to read arguments from CLI
    parser = argparse.ArgumentParser(description="Script to Stop EC2 Instance with DryRun capability")

    # Define --dry-run flag. action='store_true' means if flag is present, it evaluates to True.
    parser.add_argument('--dry-run', action='store_true', help="Enable DryRun to check permissions without stopping")
    
    # Parser for instance-id from CLI to make it more flexible
    parser.add_argument('--instance-id', required=True, help="Target EC2 Instance ID") 

    # Parse all arguments entered by the user
    args = parser.parse_args()

    # Call the function with parsed arguments
    auto_stop_instance_dry_run(args.instance_id, args.dry_run)