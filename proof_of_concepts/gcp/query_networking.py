from google.cloud import compute_v1

# Configure the project ID (replace with your project ID)
project_id = "your-project-id"

# Create a Compute Engine client
client = compute_v1.ProjectsClient()

# Define methods to get information on specific resources

def get_vpc_info(name):
  """Gets information about a VPC network."""
  request = client.get_address(project=project_id, region=name)
  return request.result()

def get_subnet_info(region, name):
  """Gets information about a subnet."""
  request = client.get_subnetwork(project=project_id, region=region, subnetwork=name)
  return request.result()

def get_firewall_info(name):
  """Gets information about a firewall rule."""
  request = client.get_firewall(project=project_id, firewall=name)
  return request.result()

# List VPC networks
print("VPC Networks:")
for network in client.list_aggregated_addresses(project=project_id).addresses:
  # Extract VPC network name from the region name
  name = network.name.split("/")[-1]
  vpc_info = get_vpc_info(name)
  print(f"- Name: {vpc_info.name}")
  print(f"  CIDR Range: {vpc_info.ip_cidr_range}")

# List subnets
print("\nSubnets:")
for region, subnets in client.list_subnetworks(project=project_id).subnetworks.items():
  for subnet in subnets:
    subnet_info = get_subnet_info(region, subnet.name)
    print(f"- Region: {region}")
    print(f"  Name: {subnet_info.name}")
    print(f"  CIDR Range: {subnet_info.ip_cidr_range}")

# List firewall rules
print("\nFirewall Rules:")
for rule in client.list_firewalls(project=project_id).firewalls:
  firewall_info = get_firewall_info(rule.name)
  print(f"- Name: {firewall_info.name}")
  print(f"  Network: {firewall_info.network}")
  print(f"  Allows: {firewall_info.allowed}")

# Remember to replace "your-project-id" with your actual project ID
print("\n**Note:** Remember to replace 'your-project-id' with your actual project ID.")
