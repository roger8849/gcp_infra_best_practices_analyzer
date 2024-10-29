from typing import List
from typing_extensions import TypedDict


class GCPBestPracticesState(TypedDict):
    projects : List[str] # Projects inside organization.
    networks : list
    firewall_rules : list
    subnets : list
    vpn_tunnels: list