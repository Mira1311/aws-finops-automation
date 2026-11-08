import logging
from mypy_boto3_ec2 import EC2Client
import boto3
from botocore.exceptions import ClientError

def tag_auditor(region_name = 'ap-southeast-1'):
    logging.info(f"Starting Tag Auditor in region: {region_name}")
    print(f"🔍 Scanning EC2 instances for missing 'Owner' tags in {region_name}...")

    try:
        ec2: EC2Client = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_instances()

        missing_tag_count = 0

        # Unnested datas
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance.get("InstanceId", "Unknown")
                
                # Flag tags
                has_owner = False
                for tag in instance.get("Tags", []):
                    if tag.get("Key") == "Owner":
                        has_owner = True
                        break
                
                # Warning if not has tag (Use 'if not' instead of '== False' for good Pythonic)
                if not has_owner:
                    warning_msg = f"WARNING: Instance {instance_id} is missing the 'Owner' tag!"
                    logging.warning(warning_msg)
                    print(f"{warning_msg}")
                    missing_tag_count += 1

        summary_msg = f"Tag Audit completed. Found {missing_tag_count} instance(s) missing 'Owner' tag."
        logging.info(summary_msg)
        print(f"{summary_msg}")

    except ClientError as e:
        error_msg = f"AWS API Error: {e.response['Error']['Message']}"
        logging.error(error_msg)
        print(f"{error_msg}")
        
    except Exception as e:
        logging.error(f"System error: {e}")
        print(f"System error: {e}")

# Local test only
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tag_auditor()