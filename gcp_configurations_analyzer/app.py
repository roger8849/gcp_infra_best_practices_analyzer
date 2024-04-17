

import google.cloud.secretmanager_v1 as secretmanager
import googleapiclient.discovery

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

from langchain.document_loaders import UnstructuredURLLoader

from unstructured.cleaners.core import remove_punctuation, clean, clean_extra_whitespace


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


def query_network_configs(project="castilla-lived"):
    """Queries Google Cloud network configurations and prints results."""

    compute = googleapiclient.discovery.build('compute', 'v1')

    # Replace 'your-project-id' with your actual Google Cloud project ID
    # project = 'your-project-id'
    project = 'castilla-lived'

    # Get a list of networks
    networks_result = compute.networks().list(project=project).execute()
    networks = networks_result.get('items', [])

    if not networks:
        print('No networks found.')
    else:
        print('Networks:')
        for network in networks:
            # print(f"- Name: {network['name']}")
            # print(f"  Description: {network.get('description')}")
            # print(f"  Subnets:")

            print('############################################')
            print(network)

            # Get details for each subnet associated with the network
            subnets_result = compute.subnetworks().list(
                project=project, region='us-central1').execute()
            subnets = subnets_result.get('items', [])

            for subnet in subnets:
                # print(f"    - {subnet['name']}, CIDR: {subnet['ipCidrRange']}")
                print("------------------------")
                print(subnet)
                print("------------------------")

            print('############################################')


def summarize_using_chat(project_id='castilla-lived', secret_id='open_ai_api_key'):
    # List of urls as parameter to
    urls = ["https://cloud.google.com/architecture/best-practices-vpc-design"]

    # create instance of UnstructuredURLLoader class
    loader = UnstructuredURLLoader(urls=urls)

    print(type(loader))

    # Create list of Documents. One for each website content
    data = loader.load()

    print(type(data), type(data[0]))

    print(data)

    print(data[0].page_content)

    chunk_size = 3000
    chunk_overlap = 200

    text_splitter = CharacterTextSplitter(
        # separator = "\n\n"
        chunk_size=chunk_size,  # Maximum size of a chunk
        chunk_overlap=chunk_overlap,  # Maintain continuity, have some overlap of chunks
        length_function=len,  # Count number of characters to measure chunk size
    )
    texts = text_splitter.split_text(data[0].page_content)

    # Create Document objects for each text chunk
    docs = [Document(page_content=t) for t in texts[:]]

    print(len(docs))

    print(docs[0].page_content)

    openai_api_key = access_secret(project_id, secret_id)

    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    # To summarize multiple documents
    # chain = "map_reduce" - find summary for each Document and then summarize all summaries
    map_reduce_chain = load_summarize_chain(llm, chain_type="map_reduce")

    # Perform summarization using run
    # docs - list of documents to summarize
    output = map_reduce_chain.run(docs)
    # install tiktoken
    print('######################################')
    print('final summary of the entire web page')
    print(output)


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


def summarize_document(url, openai_key, model_name='gpt-4'):
    "Given an URL return the summary from OpenAI model"
    llm = OpenAI(model=model_name,temperature=0, openai_api_key=openai_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    tmp_doc = generate_document(url)
    summary = chain.run([tmp_doc])
    return clean_extra_whitespace(summary)


def main():
    # Example usage (replace placeholders)
    project_id = "castilla-lived"
    secret_id = "open_ai_key"
    secret_value = access_secret(project_id, secret_id)
    print('############################################')
    print(secret_value)
    print('############################################')

    query_network_configs()
    # summarize_using_chat(project_id, secret_id)

    # generate_document(
    #     'https://cloud.google.com/architecture/best-practices-vpc-design')
    # summarize_document('https://cloud.google.com/architecture/best-practices-vpc-design', secret_value)


if __name__ == "__main__":
    main()
