import boto3
from mypy_boto3_ec2 import EC2Client
import logging
from botocore.exceptions import ClientError
from datetime import datetime
logging.basicConfig(
    filename='auto_tagging_turned_off_instances.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S' 
)

SNS_TOPIC_ARN = "arn:aws:sns:ap-southeast-1:335937357465:MyTestTpic"

def auto_tagging_off_instances(instance_id, sns_topic_arn, region_name = 'ap-southeast-1'):
    ec2: EC2Client = boto3.client('ec2', region_name=region_name)
    sns = boto3.client('sns', region_name=region_name)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        ec2.create_tags(
            Resources=[instance_id],
            Tags = [
                {
                    'Key': 'StoppedBy',
                    'Value': 'FinOpsBot'
                },
                {
                    'Key': 'StopDate',
                    "Value": current_time
                }
            ]
        )
        logging.info(f"Successfully stopped and tagged into this {instance_id}.")

        message_body = f"FinOps bot notify: Successfully automated turned off and tagged instance: {instance_id}"
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject ="[AWS Alert] - Automated turned off EC2",
            Message=message_body
        )

    except ClientError as e:
        error_msg =logging.error(f"Error came from AWS API: {e.response['Error']['Message']}")
        logging.error(error_msg)
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject="[AWS ERROR] - FinOps Bot failed",
            Message=f"Bot get into trouble while try to turned off instance: {instance_id}\n Error Detail: {error_msg}"
        )
    except Exception as e:
        logging.error(f"System error : {e}")

if __name__ == "__main__":
    auto_tagging_off_instances("i-0e01a67ad87b5bf4")