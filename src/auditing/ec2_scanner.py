import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def scan_ec2_instances(region_name='ap-southeast-1'):
    """
    Hàm quét và kiểm kê toàn bộ EC2 Instances.
    Đã được thiết kế để nhận lệnh từ main.py.
    """
    logging.info(f"Connecting to AWS (Region: {region_name}) to scan EC2 instances...")
    print(f"🔍 1. Connecting to AWS (Region: {region_name})...")
    
    try:
        # Initiate client to talk with EC2 service
        ec2_client: EC2Client = boto3.client('ec2', region_name=region_name)
        
        print("📥 2. Getting response from EC2...")
        response = ec2_client.describe_instances()
        
        print("-" * 60)
        count = 0
        
        # AWS data back have 2 layers of data
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                
                # Get data by dictionary skills
                instance_id = instance.get("InstanceId", "N/A")
                public_ip = instance.get("PublicIpAddress", "No public ip")
                state = instance.get("State", {}).get("Name", "N/A")
                
                # Print to the screen and logging the datas
                msg = f"Found EC2! | ID: {instance_id} | State: {state.upper()} | IPv4: {public_ip}"
                logging.info(msg)
                print(f"✅ {msg}")
                
                count += 1
                
        print("-" * 60)
        summary_msg = f"Total EC2 Instances calculated: {count}"
        logging.info(summary_msg)
        print(f" {summary_msg}")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response['Error']['Message']}"
        logging.error(error_msg)
        print(f" {error_msg}")
        
    except Exception as e:
        logging.error(f"System error: {e}")
        print(f" System error: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scan_ec2_instances()