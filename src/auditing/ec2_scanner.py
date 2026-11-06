import boto3
from mypy_boto3_ec2 import EC2Client

def scan_ec2_instances():
    print("1. Connecting to AWS (Region: ap-southeast-1)...")
    # Initiate client to talk with EC2 service
    ec2_client: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')
    
    print("2. Get response from EC2 back...")
    # Get response from EC2
    response = ec2_client.describe_instances()
    
    print("-" * 50)
    count = 0
    
    #AWS data back have 2 layers of datas
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            
            #Get data by dictionary skills
            instance_id = instance.get("InstanceId", "N/A")

            #Get ipv4
            public_ip = instance.get("PublicIpAddress", "No public ip")

            # Key "State" is a deeper dictionary inside a larger dictionary, we take key "Name"
            state = instance.get("State", {}).get("Name", "N/A")
            
            print(f"✅ Found EC2 instance! | ID: {instance_id} | Trạng thái: {state} , IPv4: {public_ip}")
            count += 1
            
    print("-" * 50)
    print(f"Calculated EC2 Instance right now: {count}")

# Điểm kích hoạt script
if __name__ == "__main__":
    scan_ec2_instances()
 