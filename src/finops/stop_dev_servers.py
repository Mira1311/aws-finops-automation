import boto3
from mypy_boto3_ec2 import EC2Client

def hunt_and_stop_dev_servers():
    ec2_client: EC2Client = boto3.client('ec2', region_name='ap-southeast-1')
    print("1. Scanning AWS System")
    
    response = ec2_client.describe_instances()
    target_instances = [] # A list which represent instances need to be killed

    # Get data from layers
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance.get("InstanceId")
            state = instance.get("State", {}).get("Name")
            
            # Skip if state is not running
            if state != "running":
                continue
                
            # check if tags == dev
            is_dev = False
            for tag in instance.get("Tags", []):
                if tag.get("Key") == "Environment" and tag.get("Value") == "dev":
                    is_dev = True
                    break # find dev -> break the loop
            
            # if tag is dev and state is running -> append to terminated target list
            if is_dev:
                target_instances.append(instance_id)
                print(f"  [WARNING] Detected Dev monitor wasting money: {instance_id}")

    print("-" * 50)
    # Send terminated command
    if len(target_instances) > 0:
        print(f"2. Decided: Turned off {len(target_instances)} instances.")
        # Boto3 active
        ec2_client.stop_instances(InstanceIds=target_instances)
        print(f"✅ Send Stop signal successfully for: {target_instances}")
    else:
        print("✅ System fine. No dev instances wasting money.")

if __name__ == "__main__":
    hunt_and_stop_dev_servers()