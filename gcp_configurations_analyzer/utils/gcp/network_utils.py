
import googleapiclient.discovery

def query_network_configs(project="castilla-lived"):
    """Queries Google Cloud network configurations and prints results."""

    compute = googleapiclient.discovery.build('compute', 'v1')



    # Get a list of networks
    networks_result = compute.networks().list(project=project).execute()
    networks = networks_result.get('items', [])

    if not networks:
        print('No networks found.')
    else:
        print('Networks:')
        for network in networks:
            print(f"- Name: {network['name']}")
            print(f"  Description: {network.get('description')}")
            print(f"  Subnets:")

            print('############################################')
            print(network)

            # Get details for each subnet associated with the network
            subnets_result = compute.subnetworks().list(
                project=project, region='us-central1').execute()
            subnets = subnets_result.get('items', [])

            for subnet in subnets:
                print(f"    - {subnet['name']}, CIDR: {subnet['ipCidrRange']}")
                print("------------------------")
                print(subnet)
                print("------------------------")

            print('############################################')