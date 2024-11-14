import logging
import re

from google.cloud import compute_v1
from google.cloud import resourcemanager_v3

from utils.app.console_utils import ConsoleUtils as cu


class OrganizationUtils:
    @staticmethod
    def get_organization_id() -> int:
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
                return 0

    @staticmethod
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
                    print()
            except ValueError:
                logging.error("Invalid project ID format.")
            except KeyboardInterrupt:
                logging.error("\n Project id Input canceled.")
                return ''

    @staticmethod
    def get_all_regions(project_id: str) -> list:
        """
        Retrieves a list of all regions available in a given project.

        Args:
          project_id: The ID of the Google Cloud project.

        Returns:
          A list of region names (e.g., ['us-central1', 'europe-west1']).
        """
        try:
            client = compute_v1.RegionsClient()
            request = compute_v1.ListRegionsRequest(project=project_id)

            response = client.list(request=request)

            regions = [region.name for region in response.items]
            # print(regions)
            return regions
        except Exception as e:
            logging.error(f"Error getting regions: {e}")
            return []




    @staticmethod
    def get_folders(parent_id, folders=None):

        # This function will return a list of folder_id for all the folders and
        # subfolders respectively

        if folders is None:
            folders = []

        # Creating folder client
        client = resourcemanager_v3.FoldersClient()
        request = resourcemanager_v3.ListFoldersRequest(
            parent=parent_id,
        )

        page_result = client.list_folders(request=request)
        for pages in page_result:
            folders.append(pages.name)
            OrganizationUtils.get_folders(parent_id=pages.name, folders=folders)
        return folders

    @staticmethod
    def search_projects(folder_id):
        # This function will take folder_id input and returns
        # the list of project_id under a given folder_id

        client = resourcemanager_v3.ProjectsClient()

        query = f"parent:{folder_id}"
        request = resourcemanager_v3.SearchProjectsRequest(query=query)
        page_result = client.search_projects(request=request)
        search_result = []
        for pages in page_result:
            search_result.append(pages)
        return search_result

    @staticmethod
    def list_projects(organization_id : str) -> list:
        # will returns the list of all active projects(project_id)
        active_project = []
        for folders in OrganizationUtils.get_folders(parent_id=f"organizations/{organization_id}", folders=None):
            for projects in OrganizationUtils.search_projects(folders):
                if str(projects.state) == "1":
                    # print(str(projects.state))
                    active_project.append(projects.project_id)

        return active_project
