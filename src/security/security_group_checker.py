import boto3
from mypy_boto3_ec2 import EC2Client
import logging
import argparse

logging.basicConfig(
    filename='security_alert.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)

def security_check(check_port):
    ec2: EC2Client = boto3.client('ec2', region_name = 'ap-southeast-1')
    print("Scanning the system...")
    #Get the security response
    response = ec2.describe_security_groups()
    #Unnesting 1st layer of the response and get the name and id
    for sec_group in response.get("SecurityGroups", []):
        group_name = sec_group.get("GroupName")
        group_id = sec_group.get("GroupId")
        #Unnnesting 2nd layer of the response (inside 1st layer) to get ip permission
        for ip_permission in sec_group.get("IpPermissions",[]):
            #check port = out target port to check or not
            if ip_permission.get("FromPort") == check_port:
                for ip_range in  ip_permission.get("IpRanges", []):
                    if ip_range.get("CidrIp") == "0.0.0.0/0":
                        logging.warning(f"This security group: '{group_name}' with the id '{group_id}' is in the problem!")
                        break
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type = int, default = 22)
    args = parser.parse_args()

    security_check(args.port)