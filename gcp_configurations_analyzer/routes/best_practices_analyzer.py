import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph

from models.gcp_best_practices_state import GCPBestPracticesState
from utils.app.app_utils import AppUtils as au
from utils.app.console_utils import ConsoleUtils as cu
from utils.app.init_utils import InitUtils
from utils.app.report_utils import ReportUtils as ru
from utils.gcp.network_utils import NetworkUtils as nu
from utils.gcp.organization_utils import OrganizationUtils as ou


class BestPracticesAnalyzer:
    def __init__(self):
        self.llm = None

    @staticmethod
    def get_all_projects(state: GCPBestPracticesState):
        """
        Retrieves a list of all projects under a given organization.

        Args:
          :param state:

        Returns:
          A list of project IDs.
        """
        organization_id = InitUtils.application_configuration.main_organization_id
        projects = ou.list_projects(organization_id)
        return {"projects": projects} if projects else {"projects": None}

    @staticmethod
    def get_all_networks(state: GCPBestPracticesState):
        projects_id = state["projects"]

        networks = firewall_rules = subnets = []
        networks_pretty_config = firewall_rules_pretty_config = subnets_pretty_config = ""
        network_projects = []
        for id in projects_id:
            project_network_information = nu.get_project_network_information(id)
            if (
                    project_network_information
                    and project_network_information["networks"]
                    and project_network_information["networks"]._response.items
            ):
                networks.append(project_network_information["networks"])
                if project_network_information["network_pretty_config"]:
                    networks_pretty_config += project_network_information[
                        "network_pretty_config"
                    ]

                firewall_rules.append(project_network_information["firewall_rules"])

                if project_network_information["firewall_rules_pretty_config"]:
                    firewall_rules_pretty_config += project_network_information[
                        "firewall_rules_pretty_config"
                    ]

                subnets.append(project_network_information["subnets"])
                if project_network_information["subnets_pretty_config"]:
                    subnets_pretty_config += project_network_information[
                        "subnets_pretty_config"
                    ]
                network_projects.append(id)

        return {
            "networks": networks,
            "networks_pretty_config": networks_pretty_config,
            "firewall_rules": firewall_rules,
            "firewall_rules_pretty_config": firewall_rules_pretty_config,
            "subnets": subnets,
            "subnets_pretty_config": subnets_pretty_config,
            "network_projects": network_projects,
        }

    @staticmethod
    def get_all_vpn_tunnels(state: GCPBestPracticesState):
        projects_id = state["network_projects"]
        tunnels = []
        vpn_pretty_config = ""
        for id in projects_id:
            vpn_tunnel_information = nu.get_vpn_tunnels(id)
            if vpn_tunnel_information and vpn_tunnel_information["vpn_tunnels"]:
                tunnels.append(vpn_tunnel_information["vpn_tunnels"])
            if vpn_tunnel_information and vpn_tunnel_information["vpn_pretty_config"]:
                vpn_pretty_config += vpn_tunnel_information["vpn_pretty_config"]

        return {"vpn_tunnels": tunnels, "vpn_pretty_config": vpn_pretty_config}

    def summarize_vpc_best_practices(self, state: GCPBestPracticesState):
        url = "https://cloud.google.com/architecture/best-practices-vpc-design"
        text = au.extract_text_from_url(url)

        analyzer_instructions = f"""You are a VPC best practices analyzer for configurations in google cloud. You have extracted text for the following Webpage:
    
        {url}
    
        Now I need you to summarize the following text:
        
        {text}
    
        and understand pretty well it's content, because you will use it to analyze some configurations.
        
        """
        vpc_best_practices = self.llm.invoke(
            [SystemMessage(content=analyzer_instructions)]
            + [
                HumanMessage(
                    content=f"Summarize the content of the VPC best practices you've extracted."
                )
            ]
        )
        return {"vpc_best_practices": vpc_best_practices.content}

    def summarize_vpn_best_practices(self, state: GCPBestPracticesState):
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
        vpn_best_practices = self.llm.invoke(
            [SystemMessage(content=analyzer_instructions)]
            + [
                HumanMessage(
                    content=f"Summarize the content of the VPN best practices you've extracted."
                )
            ]
        )

        return {"vpn_best_practices": vpn_best_practices.content}

    def analyze_vpc_best_practices(self, state: GCPBestPracticesState):
        vpc_best_practices = state["vpc_best_practices"]
        network_pretty_config = state["networks_pretty_config"]
        firewall_rules_pretty_config = state["firewall_rules_pretty_config"]
        subnets_pretty_config = state["subnets_pretty_config"]

        system_instructions = """
            You are a GCP Specialist with deep expertise in Google Cloud's networking services. 
            Your task is to provide actionable, specific, and configuration-aware recommendations for improving a VPC setup.
            Base your advice on the provided best practices and the detailed configuration information.
        """

        human_instructions = f"""
            Review the following summarized VPC and network management best practices:
            \"\"\"{vpc_best_practices}\"\"\"

            Analyze the current VPC setup provided below and identify specific action items for improvement based on these best practices:
            - **VPC Configuration**: 
              {network_pretty_config}
            - **Firewall Rules**: 
              {firewall_rules_pretty_config}
            - **Subnets**: 
              {subnets_pretty_config}

            Guidelines for your recommendations:
            - Be specific and directly reference the provided configuration.
            - Highlight any misalignments with the best practices.
            - Propose clear, actionable steps to improve the configuration.
            - Avoid generic suggestions; tailor your advice to the provided setup.

            Provide your response in the following format:
            1. **Issue/Observation**: Describe the specific issue or potential improvement.
            2. **Recommendation**: Provide a clear action item to address the issue.
            3. **Rationale**: Explain how this aligns with the best practices.
        """

        vpc_action_items = self.llm.invoke(
            [SystemMessage(content=system_instructions)]
            + [HumanMessage(content=human_instructions)]
        )

        return {"vpc_action_items": vpc_action_items.content}

    def analyze_vpn_best_practices(self, state: GCPBestPracticesState):
        vpn_best_practices = state["vpn_best_practices"]
        vpn_pretty_config = state["vpn_pretty_config"]

        system_instructions = f"""
            You're a GCP Specialist, now this is the summarized text of the best practices recommended for VPN and network management in GCP
        """
        human_instructions = f"""
            Taking into account the summarized VPN and network management best practices:
            \"{vpn_best_practices}\""
            
            Also taking into account your own experiencia, provide action items and recommendations for my current:
            VPN CONFIGURATION:
            {vpn_pretty_config}
    
            What action items can I execute to improve my configuration based on the VPN Best practices?
    
            Be specific with my configuration do not give me generic recommendation please analyze my current configuration provided above.
        """

        vpn_action_items = self.llm.invoke(
            [SystemMessage(content=system_instructions)]
            + [HumanMessage(content=human_instructions)]
        )

        return {"vpn_action_items": vpn_action_items.content}

    @staticmethod
    def write_final_report(state: GCPBestPracticesState):
        final_report = ru.get_report_template().format(
            vpc_config=state["networks_pretty_config"],
            firewall_rules_config=state["firewall_rules_pretty_config"],
            subnets_config=state["subnets_pretty_config"],
            vpn_config=state["vpn_pretty_config"],
            vpc_best_practices=state["vpc_best_practices"],
            vpn_best_practices=state["vpn_best_practices"],
            vpc_action_items=state["vpc_action_items"],
            vpn_action_items=state["vpn_action_items"],
        )
        md_filename = ru.generate_filename()
        f = open(f"./reports/{md_filename}", "w")
        f.write(final_report)

        absolute_path = os.path.abspath(f.name)
        f.close()

        cu.print_heading1_message(f'Analisys ended find the full report at {absolute_path}')


        ru.markdown_to_pdf(f"./reports/{md_filename}", f"./reports/{md_filename}.pdf")
        return {"final_report": final_report}

    def build_graph(self) -> StateGraph:
        builder = StateGraph(GCPBestPracticesState)

        # add nodes to the graph builder
        builder.add_node(BestPracticesAnalyzer.get_all_projects.__name__, BestPracticesAnalyzer.get_all_projects)
        builder.add_node(BestPracticesAnalyzer.get_all_networks.__name__, BestPracticesAnalyzer.get_all_networks)
        builder.add_node(BestPracticesAnalyzer.get_all_vpn_tunnels.__name__, BestPracticesAnalyzer.get_all_vpn_tunnels)
        builder.add_node(
            self.summarize_vpc_best_practices.__name__, self.summarize_vpc_best_practices
        )
        builder.add_node(
            self.summarize_vpn_best_practices.__name__, self.summarize_vpn_best_practices
        )
        builder.add_node(self.analyze_vpc_best_practices.__name__, self.analyze_vpc_best_practices)
        builder.add_node(self.analyze_vpn_best_practices.__name__, self.analyze_vpn_best_practices)
        builder.add_node(BestPracticesAnalyzer.write_final_report.__name__, BestPracticesAnalyzer.write_final_report)

        # add edges to the graph builder.
        builder.add_edge(START, BestPracticesAnalyzer.get_all_projects.__name__)

        builder.add_edge(BestPracticesAnalyzer.get_all_projects.__name__,
                         BestPracticesAnalyzer.get_all_networks.__name__)
        builder.add_edge(BestPracticesAnalyzer.get_all_networks.__name__,
                         BestPracticesAnalyzer.get_all_vpn_tunnels.__name__)

        builder.add_edge(BestPracticesAnalyzer.get_all_projects.__name__, self.summarize_vpc_best_practices.__name__)
        builder.add_edge(
            self.summarize_vpc_best_practices.__name__, self.summarize_vpn_best_practices.__name__
        )

        builder.add_edge(BestPracticesAnalyzer.get_all_vpn_tunnels.__name__, self.analyze_vpc_best_practices.__name__)
        builder.add_edge(
            self.summarize_vpn_best_practices.__name__, self.analyze_vpc_best_practices.__name__
        )

        builder.add_edge(
            self.analyze_vpc_best_practices.__name__, self.analyze_vpn_best_practices.__name__
        )
        builder.add_edge(self.analyze_vpn_best_practices.__name__, BestPracticesAnalyzer.write_final_report.__name__)
        builder.add_edge(BestPracticesAnalyzer.write_final_report.__name__, END)

        return builder

    def start_analysis(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            openai_api_key=InitUtils.get_application_configuration().llm_api_key,
        )

        thread = {"configurable": {"thread_id": "1"}}
        builder = self.build_graph()

        graph = builder.compile()

        # display(Image(graph.get_graph().draw_mermaid_png()))
        graph.get_graph().draw_png("./generated_graph.png")

        graph.invoke(
            {"projects": ["castilla-lived"], "network_projects": ["castilla-lived"]}, thread
        )
