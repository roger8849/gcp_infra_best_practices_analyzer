from google.cloud.secretmanager import SecretManagerServiceClient



def access_secret(project_id, secret_id, version_id="latest"):
    """
        Retrieves the value of a secret from Secret Manager.

        Args:
            project_id: The ID of the Google Cloud project.
            secret_id: The ID of the secret.
            version_id: The ID of the secret version. Defaults to "latest".

        Returns:
            The secret value as a string, or None if the secret is not found.
    """

    client = SecretManagerServiceClient()

    # Build the resource name of the secret version.
    secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": secret_path})

    # Extract the secret payload.
    secret_payload = response.payload.data.decode("utf-8")

    return secret_payload
