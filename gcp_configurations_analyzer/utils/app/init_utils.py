import logging
from inspect import _void

import utils.app.console_utils as cu
import utils.gcp.organization_utils as ou
from models.application_configuration import ApplicationConfiguration


class InitUtils:
    def __init__(self) -> _void:
        self.application_configuration = None

    def start_app_init(self) -> _void:
        self.init_logging()
        self.print_welcome_messages()
        self.init_application_configuration()

    def init_logging(self) -> _void:
        logging.basicConfig(level=logging.NOTSET)
    
    def print_welcome_messages(self) -> _void:
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


    def init_application_configuration(self) -> ApplicationConfiguration:
        org_id = ou.get_organization_id()
        project_id = None 

        return ApplicationConfiguration(org_id, project_id, )

