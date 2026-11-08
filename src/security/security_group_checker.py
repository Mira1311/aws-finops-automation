import boto3
import logging
import argparse
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

def security_check(check_port, region_name='ap-southeast-1'):
    """
    Scans Security Groups to find rules that allow public access (0.0.0.0/0)
    to a specific target port (e.g., port 22 for SSH).
    Designed to be imported and executed by main.py or run standalone.
    """
    logging.info(f"Starting security group scan for open port {check_port} in {region_name}...")
    print(f"[INFO] Scanning Security Groups for public access (0.0.0.0/0) on port {check_port} in {region_name}...")

    try:
        ec2: EC2Client = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_security_groups()
        
        vulnerable_groups = 0

        for sec_group in response.get("SecurityGroups", []):
            group_name = sec_group.get("GroupName")
            group_id = sec_group.get("GroupId")
            
            for ip_permission in sec_group.get("IpPermissions", []):
                # Check if the rule applies to our target port
                if ip_permission.get("FromPort") == check_port:
                    for ip_range in ip_permission.get("IpRanges", []):
                        if ip_range.get("CidrIp") == "0.0.0.0/0":
                            msg = f"VULNERABILITY DETECTED: Security Group '{group_name}' ({group_id}) allows public access to port {check_port}!"
                            logging.warning(msg)
                            print(f"[WARNING] {msg}")
                            vulnerable_groups += 1
                            break # Move to next security group once a vulnerability is confirmed

        summary_msg = f"Security scan completed. Found {vulnerable_groups} vulnerable Security Group(s)."
        logging.info(summary_msg)
        print(f"[SUCCESS] {summary_msg}")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response.get('Error', {}).get('Message', str(e))}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
        
    except Exception as e:
        logging.error(f"System Error: {e}")
        print(f"[ERROR] System Error: {e}")

# This block allows the script to be tested standalone via CLI
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="Security Group Port Vulnerability Scanner")
    parser.add_argument('--port', type=int, default=22, help="Port to check for public access (default: 22)")
    args = parser.parse_args()

    security_check(args.port)