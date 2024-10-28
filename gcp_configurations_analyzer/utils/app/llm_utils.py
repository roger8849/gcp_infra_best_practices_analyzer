import logging
import re

import utils.gcp.secret_manager_utils as smu


def get_llm_api_key(project_id):
    """
    Provides two options for retrieving the llm_api_key:
      1. From Google Cloud Secret Manager
      2. From the console with validation

    Args:
      project_id: The ID of the Google Cloud project.

    Returns:
      The llm_api_key retrieved from the chosen source.
    """

    logging.info("Choose how to retrieve the llm_api_key:")
    logging.info(f"1. From Google Cloud Secret Manager (project_id: {project_id}, secret_id: llm_api_key)")
    logging.info("2. From the console")

    while True:
        try:
            choice = input("Enter your choice (1 or 2): ")
            if choice == "1":
                # Retrieve from Secret Manager
                return smu.access_secret(project_id, "llm_api_key")
            elif choice == "2":
                # Read from console with validation
                pattern = r"^.{10,100}$"  # Regex for 10 to 100 characters
                while True:
                    try:
                        api_key = input("Enter the llm_api_key (10-100 chars): ")
                        if re.match(pattern, api_key):
                            return api_key
                        else:
                            logging.error(
                                "Invalid API key length. Please enter between 10 and 100 characters."
                            )
                    except KeyboardInterrupt:
                        logging.error("\nInput canceled.")
                        return None
            else:
                logging.error("Invalid choice. Please enter 1 or 2.")
        except KeyboardInterrupt:
            logging.error("\nInput canceled.")
            return None

