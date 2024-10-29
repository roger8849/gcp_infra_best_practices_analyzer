from langgraph.graph import START, END, StateGraph
from models.gcp_best_practices_state import GCPBestPracticesState

import utils.gcp.organization_utils as ou
from utils.app.init_utils import InitUtils 
import utils.gcp.network_utils as nu


def get_all_projects(state: GCPBestPracticesState):
    """
    Retrieves a list of all projects under a given organization.

    Args:
      organization_id: The ID of the Google Cloud organization.

    Returns:
      A list of project IDs.
    """
    organization_id = InitUtils.application_configuration.main_organization_id
    projects = ou.list_projects(organization_id)
    return {'projects': projects} if projects else {'projects': None}

def get_all_networks(state: GCPBestPracticesState):
    projects_id = state['projects']
    # networks = []
    networks = firewall_rules = subnets = []
    for id in projects_id:
        #     networks.append(nu.query_network_configs(id))
        # return {'networks': networks} if networks else {'networks': []}
        project_network_information = nu.get_project_network_information(id)
        if project_network_information and project_network_information['networks']:
            networks.append(project_network_information['networks'])
            firewall_rules.append(project_network_information['firewall_rules'])
            subnets.append(project_network_information['subnets'])
        

    return {'networks': networks, 'firewall_rules': firewall_rules, 'subnets': subnets}

def get_all_vpn_tunnels(state:GCPBestPracticesState):
    projects_id = state['projects']
    tunnels = []
    for id in projects_id:
        project_tunnels = nu.get_vpn_tunnels(id)
        if project_tunnels:
            tunnels.append(project_tunnels)
    return {'tunnels': tunnels}
    


def build_graph() -> StateGraph:
    builder = StateGraph(GCPBestPracticesState)
    builder.add_node(get_all_projects.__name__, get_all_projects)
    builder.add_node(get_all_networks.__name__, get_all_networks)
    builder.add_node(get_all_vpn_tunnels.__name__, get_all_vpn_tunnels)
    # builder.add_node(get_init_utils.__name__, get_init_utils)

    builder.add_edge(START, get_all_projects.__name__)
    # builder.add_edge(get_init_utils.__name__, get_available_regions.__name__)
    builder.add_edge(get_all_projects.__name__, get_all_networks.__name__)
    builder.add_edge(get_all_projects.__name__, get_all_vpn_tunnels.__name__)
    builder.add_edge(get_all_networks.__name__, END)
    builder.add_edge(get_all_vpn_tunnels.__name__, END)

    return builder

def start_analysis():
    thread = {"configurable": {"thread_id": "1"}}
    builder = build_graph()

    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    graph.get_graph().draw_png("./generated_graph.png")

    graph.invoke({'projects': []}, thread)
    # for event in graph.stream({}, thread, stream_mode="values"):
    #     print(event)

