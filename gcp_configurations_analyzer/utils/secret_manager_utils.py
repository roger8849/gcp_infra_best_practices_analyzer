from google.cloud import secretmanager

class SecretManagerUtils:
    """
    A utility class for interacting with Google Cloud Secret Manager.
    """

    def __init__(self, project_id):
        """
        Initializes a new SecretManagerUtils instance.

        Args:
            project_id: The ID of the Google Cloud project.
        """
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def get_secret(self, secret_id):
        """
        Retrieves the value of a secret from Secret Manager.

        Args:
            secret_id: The ID of the secret.

        Returns:
            The secret value as a string, or None if the secret is not found.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

# Example usage
if __name__ == "__main__":
    # Replace with your actual project ID and secret ID
    project_id = "castilla-lived"
    secret_id = "your-secret-id"

    utils = SecretManagerUtils(project_id)
    secret_value = utils.get_secret(secret_id)

    if secret_value:
        print(f"The secret value is: {secret_value}")
    else:
        print(f"Secret not found: {secret_id}")