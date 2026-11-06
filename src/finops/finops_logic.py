#Emulator list running EC2 on AWS
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

for server in ec2_servers:
    if server.startswith("dev-") or server.startswith("test-"):
            stop_list.append(server)
            print(f"Action: Stopping {server}...")
    else:
          keep_running_list.append(server)
          print(f"Action: Keeping {server} running.")

print(f"Number of servers are shut down: {len(stop_list)}")
print(f"Number of servers are still running: {len(keep_running_list)}")

for stop_server in stop_list:
      print(f"Stop server name: {stop_server}")
print()
for run_server in keep_running_list:
      print(f"Running server name: {run_server}")