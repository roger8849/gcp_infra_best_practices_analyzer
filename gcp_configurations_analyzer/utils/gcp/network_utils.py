from utils.app.console_utils import ConsoleUtils as cu
from google.cloud import compute_v1
from utils.app.init_utils import InitUtils
import traceback

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

class NetworkUtils:

    @staticmethod
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
            network_pretty_config = ''
            # cu.print_heading1_message(str(networks))
            for net in networks:
                network_pretty_config = ''.join(
                    [
                        str(network_pretty_config),
                        "-" * 50,
                        "\n",
                        "Network name: ",
                        str(net.name),
                        "\n",
                        "Auto create subnetworks: ",
                        str(net.auto_create_subnetworks),
                        "\n",
                        "Network creation timestamp: ",
                        str(net.creation_timestamp),
                        "\n",
                        "Network description: ",
                        str(net.description),
                        "\n",
                        "Network Enable ULA Internal IPv6: ",
                        str(net.enable_ula_internal_ipv6),
                        "\n",
                        "Network Firewall Policy: ",
                        str(net.firewall_policy),
                        "\n",
                        "Network Gateway: ",
                        str(net.gateway_i_pv4),
                        "\n",
                        "Network Ipv4 Range: ",
                        str(net.I_pv4_range),
                        "\n",
                        "Network id: ",
                        str(net.id),
                        "\n",
                        "Network Internal IPv6 range: ",
                        str(net.internal_ipv6_range),
                        "\n",
                        "Network kind: ",
                        str(net.kind),
                        "\n",
                        "Network MTU: ",
                        str(net.mtu),
                        "\n",
                        "Network Firewall Policy enforcer: ",
                        str(net.network_firewall_policy_enforcement_order),
                        "\n",
                        "Network Peerings: ",
                        str(net.peerings),
                        "\n",
                        "Network Routing config: ",
                        str(net.routing_config),
                        "\n",
                        "-" * 50,
                        "\n"
                    ]
                )



            firewall_client = compute_v1.FirewallsClient()
            firewall_rules = firewall_client.list(project=project_id)
            firewall_rules_pretty_config = str()
            for fwr in firewall_rules:
                firewall_rules_pretty_config = "".join(
                    [
                        str(firewall_rules_pretty_config),
                        "-" * 50,
                        "\n",
                        "Firewall rule id: ",
                        str(fwr.id),
                        "\n",
                        "Firewall rule name: ",
                        str(fwr.name),
                        "\n",
                        "Firewall rule description: ",
                        str(fwr.description),
                        "\n",
                        "Firewall rule priority: ",
                        str(fwr.priority),
                        "\n",
                        "Firewall rule source ranges: ",
                        str(fwr.source_ranges),
                        "\n",
                        "Firewall rule source service accounts: ",
                        str(fwr.source_service_accounts),
                        "\n",
                        "Firewall rule network: ",
                        str(fwr.network),
                        "\n",
                        "Firewall rule target tags: ",
                        str(fwr.target_tags),
                        "\n",
                        "Firewall rule target service accounts: ",
                        str(fwr.target_service_accounts),
                        "\n",
                        "Firewall rule kind",
                        str(fwr.kind),
                        "\n",
                        "Firewall rule disabled: ",
                        str(fwr.disabled),
                        "\n",
                        "-" * 50,
                        "\n"
                    ]
                )
            cu.print_heading1_message(firewall_rules_pretty_config)

            # Get subnets
            subnets = []
            subnet_client = compute_v1.SubnetworksClient()
            subnets = subnet_client.list_usable(project=project_id)
            subnets_pretty_config = ""
            for subnet in subnets:
                subnets_pretty_config = "".join(
                    [
                        str(subnets_pretty_config),
                        "-" * 50,
                        "\n",
                        # "Subnet name: ",
                        # str(subnet.name),
                        # "\n",
                        "Subnet ip_ciddr range",
                        str(subnet.ip_cidr_range),
                        "\n",
                        "Subnet purpose",
                        str(subnet.purpose),
                        "\n",
                        "Subnet secondary ip range",
                        str(subnet.secondary_ip_ranges),
                        "\n",
                        "Subnet network",
                        str(subnet.network),
                        "\n",
                        "Subnet internal ipv6 prefix",
                        str(subnet.internal_ipv6_prefix),
                        "\n",
                        "Subnet external ipv6 prefix",
                        str(subnet.external_ipv6_prefix),
                        "\n",
                        "-" * 50,
                        "\n",
                    ]
                )
            return {
                "firewall_rules": firewall_rules,
                "firewall_rules_pretty_config": firewall_rules_pretty_config,
                "networks": networks,
                "network_pretty_config": network_pretty_config,
                "subnets": subnets,
                "subnets_pretty_config": subnets_pretty_config,
            }

        except Exception as e:
            print(f"Error getting networking information: {e}")
            print(traceback.format_exc())
            return None

    @staticmethod
    def get_vpn_tunnels(project_id):
        vpn_client = compute_v1.VpnTunnelsClient()
        tunnels = []
        vpn_pretty_config = ""
        for region_name in InitUtils.application_configuration.region_list:
            vpn_tunnels = vpn_client.list(project=project_id, region=region_name)
            print(f"VPN Tunnels in {region_name}:")
            for tunnel in vpn_tunnels:
                tunnels.append(tunnel)
                vpn_pretty_config = "".join(
                    [
                        str(vpn_pretty_config),
                        "-" * 50,
                        "\n",
                        "Tunnel name",
                        str(tunnel.name),
                        "\n",
                        "Tunnel IKE Version: ",
                        str(tunnel.ike_version),
                        "\n",
                        "Tunnel Peer ip: ",
                        str(tunnel.peer_ip),
                        "\n",
                        "Tunnel status: ",
                        str(tunnel.status),
                        "\n",
                        "Tunnel Shared secret: ",
                        str(tunnel.shared_secret ),
                        "\n",
                        "Tunnel Peer GCP Gateway: ",
                        str(tunnel.peer_gcp_gateway ),
                        "\n",
                        "Tunnel Kind: ",
                        str(tunnel.kind),
                        "\n",
                        "-" * 50,
                        "\n",
                    ]
                )
        return {
            "vpn_tunnels": tunnels,
            "vpn_pretty_config": vpn_pretty_config,
        }
