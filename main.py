import argparse
import logging
import sys

#1. Auditing Module Imports
from src.auditing import auto_tagging_off_instance
from src.auditing import auto_tagging_on_and_remove_old_tag_instance
from src.auditing import ec2_scanner
from src.auditing import tag_auditor
#2. Finops mudule imports
from src.finops import auto_start
from src.finops import auto_stop
from src.finops import auto_stop_only_one_instance
from src.finops import cost_check
from src.finops import stop_dev_servers
from src.finops import inventory_summary
from src.finops import start_dev_server
from src.finops import finops_logic
#3. Security module imports
from src.security import security_group_checker

def setup_logging():
    """
    Centralize logging configuration for the entire application.
    Outputs to finops_bot.log and streams to stdout for Docker compatibility.
    """
    logging.basicConfig(
        filename='finops_bot.log',
        level=logging.INFO,
        format='[%(asctime)s] - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)


def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="AWS FinOps Bot - Central Command Dispatcher",
        epilog="Example: python main.py --action check-cost --region ap-southeast-1"
    )

    parser.add_argument(
        '-a', '--action',
        type=str,
        required=True,
        choices=[
            'stop-instances', 
            'stop-tag-alert', 
            'start-tag', 
            'scan-inventory', 
            'audit-tags', 
            'wake-bot-instances',
            'stop-dry-run',
            'check-cost',
            'inventory-summary',
            'start-devs',
            'stop-devs',
            'simulate-filter',
            'check-security'
        ],
        help="The specific FinOps action to execute."
    )

    parser.add_argument('-r', '--region', type=str, default='ap-southeast-1', help="AWS Region (default: ap-southeast-1)")
    parser.add_argument('--instance-ids', type=str, nargs='+', help="List of EC2 Instance IDs")
    parser.add_argument('--instance-id', type=str, help="A single EC2 Instance ID")
    parser.add_argument('--sns-topic', type=str, help="SNS Topic ARN")
    parser.add_argument('--dry-run', action='store_true', help="Enable DryRun to check permissions without modifying resources")
    parser.add_argument('--port', type=int, default=22, help="Target port for security check (default: 22)")

    args = parser.parse_args()
    logging.info(f"Initializing FinOps Bot. Action: {args.action} | Region: {args.region}")

    # Routing logic using the newly structured module imports
    if args.action == 'stop-instances':
        if not args.instance_ids:
            logging.error("Missing --instance-ids.")
            sys.exit(1)
        auto_stop.manage_ec2_instances(args.instance_ids, args.region) # Adjust function call suffix if needed based on your module's internal function name

    elif args.action == 'stop-tag-alert':
        if not args.instance_id or not args.sns_topic:
            logging.error("Missing --instance-id or --sns-topic.")
            sys.exit(1)
        auto_tagging_off_instance.auto_tagging_off_instances(args.instance_id, args.sns_topic, args.region)

    elif args.action == 'start-tag':
        if not args.instance_id:
            logging.error("Missing --instance-id.")
            sys.exit(1)
        auto_tagging_on_and_remove_old_tag_instance.auto_tagging_on_instances(args.instance_id, args.region)

    elif args.action == 'scan-inventory':
        ec2_scanner.scan_ec2_instances(args.region)

    elif args.action == 'audit-tags':
        tag_auditor.tag_auditor(args.region)

    elif args.action == 'wake-bot-instances':
        auto_start.auto_start_instances_stopped_by_bot(args.region)

    elif args.action == 'stop-dry-run':
        if not args.instance_id:
            logging.error("Missing --instance-id.")
            sys.exit(1)
        auto_stop_only_one_instance.auto_stop_instance_dry_run(args.instance_id, args.dry_run, args.region)
        
    elif args.action == 'check-cost':
        cost_check.calculate_price(args.region)
        
    elif args.action == 'inventory-summary':
        inventory_summary.inventory_summary(args.region)
        
    elif args.action == 'start-devs':
        start_dev_server.hunt_and_start_dev_servers(args.region)
        
    elif args.action == 'stop-devs':
        stop_dev_servers.hunt_and_stop_dev_servers(args.region)

    elif args.action == 'simulate-filter':
        finops_logic.simulate_environment_filtering()
        
    elif args.action == 'check-security':
        security_group_checker.security_check(args.port, args.region)

if __name__ == "__main__":
    main()