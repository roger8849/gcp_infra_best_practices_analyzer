from langgraph.graph import START, END, StateGraph
from models.gcp_best_practices_state import GCPBestPracticesState

import utils.gcp.organization_utils as ou
from utils.app.init_utils import InitUtils
import utils.gcp.network_utils as nu
import utils.app.app_utils as au

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

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
    return {"projects": projects} if projects else {"projects": None}


def get_all_networks(state: GCPBestPracticesState):
    projects_id = state["projects"]

    networks = firewall_rules = subnets = []
    network_projects = []
    for id in projects_id:
        project_network_information = nu.get_project_network_information(id)
        if project_network_information and project_network_information["networks"]:
            networks.append(project_network_information["networks"])
            firewall_rules.append(project_network_information["firewall_rules"])
            subnets.append(project_network_information["subnets"])
            network_projects.append(id)

    return {
        "networks": networks,
        "firewall_rules": firewall_rules,
        "subnets": subnets,
        "network_projects": network_projects,
    }


def get_all_vpn_tunnels(state: GCPBestPracticesState):
    projects_id = state["network_projects"]
    tunnels = []
    for id in projects_id:
        project_tunnels = nu.get_vpn_tunnels(id)
        if project_tunnels:
            tunnels.append(project_tunnels)
    return {"tunnels": tunnels}


def summarize_vpc_best_practices(state: GCPBestPracticesState):
    url = "https://cloud.google.com/architecture/best-practices-vpc-design"
    text = au.extract_text_from_url(url)

    analyzer_instructions = f"""You are a VPC best practices analyzer for configurations in google cloud. You have extracted text for the following Webpage:

    {url}

    Now I need you to summarize the following text:
    
    {text}

    and understand pretty well it's content, because you will use it to analyze some configurations.
    
    """
    vpc_best_practices = llm.invoke(
        [SystemMessage(content=analyzer_instructions)]
        + [
            HumanMessage(
                content=f"Summarize the content of the VPC best practices you've extracted."
            )
        ]
    )
    return {"vpc_best_practices": vpc_best_practices.content}


def summarize_vpn_best_practices(state: GCPBestPracticesState):
    url = (
        "https://cloud.google.com/network-connectivity/docs/vpn/concepts/best-practices"
    )

    text = au.extract_text_from_url(url)

    analyzer_instructions = f"""You are a VPN best practices analyzer for configurations in google cloud. You have extracted text for the following Webpage:

    {url}

    Now I need you to summarize the following text:
    
    {text}

    and understand pretty well it's content, because you will use it to analyze some configurations.
    
    """
    vpn_best_practices = llm.invoke(
        [SystemMessage(content=analyzer_instructions)]
        + [
            HumanMessage(
                content=f"Summarize the content of the VPN best practices you've extracted."
            )
        ]
    )

    return {"vpn_best_practices": vpn_best_practices.content}

# def normalize_gcp_information(state: GCPBestPracticesState):
    

def build_graph() -> StateGraph:
    builder = StateGraph(GCPBestPracticesState)

    # add nodes to the graph builder
    builder.add_node(get_all_projects.__name__, get_all_projects)
    builder.add_node(get_all_networks.__name__, get_all_networks)
    builder.add_node(get_all_vpn_tunnels.__name__, get_all_vpn_tunnels)
    builder.add_node(
        summarize_vpc_best_practices.__name__, summarize_vpc_best_practices
    )
    builder.add_node(
        summarize_vpn_best_practices.__name__, summarize_vpn_best_practices
    )

    # add edges to the graph builder.
    builder.add_edge(START, get_all_projects.__name__)

    builder.add_edge(get_all_projects.__name__, get_all_networks.__name__)
    builder.add_edge(get_all_networks.__name__, get_all_vpn_tunnels.__name__)

    builder.add_edge(get_all_projects.__name__, summarize_vpc_best_practices.__name__)
    builder.add_edge(
        summarize_vpc_best_practices.__name__, summarize_vpn_best_practices.__name__
    )

    builder.add_edge(get_all_vpn_tunnels.__name__, END)
    builder.add_edge(summarize_vpn_best_practices.__name__, END)
    
    

    return builder


def start_analysis():
    global llm 
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=InitUtils.get_application_configuration().llm_api_key)
    thread = {"configurable": {"thread_id": "1"}}
    builder = build_graph()

    graph = builder.compile()

    # display(Image(graph.get_graph().draw_mermaid_png()))
    graph.get_graph().draw_png("./generated_graph.png")

    # graph.invoke(
    #     {
    #         "projects": ou.list_projects(
    #             InitUtils.application_configuration.main_organization_id
    #         ),
    #         "vpc_best_practices": "",
    #         "vpn_best_practices": "",
    #     },
    #     thread
    # )
    graph.invoke(
        {
            "projects": ['castilla-lived'],
            "network_projects": ["castilla-lived"]
        },
        thread
    )
