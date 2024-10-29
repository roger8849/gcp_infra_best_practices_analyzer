from langgraph.graph import START, END, StateGraph
from models.gcp_best_practices_state import GCPBestPracticesState

import utils.gcp.organization_utils as ou

from google.cloud import resourcemanager_v3
from utils.app.init_utils import InitUtils 


def get_all_projects(state: GCPBestPracticesState):
    """
    Retrieves a list of all projects under a given organization.

    Args:
      organization_id: The ID of the Google Cloud organization.

    Returns:
      A list of project IDs.
    """
    organization_id = InitUtils.application_configuration.main_organization_id
    try:
        client = resourcemanager_v3.ProjectsClient()
        request = resourcemanager_v3.SearchProjectsRequest(
            query=f"parent.id:{organization_id}"
        )
        response = client.search_projects(request=request)

        projects = [project.project_id for project in response.projects]
        return {'projects', projects}
    except Exception as e:
        print(f"Error getting projects: {e}")
        return []


def build_graph() -> StateGraph:
    builder = StateGraph(GCPBestPracticesState)
    builder.add_node(get_all_projects.__name__, get_all_projects)
    # builder.add_node(get_init_utils.__name__, get_init_utils)

    builder.add_edge(START, get_all_projects.__name__)
    # builder.add_edge(get_init_utils.__name__, get_available_regions.__name__)
    builder.add_edge(get_all_projects.__name__, END)

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

