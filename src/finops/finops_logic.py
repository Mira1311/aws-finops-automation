import logging

def simulate_environment_filtering(ec2_servers=None):
    """
    Simulates filtering EC2 instances based on environment naming conventions.
    Automatically stops 'dev-' and 'test-' servers while keeping others running.
    """
    if ec2_servers is None:
        ec2_servers = [
            "prod-web-01",
            "dev-backend-01",
            "test-database-01",
            "prod-payment-db",
            "dev-worker-02",
            "staging-api-01"
        ]

    stop_list = []
    keep_running_list = []

    logging.info("Starting EC2 environment filtering simulation.")
    print("[INFO] Starting EC2 environment filtering simulation.\n")

    # Categorize servers based on naming prefix
    for server in ec2_servers:
        if server.startswith("dev-") or server.startswith("test-"):
            stop_list.append(server)
            logging.info(f"Action: Stopping {server}...")
            print(f"[ACTION] Stopping {server}...")
        else:
            keep_running_list.append(server)
            logging.info(f"Action: Keeping {server} running.")
            print(f"[ACTION] Keeping {server} running.")

    print("-" * 50)
    
    # Print and log summaries
    summary_stopped = f"Total servers shut down: {len(stop_list)}"
    summary_running = f"Total servers still running: {len(keep_running_list)}"
    
    logging.info(summary_stopped)
    logging.info(summary_running)
    
    print(f"[SUMMARY] {summary_stopped}")
    print(f"[SUMMARY] {summary_running}")
    print("-" * 50)

    # Detailed lists
    for stop_server in stop_list:
        print(f"[STOPPED] Server name: {stop_server}")
        
    print()
    
    for run_server in keep_running_list:
        print(f"[RUNNING] Server name: {run_server}")

# This block allows the script to be tested standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    simulate_environment_filtering()