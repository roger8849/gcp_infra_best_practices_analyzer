import utils.app.console_utils as cu
from google.cloud import compute_v1
from utils.app.init_utils import InitUtils

# def query_network_configs(project_id):
# """Queries Google Cloud network configurations and prints results."""

# compute = googleapiclient.discovery.build('compute', 'v1')


# # Get a list of networks
# networks_result = compute.networks().list(project_id).execute()
# networks = networks_result.get('items', [])

# if networks:
#     # print(networks)
#     cu.print_heading1_message("Networks:")
#     cu.print_heading2_message(str(networks))

#     return networks
#     # print('Networks:')
#     # for network in networks:
#     #     print(f"- Name: {network['name']}")
#     #     print(f"  Description: {network.get('description')}")
#     #     print(f"  Subnets:")

#     #     print(network)

#     #     # Get details for each subnet associated with the network
#     #     subnets_result = compute.subnetworks().list(
#     #         project=project, region='us-central1').execute()
#     #     subnets = subnets_result.get('items', [])

#     #     for subnet in subnets:
#     #         print(f"    - {subnet['name']}, CIDR: {subnet['ipCidrRange']}")
#     #         print("------------------------")
#     #         print(subnet)
#     #         print("------------------------")

#     #     print('############################################')
# else:
#     cu.print_normal_message(f'No networks found in project {project_id}.')


def get_project_network_information(project_id):
    """
    Retrieves networking information (firewalls, networks, subnets) from a GCP project.

    Args:
        project_id: The ID of the Google Cloud project.

    Returns:
        A dictionary containing lists of firewalls, networks, and subnets.
    """

    try:
        network_client = compute_v1.NetworksClient()
        networks = network_client.list(project=project_id)

        cu.print_heading1_message(str(networks))

        # print(networks)
        # networks = [network for network in query_networks if query_networks]
        # query_networks = network_client.list(project=project_id)
        # networks = [network for network in query_networks if query_networks]

        firewall_client = compute_v1.FirewallsClient()
        # query_firewall_rules = firewall_client.list(project=project_id)
        # firewall_rules = [firewall for firewall in query_firewall_rules if query_firewall_rules]
        firewall_rules = firewall_client.list(project=project_id)
        # print(firewall_rules)

        # Get subnets
        subnets = []
        subnet_client = compute_v1.SubnetworksClient()
        subnets = subnet_client.list_usable(project=project_id)
        # subnets = [subnet_client.list_usable(project=project_id, region=region_name) for region_name in InitUtils.application_configuration.region_list]

        # print(subnets)
        # for network in networks:
        #     # subnetworks_request = compute_v1.ListSubnetworksRequest(
        #     #     project=project_id, region=network.region
        #     # )
        #     # subnets.extend(list(subnetworks_client.list(request=subnetworks_request)))
        #     subnet_client = compute_v1.SubnetworksClient()
        #     # subnets = [subnet_client.list(project=project_id, region=region_name) for region_name in InitUtils.application_configuration.region_list]
        #     subnets = subnet_client.list(project=project_id)

        return {
            "firewall_rules": firewall_rules,
            "networks": networks,
            "subnets": subnets,
        }

    except Exception as e:
        print(f"Error getting networking information: {e}")
        return None


def get_vpn_tunnels(project_id):
    vpn_client = compute_v1.VpnTunnelsClient()
    tunnels = []
    for region_name in InitUtils.application_configuration.region_list:
        vpn_tunnels = vpn_client.list(project=project_id, region=region_name)
        print(f"VPN Tunnels in {region_name}:")
        for tunnel in vpn_tunnels:
            tunnels.append(tunnel)
            print(f"Name: {tunnel.name}")
            # print(f"Network: {tunnel.network}")
            print(f"Region: {tunnel.region}")
            print(f"Peer IP: {tunnel.peer_ip}")
            print(f"Router: {tunnel.router}")
            print(f"Status: {tunnel.status}")
            print("-" * 40)
    return tunnels


