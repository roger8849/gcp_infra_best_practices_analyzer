'''
Explanation:

Imports: The script imports the googleapiclient.discovery library for interacting with Google Cloud APIs.
query_network_configs Function:
Builds the API Client: Creates a Compute Engine API client using googleapiclient.discovery.build.
Project ID: Replaces 'your-project-id' with your Google Cloud project ID.
Lists Networks: Fetches a list of networks within your project.
Prints Network Details: Iterates through the networks, printing their name, description, and associated subnets.
if __name__ == '__main__': This block ensures the query_network_configs function is executed when the script is run directly.
'''


import googleapiclient.discovery

def query_network_configs():
    """Queries Google Cloud network configurations and prints results."""

    compute = googleapiclient.discovery.build('compute', 'v1')

    # Replace 'your-project-id' with your actual Google Cloud project ID
    # project = 'your-project-id' 
    project = 'castilla-host-project' 

    # Get a list of networks 
    networks_result = compute.networks().list(project=project).execute()
    networks = networks_result.get('items', [])

    if not networks:
        print('No networks found.')
    else:
        print('Networks:')
        for network in networks:
            # print(f"- Name: {network['name']}")
            # print(f"  Description: {network.get('description')}")
            # print(f"  Subnets:")
            print(network)

            # Get details for each subnet associated with the network
            subnets_result = compute.subnetworks().list(project=project, region='us-central1').execute()
            subnets = subnets_result.get('items', [])

            for subnet in subnets:
                # print(f"    - {subnet['name']}, CIDR: {subnet['ipCidrRange']}")
                print(subnet)

            print("------------------------")

if __name__ == '__main__':
    query_network_configs()
