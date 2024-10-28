import logging
import re

from google.cloud import compute_v1

import utils.app.console_utils as cu


def get_organization_id() -> str:
    cu.print_normal_message("Insert your organization id")
    while True:
        try:
            cu.print_normal_message(
                "Insert your organization id, must be a number of 12 digits. I.E: <885157069XXX>"
            )
            org_id = input("")
            if org_id and len(org_id) == 12 and org_id.isnumeric:
                return int(org_id)
            else:
                logging.error(
                    f"{org_id}  is not a number of 12 digits please try again"
                )
        except KeyboardInterrupt:
            logging.error("\n Org id input canceled.")
            return None


def get_project_id() -> str:
    """
    Reads a project ID from the console with validation.

    Returns:
      The valid project ID entered by the user, or None if the user gives up.
    """

    pattern = r"^[a-z][a-z0-9-]{2,28}[a-z0-9]$"  # Regex for valid project ID

    while True:
        try:
            project_id = input(
                "Enter a project ID (4-30 chars, lowercase, digits, hyphens): "
            )
            if re.match(pattern, project_id):
                return project_id
            else:
                logging.error(f"The project id {project_id} has an invalid format.")
        except ValueError:
            logging.error("Invalid project ID format.")
        except KeyboardInterrupt:
            print("\nInput canceled.")
            return None


def get_all_regions(project_id="castilla-lived"):
    """
    Retrieves a list of all regions available in a given project.

    Args:
      project_id: The ID of the Google Cloud project.

    Returns:
      A list of region names (e.g., ['us-central1', 'europe-west1']).
    """
    try:
        client = compute_v1.RegionsClient()
        # request = compute_v1.ListRegionsRequest(project=project_id)
        request = compute_v1.ListRegionsRequest(project="")
        response = client.list(request=request)

        regions = [region.name for region in response.items]
        print(regions)
        return regions
    except Exception as e:
        print(f"Error getting regions: {e}")
        return []
