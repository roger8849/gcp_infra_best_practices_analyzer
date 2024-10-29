import logging
import re

import requests
from bs4 import BeautifulSoup

import utils.gcp.secret_manager_utils as smu


def get_api_key(project_id, key_name) -> str:
    """
    Retrieves an API key from either Google Cloud Secret Manager or the console.

    Args:
        project_id: The ID of the Google Cloud project.
        key_name: The name of the API key.

    Returns:
        The API key as a string, or None if the user gives up.
    """

    logging.info(f"Choose how to retrieve the {key_name}:")
    logging.info(
        f"1. From Google Cloud Secret Manager (project_id: {project_id}, secret_id: {key_name})"
    )
    logging.info("2. From the console")

    while True:
        try:
            choice = input("Enter your choice (1 or 2): ")
            if choice == "1":
                # Retrieve from Secret Manager
                return smu.access_secret(project_id, key_name)
            elif choice == "2":
                # Read from console with validation
                pattern = r"^.{10,100}$"  # Regex for 10 to 100 characters
                while True:
                    try:
                        api_key = input(f"Enter the {key_name} (10-100 chars): ")
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


def setup_langsmith_tracking(project_id) -> dict:
    """
    Asks the user if they want to track the application execution using LangSmith
    and prompts for the LangChain API key if needed.

    Returns:
      A dictionary containing the 'track' status (True/False) and the
      'langchain_api_key' if provided, or None if the user chooses not to track.
    """

    while True:
        try:
            choice = input(
                "Do you want to track application execution with LangSmith? (y/n): "
            )
            if choice.lower() == "y":
                return {
                    "track": True,
                    "langchain_api_key": get_api_key(project_id, "langchain_api_key"),
                }

            elif choice.lower() == "n":
                return {"track": False, "langchain_api_key": None}
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
        except KeyboardInterrupt:
            print("\nInput canceled.")
            return None


def extract_text_from_url(url):
    """
    Extracts the text content from a given URL.

    Args:
    url: The URL to extract text from.

    Returns:
    The extracted text content as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Get text from all remaining elements
        text = soup.get_text()

        # Clean up the text (remove extra whitespace)
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
