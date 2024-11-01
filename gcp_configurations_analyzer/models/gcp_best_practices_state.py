from typing import List
from typing_extensions import TypedDict


class GCPBestPracticesState(TypedDict):
    projects: list # Projects inside organization.
    network_projects: list  # Projects with VPCs configured.
    networks: list  # List of VPC networks
    firewall_rules: list  # List of firewall rules
    subnets: list  # List of subnets
    vpn_tunnels: list  # List of vpn_tunnels
    vpc_best_practices: (
        str  # Summarized string with the documentation of the VPC best practices.
    )
    vpn_best_practices: (
        str  # Summarzed string with the documentation of the VPN best practices.
    )

    networks_pretty_config: (
        str # Contains a pretty string with the network configuration
    )

    firewall_rules_pretty_config: (
        str # Contains a pretty string with the firewall rules configuration
    )

    subnets_pretty_config: (
        str # Contains a pretty string with the subnet configuration
    )

    vpn_pretty_config: (
        str # Contains a pretty string with the VPN configuration.
    )
    
    vpc_action_items: (
        str # Contains the best practices recommended by the llm model.
    )
    
    vpn_action_items: (
        str # Contains the best practices recommended by the llm model.
    )

    final_report: (
        str # Contains the final report in markdown
    )

