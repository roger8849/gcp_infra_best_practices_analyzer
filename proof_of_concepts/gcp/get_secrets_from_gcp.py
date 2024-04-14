"""
Explanation:

Import: Imports the google.cloud.secretmanager_v1 library.
access_secret Function
Project ID and Secret ID: Takes your project ID and the secret's ID as input.
Secret Version: Optional version_id parameter to specify the secret version (defaults to "latest")
Client Creation: Creates a Secret Manager client.
Secret Path: Constructs the fully qualified resource name of the secret version.
Accessing the Secret: Retrieves the secret version using client.access_secret_version.
Decoding: Decodes the secret payload from bytes to a UTF-8 string.
Example Usage:
Replace your-project-id and your-secret-name with the appropriate values.
The access_secret function is called, and the returned secret value is printed.


Key Points:

Authentication: Make sure you've authenticated your Google Cloud environment (e.g., gcloud auth application-default login).
Permissions: The service account you're using needs the Secret Manager Secret Accessor role to read secrets.
"""


import google.cloud.secretmanager_v1 as secretmanager

def access_secret(project_id, secret_id, version_id="latest"):
    """Accesses the payload for the given secret version."""

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": secret_path})

    # Extract the secret payload.
    secret_payload = response.payload.data.decode("utf-8")

    return secret_payload

# Example usage (replace placeholders)
your_project_id = "castilla-lived"
your_secret_id = "open_ai_key"
secret_value = access_secret(your_project_id, your_secret_id)
print(secret_value)


