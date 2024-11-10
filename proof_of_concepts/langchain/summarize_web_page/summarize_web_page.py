from langchain.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from unstructured.cleaners.core import remove_punctuation, clean, clean_extra_whitespace
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from google.cloud import secretmanager


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = client.secret_version_path(project_id, secret_id, version_id)

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum.
    if response.payload.data_crc32c != response.payload.data_crc32c:
        print("Data corruption detected.")
        return

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    print("Plaintext: {}".format(payload))

    return payload


def generate_document(url):
    "Given an URL, return a langchain Document to futher processing"
    loader = UnstructuredURLLoader(urls=[url],
                                   mode="elements",
                                   post_processors=[clean, remove_punctuation, clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [
        e for e in elements if e.metadata['category'] == "NarrativeText"]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source": url})


generate_document(
    'https://www.w3schools.com/html/html_editors.asp')
