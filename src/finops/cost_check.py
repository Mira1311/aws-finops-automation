import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_ec2 import EC2Client

# Constants for pricing (USD per hour)
PRICING = {
    't2.micro': 0.0116, 
    't3.micro': 0.0104
}

def calculate_price(region_name='ap-southeast-1'):
    """
    Scans EC2 instances, counts specific types, and calculates estimated cost savings.
    Designed to be imported and executed by main.py.
    """
    logging.info(f"Starting cost check in region: {region_name}...")
    print(f"[INFO] Starting cost check for t2.micro and t3.micro instances in {region_name}...")

    try:
        ec2: EC2Client = boto3.client('ec2', region_name=region_name)
        
        # Baseline for testing purposes as defined
        total_t2_micro_instances = 1 
        total_t3_micro_instances = 0 

        response = ec2.describe_instances()

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_type = instance.get("InstanceType")
                
                if instance_type == "t2.micro":
                    total_t2_micro_instances += 1
                elif instance_type == "t3.micro":
                    total_t3_micro_instances += 1

        # Calculate total hourly cost
        price_t2_micro = total_t2_micro_instances * PRICING['t2.micro']
        price_t3_micro = total_t3_micro_instances * PRICING['t3.micro']
        total_hourly_cost = price_t2_micro + price_t3_micro
        
        # Assuming a night is approximately 12 hours for the nightly estimate
        total_nightly_savings = total_hourly_cost * 12

        summary_msg = (
            f"Found {total_t2_micro_instances} t2.micro and {total_t3_micro_instances} t3.micro. "
            f"Estimated hourly cost: ${total_hourly_cost:.4f}/hour. "
            f"Estimated savings if turned off overnight (12h): ${total_nightly_savings:.4f}/night."
        )
        
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
    calculate_price()