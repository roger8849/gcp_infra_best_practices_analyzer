import logging
from inspect import _void

import utils.app.console_utils as cu
import utils.gcp.organization_utils as ou
from models.application_configuration import ApplicationConfiguration
import utils.app.app_utils as appu
from langchain_openai import ChatOpenAI
import os


class InitUtils:
    application_configuration : ApplicationConfiguration
    
    @staticmethod
    def start_app_init() -> _void:
        InitUtils.init_logging()
        InitUtils.print_welcome_messages()
        InitUtils.init_application_configuration()
    
    @staticmethod
    def init_logging() -> _void:
        logging.basicConfig(level=logging.NOTSET)
    
    @staticmethod
    def print_welcome_messages() -> _void:
        # printing welcome message
        cu.print_heading1_message(
            "Welcome to the google cloud best practices analyzer powered by LLMs"
        )
        cu.print_heading2_message(
            "This application works with Google Cloud SDK make sure you have it installed and you have run:"
        )
        cu.print_heading2_message("Initialized gcloud sdk: gcloud init")
        cu.print_heading2_message(
            "Initialized application default credentials: gcloud auth application-default login"
        )
        cu.print_heading2_message("Otherwise the application won't work properly.")

    @staticmethod
    def _set_env(var: str, value: str) -> _void:
        os.environ[var] = value
        
    @staticmethod
    def init_application_configuration() -> ApplicationConfiguration:
        org_id = ou.get_organization_id()
        project_id = ou.get_project_id() 
        llm_api_key = appu.get_api_key(project_id, "llm_api_key")
        langchain_config = appu.setup_langsmith_tracking(project_id)
        InitUtils.application_configuration = ApplicationConfiguration()

        if langchain_config['track']:
            langchain_api_key = langchain_config['langchain_api_key']
            InitUtils._set_env("LANGCHAIN_TRACING_V2", "true")
            InitUtils._set_env("LANGCHAIN_API_KEY", langchain_api_key)
            InitUtils._set_env("LANGCHAIN_PROJECT", "langchain-academy")
            InitUtils.application_configuration.langchain_api_key = langchain_api_key
        

        InitUtils.application_configuration.main_organization_id = org_id
        InitUtils.application_configuration.main_project_id = project_id
        InitUtils.application_configuration.llm_api_key = llm_api_key
        InitUtils.application_configuration.region_list = ou.get_all_regions(project_id)

        InitUtils.application_configuration.llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=llm_api_key)
        
    def get_application_configuration() -> ApplicationConfiguration:
        return InitUtils.application_configuration

